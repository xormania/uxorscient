#!/usr/bin/env python3
"""Install the workflow's pinned components through Symfony UX Toolkit, then build assets."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'dev/app'
REVISION = '40d957cd1ea7766ac0dee742816948ce5ae05bc3'
KIT = 'https://github.com/xormania/uxor:' + REVISION
RECIPES = ('theme', 'data-table', 'modal', 'toast', 'form-theme')
MARKER = APP / 'var/workflow-uxor.json'


def console(*arguments: str) -> None:
    subprocess.run([os.environ.get('PHP_BIN', 'php'), 'bin/console', *arguments, '--no-interaction'], cwd=APP, check=True)


def installed_files() -> dict[str, str]:
    paths = [*APP.glob('src/UXor/**/*'), *APP.glob('templates/components/**/*'),
             *APP.glob('templates/form/**/*'), *APP.glob('assets/lib/**/*'),
             *APP.glob('assets/controllers/*'), APP / 'assets/styles/uxor.css']
    return {str(path.relative_to(APP)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths) if path.is_file() and path.name not in {'counter_controller.js', 'customer_saved_controller.js'}}


def main() -> None:
    expected = {'repository': 'https://github.com/xormania/uxor', 'revision': REVISION, 'recipes': list(RECIPES)}
    if MARKER.exists():
        recorded = json.loads(MARKER.read_text())
        if any(recorded.get(key) != value for key, value in expected.items()):
            raise SystemExit('The workflow component reference changed. Inspect existing application-owned files before reinstalling.')
        if recorded.get('files') != installed_files():
            raise SystemExit('Installed fixture components are missing or customized. Inspect the changes before reinstalling.')
        print('Existing workflow source installation verified; no component files overwritten.')
    else:
        if installed_files():
            raise SystemExit('Existing component files have no workflow receipt. Inspect them before installing; no files changed.')
        # No force: an existing application's files must never be silently replaced.
        for recipe in RECIPES:
            console('ux:install', recipe, '--kit=' + KIT)
        MARKER.parent.mkdir(parents=True, exist_ok=True)
        MARKER.write_text(json.dumps(expected | {'files': installed_files()}, indent=2) + '\n')
    console('cache:clear')
    console('importmap:install')
    console('ux:icons:lock')
    console('tailwind:build', '--minify')
    console('cache:clear')
    print(json.dumps({'status': 'ready', 'components': expected, 'application': str(APP)}))


if __name__ == '__main__':
    main()
