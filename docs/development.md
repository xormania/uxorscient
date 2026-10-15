# Developing UXorscient

The repository root is the distributable Composer library. `dev/app` is a
separate Symfony application that consumes it through a Composer path repository.
Its own autoloading, runtime dependencies, configuration and generated cache stay
inside that application. It has no sibling UXor recipe paths and no database.

The fixture starts on Symfony 7.4 and UX 3.5.1 with PHP >=8.4. The prepared Docker
runtime uses PHP 8.5. A supported-version claim belongs to the combinations that
CI actually exercises; the environment definition alone is not a passing test.

## Native development

Provide PHP >=8.4 and Composer 2 with the extensions required by the lockfiles.
Then run from the repository root:

```sh
python3 dev/run.py --native prepare
python3 dev/run.py --native check
python3 dev/run.py --native serve
```

The last command serves in the foreground. Stop it with Ctrl-C. In a second
terminal, `python3 dev/run.py --native status` checks a real Symfony request and
prints the application URL. The default port is stable for the checkout's
canonical path. Set `UXORSCIENT_HTTP_PORT=21080` on every command to select an
explicit port. Separate worktrees receive separate default ports and mutable
fixture directories.

`PHP_BIN` selects an executable path. `COMPOSER_BIN` selects an executable path or
a `.phar` file, which the runner invokes through `PHP_BIN`. These are paths,
not shell command strings. `prepare --no-assets` skips importmap downloads for
console-only work; browser readiness requires the normal preparation.

Preparation installs the root and application locks, preserves an existing
`.env.local`, generates a private development secret when it is absent, warms
the application container, initializes Mate and explicitly discovers extensions.
Repeating Mate initialization
keeps its existing configuration; its upstream initializer owns generated
instructions and skill discovery. Track intentional lock changes in the PR.

## Prepared Docker development

Provide Python >=3.9, Git, a working Docker engine, Docker Compose v2 and registry
and dependency access. The selected resources are accepted `linux/amd64` xorder
images, pinned by digest in `xorder-support.lock.json` and
`dev/serena-support.lock.json`.

```sh
python3 dev/run.py up
python3 dev/run.py status
python3 dev/run.py check
python3 dev/run.py exec bin/console list make --format=json
python3 dev/run.py exec vendor/bin/mate tools:list --format=json
python3 dev/run.py down
```

The first use fetches the reviewed xorder source revision
`97cb40b083f4ccf16148355c4e785ed0c6e4b00a` into ignored `dev/.tools/xorder`.
Alternatively, `XORDER_DIR` can select an existing clean checkout at that revision.
The runner consumes xorder's support checker and Serena launcher directly.
No provider implementation is copied into UXorscient.

The support checker obtains current release policy before a pull and validates
Docker-observed image identities before project commands. Workloads against an
already running stack also validate actual container images. An explicit
`XORDER_SUPPORT_POLICY_FILE` may select a recently fetched offline receipt under
xorder's [documented freshness rules](https://github.com/xormania/xorder/blob/97cb40b083f4ccf16148355c4e785ed0c6e4b00a/docs/downstream-support.md).
Update the release group and image selections together after checking the
replacement. Cached image bytes do not extend group support.

The application uses FrankenPHP with project-owned Caddy configuration, a
loopback HTTP port and per-worktree Compose project/volumes. Composer downloads
persist in the stack's home volume. Source, installed dependencies and generated
application state belong to the selected checkout; do not share another
worktree's mutable `vendor` or compiled Symfony container.

`down` and `status` remain usable for cleanup and diagnosis when a group expires.
The runner does not start Docker, provide registry authentication, or relay a
host-only network proxy. Use a network configuration reachable from containers;
the native path remains available when Docker is unavailable. No host home or
Docker socket is mounted into the application.

## Native tools and application exercises

Commands run in `dev/app` through its runtime. Prefix them with `--native` when
using host PHP:

```sh
python3 dev/run.py exec bin/console debug:container App\\Controller\\DevelopmentController
python3 dev/run.py exec bin/console make:command
python3 dev/run.py exec vendor/bin/mate tools:list --format=json
python3 dev/run.py exec bin/console ux:install button --kit=https://github.com/xormania/uxor
```

The last command uses normal Toolkit installation. The selected kit revision and
any follow-up Composer, CSS and asset work must be recorded for a reproducible
UXor task. Source copied into the fixture belongs to the fixture. The initial
page separately exercises a local Stimulus counter and a Turbo Frame; these are
environment smoke interactions, not a substitute for a completed UXor workflow.

Mate uses the fixture's compiled container. Its configuration advertises the
matching native/container runner invocation. `mate.php_version` is unpinned
because both PHP 8.4 and 8.5 are development candidates; dependency checks and CI
establish the exercised runtime. Use this runner when switching modes so the
generated agent instructions reflect the selected invocation.

## Serena v2 REPL

Prepare the external provider once, then register the stdio command in the
agent's MCP configuration:

```sh
python3 dev/run.py serena --prepare
python3 /absolute/path/to/uxorscient/dev/run.py serena --write
```

Omit `--write` for inspection. MCP startup does not pull images. Each worktree
has a separate prepared index and project binding. The root project exposes
library and consuming-application source together. Install its own dependencies
before indexing.

Run `python3 dev/check-serena.py` after application preparation to collect actual
provider evidence. It checks PHP symbol lookup, variables retained across cells,
an edit that remains after a deliberately failed cell, and a reconnect that loses
REPL variables while retaining that edit. It edits only a uniquely named temporary
PHP probe, closes both sessions and removes the probe. A per-worktree lease keeps
verification runs serialized. The resulting receipt is
`dev/.state/serena-evidence.json`; source definitions and mocked harness tests do
not establish these provider behaviors. Docker CI runs the real check.

Call `initial_instructions` first. Use the returned session ID for every
`serena_repl` call, and discover the current operation definitions before calling
them. For example, after initial instructions:

```python
s.info('lsp.find_symbol', 'lsp.find_referencing_symbols')
s.lsp.find_symbol('DevelopmentController', relative_path='dev/app/src/Controller/DevelopmentController.php')
```

Cells retain variables. A failed or interrupted cell may already have changed
files: inspect the error and resulting source before retrying. Reconnecting
creates new REPL variables while source edits remain. No automatic replay is
performed. Use separate worktrees for concurrent editing.

PHPactor covers explicit PHP symbols and references. Twig, service names,
Stimulus lifecycle/action names and other convention-based entry points also
require text search; an empty references result does not prove they are unused.
The prepared provider supplies PHPactor and JavaScript/TypeScript support. Its
REPL has the capabilities granted by the external runner; it is not an
application-specific role policy or coordination system.

## Checks and provenance

`check` validates the application container and Twig templates, lists Mate tools
and asks Mate to inspect the actual compiled controller service. `status` establishes a served health
response. Browser interaction and independent package-archive installation are
additional acceptance evidence, not implied by either command.

The small runner checks execute without Docker or PHP:

```sh
python3 -m unittest discover -s dev/tests -v
```

The environment reuses:

- [xorder resource selection](https://github.com/xormania/xorder/blob/97cb40b083f4ccf16148355c4e785ed0c6e4b00a/README.md), its prepared FrankenPHP and Serena artifacts, and support checks.
- [xorder's clean Symfony Toolkit baseline](https://github.com/xormania/xorder/tree/97cb40b083f4ccf16148355c4e785ed0c6e4b00a/examples/php-toolkit/symfony-7.4) for the small independent-consumer arrangement and dependency-placement lessons.
- [UXor's demo](https://github.com/xormania/uxor/tree/40d957cd1ea7766ac0dee742816948ce5ae05bc3/demo) for practical Symfony, AssetMapper, Stimulus, Turbo and Mate integration.
- [Serena provider behavior](https://github.com/xormania/xorder/blob/97cb40b083f4ccf16148355c4e785ed0c6e4b00a/docs/serena.md) for session, recovery and semantic-navigation limits.

The fixture configuration is maintained here. Its minimal wiring is intentionally
independent of the demo's repository-relative autoloading, optional services and
application-specific launch scripts.
