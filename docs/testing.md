# Validation

CI runs the same native application commands used for development. PHP 8.4,
Composer 2, Node and Python 3 are required. Select another executable with
`PHP_BIN` or `COMPOSER_BIN` when needed; a Composer `.phar` uses `PHP_BIN`.

```sh
composer validate --strict
python3 dev/run.py --native prepare
python3 dev/run.py --native check
python3 tools/check-package.py
```

Run `vendor/bin/phpunit` when package behavior tests are present. PHP files and
the mention checker are syntax checked in CI:

```sh
node --check tools/check-github-mentions.mjs
```

The archive check asks Composer to build the distributed package, checks that
source, configuration, instructions, skills and references survive export, and
rejects development applications, tests, vendors and repository-only instructions.
It reports actual archive contents; a source checkout is not distribution proof.

The foundation's consuming application checks Symfony's container, Twig templates,
the controller service and Mate discovery. This establishes the development
environment. Independent archive installation and the full UX interaction belong
to their implementation slices; these checks do not claim either journey yet.

CodeQL checks the Python environment and packaging tools. PHP is checked through
linting, Symfony container/template checks and the package behavior suite because
CodeQL does not support PHP.

Keep tests tied to observable contracts. Reuse the fixture and test setup; add a
check when a failure changes installed behavior or the evidence agents receive.
Do not duplicate the demo's complete test suite in this package.
