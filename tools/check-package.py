#!/usr/bin/env python3
"""Check the actual Composer export, including files absent from the checkout root."""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import secrets
import shutil
import subprocess
import sys
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".github", "dev", "docs", "tests", "tools", "vendor", "var", "node_modules", "reports"}
EXCLUDED_FILES = {"AGENTS.md", "CONTRIBUTING.md", "composer.lock", "phpunit.xml.dist", "xorder-support.lock.json"}
PACKAGE_DIRECTORIES = ("src", "config", "skills", "resources")


def composer_command() -> list[str]:
    executable = os.environ.get("COMPOSER_BIN", "composer")
    if executable.endswith(".phar"):
        return [os.environ.get("PHP_BIN", "php"), executable]
    return [executable]


def check_archive(archive: Path) -> int:
    with tarfile.open(archive, mode="r:") as package:
        paths: dict[str, tarfile.TarInfo] = {}
        for member in package.getmembers():
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise RuntimeError(f"Unsafe archive path: {member.name}")
            normalized = path.as_posix().removeprefix("./")
            if normalized == ".":
                continue
            if path.parts[0] in EXCLUDED or normalized in EXCLUDED_FILES:
                raise RuntimeError(f"Development-only content exported: {normalized}")
            if member.issym() or member.islnk():
                raise RuntimeError(f"Package must contain portable regular files: {normalized}")
            paths[normalized] = member

        for required in ("composer.json", "LICENSE", "README.md"):
            if required not in paths or not paths[required].isfile():
                raise RuntimeError(f"Required package file missing: {required}")

        for directory in PACKAGE_DIRECTORIES:
            source_files = [path for path in (ROOT / directory).rglob("*") if path.is_file()]
            for source in source_files:
                relative = source.relative_to(ROOT).as_posix()
                if relative not in paths:
                    raise RuntimeError(f"Runtime or agent resource missing from package: {relative}")

        instructions = ROOT / "INSTRUCTIONS.md"
        if instructions.is_file() and instructions.name not in paths:
            raise RuntimeError("Agent instructions missing from package: INSTRUCTIONS.md")

        manifest_file = package.extractfile(paths["composer.json"])
        if manifest_file is None:
            raise RuntimeError("Cannot read exported Composer metadata")
        manifest = json.load(manifest_file)
        if manifest.get("name") != "xormania/uxorscient":
            raise RuntimeError("Unexpected Composer package identity")
        for executable in manifest.get("bin", []):
            if executable not in paths or not paths[executable].isfile():
                raise RuntimeError(f"Declared Composer executable missing from package: {executable}")
        for namespace_path in manifest.get("autoload", {}).get("psr-4", {}).values():
            for path in [namespace_path] if isinstance(namespace_path, str) else namespace_path:
                prefix = path.rstrip("/") + "/"
                if not any(name.startswith(prefix) and entry.isfile() for name, entry in paths.items()):
                    # The initial foundation declares the namespace before adding PHP classes.
                    if any(entry.is_file() for entry in (ROOT / path).rglob("*")):
                        raise RuntimeError(f"Autoload directory missing from package: {path}")

    return sum(entry.isfile() for entry in paths.values())


def execute(arguments: list[str], application: Path, *, capture: bool = False) -> str:
    result = subprocess.run(arguments, cwd=application, check=True, text=True,
                            stdout=subprocess.PIPE if capture else None)
    return result.stdout if capture else ""


def operation_result(payload, operation: str):
    """Find the public operation envelope inside Mate's transport encoding."""
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return None
    if isinstance(payload, dict):
        if payload.get("operation") == operation:
            return payload
        children = payload.values()
    elif isinstance(payload, list):
        children = payload
    else:
        return None
    for child in children:
        result = operation_result(child, operation)
        if result is not None:
            return result
    return None


def consumer_instruction_parts(content: str) -> tuple[str, str]:
    start = "<!-- BEGIN AI_MATE_INSTRUCTIONS -->"
    end = "<!-- END AI_MATE_INSTRUCTIONS -->"
    if content.count(start) != 1 or content.count(end) != 1:
        raise RuntimeError("Initialization must produce exactly one managed instruction block")
    before, managed = content.split(start, 1)
    _, after = managed.split(end, 1)
    return before, after


def versioned_archive(source: Path, destination: Path, version: str) -> str:
    """Make two temporary package versions without changing the maintained checkout."""
    marker = f"UXorscient archive update acceptance: {version}"
    with tarfile.open(source, mode="r:") as original, tarfile.open(destination, mode="w:") as output:
        for member in original.getmembers():
            exported = original.extractfile(member) if member.isfile() else None
            if exported is None:
                output.addfile(member)
                continue
            content = exported.read()
            if member.name == "composer.json":
                manifest = json.loads(content)
                manifest["version"] = version
                content = (json.dumps(manifest, indent=4) + "\n").encode()
            elif member.name in {"INSTRUCTIONS.md", "skills/build/SKILL.md"}:
                content += f"\n\n<!-- {marker} -->\n".encode()
            entry = copy.copy(member)
            entry.size = len(content)
            output.addfile(entry, io.BytesIO(content))
    return marker


def archive_repository(archive: Path) -> dict:
    with tarfile.open(archive, mode="r:") as package:
        exported = package.extractfile("composer.json")
        if exported is None:
            raise RuntimeError("Archive Composer metadata cannot be read")
        dependency = json.load(exported)
    dependency["dist"] = {"type": "tar", "url": archive.as_uri(),
                          "shasum": hashlib.sha1(archive.read_bytes(), usedforsecurity=False).hexdigest()}
    return {"type": "package", "package": dependency}


def check_update(application: Path, manifest: dict, archive: Path, old_marker: str,
                 new_marker: str, build_skill: Path) -> None:
    instructions = application / "AGENTS.md"
    custom_instructions = consumer_instruction_parts(instructions.read_text())
    component = application / "templates/components/ConsumerOwned.html.twig"
    component.parent.mkdir(parents=True, exist_ok=True)
    component.write_text('{# Application-owned custom component. #}\n<span class="consumer-custom">Keep this behavior.</span>\n')
    component_content = component.read_bytes()
    manifest["repositories"] = [archive_repository(archive)]
    (application / "composer.json").write_text(json.dumps(manifest, indent=4) + "\n")
    execute([*composer_command(), "update", "xormania/uxorscient", "--prefer-dist",
             "--no-interaction", "--no-progress"], application)
    installed = application / "vendor/xormania/uxorscient"
    metadata = json.loads((application / "vendor/composer/installed.json").read_text())
    companion = next(package for package in metadata["packages"] if package["name"] == "xormania/uxorscient")
    if installed.is_symlink() or companion["version"] != "0.0.1" or companion.get("installation-source") != "dist":
        raise RuntimeError("Composer update did not install the newer archive as a regular distribution")
    if companion.get("dist", {}).get("url") != archive.as_uri():
        raise RuntimeError("Installed package metadata does not identify the newer archive")
    if json.loads((installed / "composer.json").read_text()).get("version") != "0.0.1":
        raise RuntimeError("Updated package files do not match Composer's installed version")
    # The supported lifecycle refreshes Mate explicitly after Composer updates.
    # Mate 0.14's plugin can resolve Composer's own root when Composer runs as a PHAR.
    php = os.environ.get("PHP_BIN", "php")
    execute([php, "vendor/bin/mate", "discover", "--no-interaction"], application)
    for materialized in (application / "mate/AGENT_INSTRUCTIONS.md", build_skill):
        content = materialized.read_text()
        if new_marker not in content or old_marker in content:
            raise RuntimeError(f"The updated package's Mate refresh did not replace old guidance: {materialized.relative_to(application)}")
    if consumer_instruction_parts(instructions.read_text()) != custom_instructions:
        raise RuntimeError("Composer update changed consumer-owned instructions")
    if component.read_bytes() != component_content:
        raise RuntimeError("Composer update changed an application-owned custom component")
    catalog = operation_result(execute([php, "vendor/bin/mate", "tools:call", "uxorscient_catalog",
                                       "--query=modal", "--limit=1", "--format=json"], application, capture=True), "catalog")
    if catalog is None or catalog.get("status") != "completed" or catalog.get("reference", {}).get("version") != "0.0.1":
        raise RuntimeError("The updated Mate tool does not report the newly installed companion version")
    print("Composer update and native Mate refresh verified: newer archive installed; guidance and skills replaced; consumer instructions and custom component preserved.")


def check_consumer(archive: Path, temporary: Path) -> None:
    application = temporary / "consumer"
    tracked = execute(["git", "ls-files", "-z", "--", "dev/app"], ROOT, capture=True)
    for filename in filter(None, tracked.split("\0")):
        source = ROOT / filename
        destination = application / source.relative_to(ROOT / "dev/app")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    (application / "composer.lock").unlink(missing_ok=True)
    manifest_path = application / "composer.json"
    manifest = json.loads(manifest_path.read_text())
    first_archive = temporary / "uxorscient-0.0.0.tar"
    second_archive = temporary / "uxorscient-0.0.1.tar"
    old_marker = versioned_archive(archive, first_archive, "0.0.0")
    new_marker = versioned_archive(archive, second_archive, "0.0.1")
    manifest["repositories"] = [archive_repository(first_archive)]
    manifest["require-dev"]["xormania/uxorscient"] = "0.0.*"
    manifest_path.write_text(json.dumps(manifest, indent=4) + "\n")
    (application / ".env.local").write_text("APP_SECRET=" + secrets.token_hex(32) + "\n")
    # The fixture's repository wrapper is replaced by the independent application's invocation.
    (application / "mate/config.php").write_text("""<?php
use Symfony\\Component\\DependencyInjection\\Loader\\Configurator\\ContainerConfigurator;
return static function (ContainerConfigurator $container): void {
    $container->parameters()->set('mate.invocation', 'vendor/bin/mate');
};
""")
    custom_instructions = "# Consumer instructions\n\nKeep application decisions here.\n"
    instructions_path = application / "AGENTS.md"
    instructions_path.write_text(custom_instructions)
    execute([*composer_command(), "install", "--prefer-dist", "--no-interaction", "--no-progress"], application)
    installed = application / "vendor/xormania/uxorscient"
    if installed.is_symlink() or not installed.is_dir():
        raise RuntimeError("Independent consumer must install the archive, not a source symlink")
    php = os.environ.get("PHP_BIN", "php")
    mate = [php, "vendor/bin/mate"]
    execute([*mate, "init", "--no-interaction"], application)
    execute([*composer_command(), "dump-autoload", "--no-interaction"], application)
    execute([*mate, "discover", "--no-interaction"], application)
    first_instructions = instructions_path.read_text()
    if not first_instructions.startswith(custom_instructions):
        raise RuntimeError("Mate initialization replaced the consumer's existing instructions")
    expected_instructions = first_instructions + "\nConsumer-owned trailing instructions.\n"
    instructions_path.write_text(expected_instructions)
    execute([*mate, "init", "--no-interaction"], application)
    if consumer_instruction_parts(instructions_path.read_text()) != consumer_instruction_parts(expected_instructions):
        raise RuntimeError("Repeated initialization changed consumer-owned instructions")

    tools = json.loads(execute([*mate, "tools:list", "--format=json"], application, capture=True))
    if "uxorscient_catalog" not in tools.get("tools", {}):
        raise RuntimeError("The installed package's catalog tool was not discovered")
    catalog = operation_result(execute([*mate, "tools:call", "uxorscient_catalog", "--query=modal",
                                       "--limit=1", "--format=json"], application, capture=True), "catalog")
    expected_revision = json.loads((installed / "resources/uxor/index.json").read_text())["source"]["revision"]
    if catalog is None or catalog.get("status") != "completed" or not catalog.get("data", {}).get("items"):
        raise RuntimeError("The discovered catalog tool could not read its exported references")
    if catalog.get("reference", {}).get("uxor", {}).get("revision") != expected_revision:
        raise RuntimeError("Catalog results do not identify the packaged UXor reference revision")
    reference = operation_result(execute([*mate, "resources:read", "uxorscient://reference/FOR-AGENTS.md",
                                         "--format=json"], application, capture=True), "reference")
    if reference is None or reference.get("status") != "completed" or not reference.get("data", {}).get("content"):
        raise RuntimeError("The installed reference resource could not be read through Mate")
    skills = json.loads(execute([*mate, "skills:list", "--format=json"], application, capture=True))
    companion_skills = [skill for skill in skills.get("skills", []) if skill.get("package") == "xormania/uxorscient"]
    if {skill["original_name"] for skill in companion_skills} != {"setup", "build", "verify"}:
        raise RuntimeError("Mate did not discover all three packaged UXorscient skills")
    for skill in companion_skills:
        if not skill["enabled"] or not (application / ".agents/skills" / skill["installed_name"] / "SKILL.md").is_file():
            raise RuntimeError("A companion skill was discovered but not installed for agents")
    if "UXorscient" not in (application / "mate/AGENT_INSTRUCTIONS.md").read_text():
        raise RuntimeError("Packaged UXorscient instructions were not materialized for agents")
    build = next(skill for skill in companion_skills if skill["original_name"] == "build")
    build_skill = application / ".agents/skills" / build["installed_name"] / "SKILL.md"
    for materialized in (application / "mate/AGENT_INSTRUCTIONS.md", build_skill):
        if old_marker not in materialized.read_text():
            raise RuntimeError("The first archive's agent guidance was not installed before the update")
    print("Independent archive consumer: Mate operation, reference, provenance, three skills and repeated initialization verified.")
    check_update(application, manifest, second_archive, old_marker, new_marker, build_skill)

    execute([php, "bin/console", "importmap:install", "--no-interaction"], application)
    execute([*composer_command(), "install", "--no-dev", "--prefer-dist", "--no-interaction", "--no-progress"], application)
    if installed.exists():
        raise RuntimeError("The development-only companion remains installed after --no-dev")
    execute([php, "bin/console", "cache:clear", "--env=prod", "--no-debug", "--no-interaction"], application)
    render = r"""
require 'vendor/autoload.php';
(new Symfony\Component\Dotenv\Dotenv())->bootEnv('.env');
$kernel = new App\Kernel('prod', false);
foreach (['/health' => 'uxorscient-ready', '/' => 'UXorscient'] as $path => $marker) {
    $request = Symfony\Component\HttpFoundation\Request::create($path);
    $response = $kernel->handle($request);
    if (200 !== $response->getStatusCode() || !str_contains($response->getContent(), $marker)) {
        fwrite(STDERR, 'Production consumer did not render '.$path.PHP_EOL);
        exit(1);
    }
    $kernel->terminate($request, $response);
}
$kernel->shutdown();
echo "Production consumer boot and Twig render passed without development dependencies.\n";
"""
    execute([php, "-r", render], application)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer", action="store_true", help="Install the archive in an independent Symfony application and verify Mate and no-dev runtime")
    arguments = parser.parse_args()
    temporary = Path(tempfile.mkdtemp(prefix="uxorscient-package-"))
    try:
        subprocess.run(
            [*composer_command(), "archive", "--format=tar", "--file=uxorscient", f"--dir={temporary}"],
            cwd=ROOT,
            check=True,
        )
        archive = temporary / "uxorscient.tar"
        count = check_archive(archive)
        print(f"Composer archive verified: {count} regular files; development files excluded.")
        if arguments.consumer:
            check_consumer(archive, temporary)
    except BaseException:
        print(f"Failed package check retained for inspection: {temporary}", file=sys.stderr)
        raise
    else:
        shutil.rmtree(temporary)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError, tarfile.TarError) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        sys.exit(1)
