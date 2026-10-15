#!/usr/bin/env python3
"""Check the actual Composer export, including files absent from the checkout root."""

from __future__ import annotations

import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".github", "dev", "docs", "tests", "tools", "vendor"}
EXCLUDED_FILES = {"AGENTS.md", "CONTRIBUTING.md", "composer.lock", "phpunit.xml.dist"}
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
                    if (ROOT / path).exists():
                        raise RuntimeError(f"Autoload directory missing from package: {path}")

    return sum(entry.isfile() for entry in paths.values())


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="uxorscient-package-") as temporary:
        subprocess.run(
            [*composer_command(), "archive", "--format=tar", "--file=uxorscient", f"--dir={temporary}"],
            cwd=ROOT,
            check=True,
        )
        archive = Path(temporary) / "uxorscient.tar"
        count = check_archive(archive)
        print(f"Composer archive verified: {count} regular files; development files excluded.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError, tarfile.TarError) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        sys.exit(1)
