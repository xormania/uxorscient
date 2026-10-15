# Composable agent access

UXorscient exposes the same PHP operations through its CLI and Mate extension.
These are the initial product access surfaces. A Serena-enabled project can
compose them with source navigation and editing through Serena's existing public
`shell.execute_shell_command` API. The project does not inject a custom PHP facade
into Serena or require a second MCP server for this arrangement.

## Basis and evidence boundary

The reviewed Serena source at `b79e2a55f9d4072084977dd35bd07d31146d88b9`
defines the [public shell API](https://github.com/oraios/serena/blob/b79e2a55f9d4072084977dd35bd07d31146d88b9/src/serena/repl/api/shell_api.py).
Its result exposes `stdout`, `stderr`, `return_code` and `cwd`, which let REPL
code parse JSON and return a small useful result. Discover the selected provider's
current API using `s.info()` before invoking it. Shell execution is marked as an
editing capability and is unavailable in the prepared provider's read-only mode.

`python3 dev/check-serena.py --companion` exercises this arrangement against the
prepared provider and the fixture's installed companion. Its ordered trace covers:

1. Discover Serena shell/LSP/edit operations, installed CLI commands and the actual
   Mate schema for component lookup.
2. Select a component, read its bounded packaged reference and inspect the bound
   application's package/runtime metadata.
3. Ask Mate for the fixture controller's actual compiled service definition.
4. Inspect an existing customized temporary PHP probe before editing it.
5. Deliberately fail a cell after an edit; inspect the resulting source, recover
   the intended change and execute that recovered PHP while preserving the
   unrelated customization.
6. Reconnect through a read-only session and establish that old variables are
   gone while the recovered source remains.

The check edits only its own uniquely named temporary probe, preserves the real
fixture controller and closes both sessions. Its receipt records the selected
provider image/source, application root, observed PHP runtime, packaged reference
revision, command exit codes and task steps. A passing receipt is created only
after all checks complete. Hosted CI must execute the check to establish actual
provider evidence; mocked harness tests do not establish interoperation.

This is a **scripted integration check**. It does not evaluate whether a fresh
agent discovers the guidance, chooses the right operations or delivers a feature.
Those outcomes require a separately recorded agent evaluation. Browser behavior
also has separate consumer checks.

## Observed hosted result

On 2026-10-15, the composed probe passed in
[CI run 38711364548](https://github.com/xormania/uxorscient/actions/runs/38711364548)
at repository revision `c776bbd`. The receipt recorded eight CLI/Mate/PHP commands
with exit status zero, all bound to `/workspace/dev/app`, and nine completed checks
including partial-failure recovery and read-only reconnect. The observed command
runtime was PHP 8.5.11 at `/usr/local/bin/php` in the prepared provider.

The source revision and provider image are pinned by `dev/run.py`,
`dev/serena-support.lock.json` and `xorder-support.lock.json`. Receipt artifact
`11960602046` expires on 2026-10-22; the run link and this recorded result remain
useful after artifact expiry. This establishes the selected composed tooling path;
the native PHP 8.4 browser workflow and bounded agent task have separate evidence.

## Runtime and dependency implications

The prepared Serena container mounts the selected checkout and its application
dependencies. The composed PHP commands execute inside that container; its PHP
identity appears in the receipt. Mate reads the same mounted application's dumped
container. The web application remains a separately served runtime, so its
readiness and browser checks are separate evidence.

Serena's public shell capability has the permissions of its container process.
The xorder provider supplies the actual mount, user and networking controls. Its
runtime networking is disabled and no Docker socket is mounted. The integration
does not turn a Python REPL or facade exclusions into an execution sandbox.

The Composer companion requires no Serena runtime dependency. A project choosing
this arrangement prepares the external provider separately. Verification code
under `dev/` is excluded from the Composer distribution.

## Access decision

Use the companion CLI and Mate for the initial release. When the selected Serena
provider exposes shell execution, agents can compose those operations with LSP
and editing in the same REPL session, parse their structured JSON and retain only
the relevant facts. Discover definitions before invoking them; inspect remaining
source after an interrupted cell and avoid automatic edit replay.

A harness that permits only MCP can still use this arrangement when it permits
the Serena REPL and its shell capability. When its provider omits or disallows
shell execution, the CLI path is unavailable through that provider. A thin MCP
adapter over the existing PHP services remains an optional integration to add for
an observed consuming-harness need. The current implementation does not claim
that arbitrary UXorscient operations can be installed as native Serena facades.
