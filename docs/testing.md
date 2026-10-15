# Validation

The package/application, prepared-environment, consumer-workflow and CodeQL jobs
run on pull requests and pushes to `dev` or `master`. CodeQL also runs for
documentation changes so a ruleset requiring analysis receives a result for the
PR. Branch creation and a passing run do not configure required GitHub checks;
the maintainer manages those settings as described in [GitHub workflow](github.md).

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
environment. Hosted CI also starts the prepared Docker environment, applies the
xorder support checks, verifies FrankenPHP application readiness and stops the
environment afterward. Docker checks require a working engine and access to the
prepared images.

The same Docker job runs `python3 dev/check-serena.py` through the pinned external
MCP client. It verifies semantic source lookup, persistent REPL variables, a
partial file change surviving a failed cell, and a fresh session resetting its
variables while preserving source changes. A successful run writes
`dev/.state/serena-evidence.json`, retained as a short-lived CI artifact. The check
removes its owned scratch file and never edits application source for this probe.

When the companion's knowledge and services are present, verify distribution in a
separate application with:

```sh
python3 tools/check-package.py --consumer
```

This builds a real Composer archive, copies only the tracked Symfony fixture into
a temporary directory, and installs the archive as a development dependency with
no source symlink. It calls the discovered Mate catalog operation, reads a
packaged reference, checks the source revision and all three installed skills,
and repeats initialization with existing consumer instructions before and after
the managed block. Mate can refresh its own managed content; consumer-authored
content must survive.

The same consumer then updates between two temporary archive versions with different
instruction and build-skill content. It checks Composer's installed version and
distribution metadata, runs the documented `vendor/bin/mate discover` refresh,
and verifies that the new guidance replaces the old content while consumer
instructions and a customized application component remain intact. No source
checkout is linked into either installation, and no vendor files are patched.
The explicit refresh matters: Mate 0.14.0's plugin resolved Composer 2.10.3's own
root inside its PHAR in this check, leaving application guidance unchanged.

Finally it removes development dependencies, clears the production container and
boots the application to render both its health endpoint and Twig page. This
proves the companion can remain development-only. Full Turbo browser interaction
is verified by its dedicated workflow; these checks do not claim that journey.
Successful checks remove their temporary application. A failed check prints and
retains its temporary directory for inspection; remove it after investigating.

CodeQL checks the Python environment and packaging tools. PHP is checked through
linting, Symfony container/template checks and the package behavior suite because
CodeQL does not support PHP.

Keep tests tied to observable contracts. Reuse the fixture and test setup; add a
check when a failure changes installed behavior or the evidence agents receive.
Do not duplicate the demo's complete test suite in this package.
