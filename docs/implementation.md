# Implementation status

UXorscient helps agents discover, install, compose, diagnose and verify UXor in a
Symfony application. Work has two deliverables: the environment used to develop
this package and the companion installed as a development dependency elsewhere.

| Work | Deliverable | Evidence required |
| --- | --- | --- |
| Foundation | Composer library, independent Symfony fixture, prepared runtime, Mate and Serena setup | Clean setup, native generation/diagnostics and a served application |
| Knowledge | Generated pinned UXor references and setup/build/verify skills | Exported package has valid resources and discoverable skills |
| Project awareness | Shared catalog, inspection and targeted checks | Real findings, explicit unknowns and correct application binding |
| Application workflow | Selected source-installation and Turbo interaction | Validation, successful save, feedback and coherent history |
| Composable access | Verified Serena/Mate workflow and an appropriate adapter | Observed task and partial-failure recovery |
| Release proof | Independent archive consumer and support matrix | Repeatable installation and runtime with development tools omitted |

The companion now includes pinned references for 64 components, three task skills,
seven CLI/Mate operations and selected-component static wiring checks. An actual
archive consumer verifies first setup, repeated initialization, Composer updates,
explicit Mate refresh and preservation of project instructions and a custom component.
It also boots and renders after development dependencies are removed.

CLI and Mate are the initial product interfaces. The composable-access check uses
Serena's public shell, LSP and edit APIs against the same mounted application;
[the access decision](composable-access.md) records its boundaries. The practical
browser workflow and fresh-agent evaluation are separate acceptance subjects.
Package publication is a later release action; a repository alone does not establish
Packagist availability.

## Exercised support combination

| Part | Executed combination |
| --- | --- |
| PHP and framework | PHP 8.4; Symfony 7.4 |
| UX and agent tooling | Symfony UX 3.5; Mate 0.14; native Makers |
| Composer lifecycle | Composer 2; actual archive install/update and explicit Mate discovery |
| Assets | The current UXor AssetMapper profile; custom profiles return explicit unknowns |
| Serena | Pinned external prepared provider; real symbol/session/recovery checks in hosted CI |

Composer constraints permit additional versions, but those constraints do not
establish executed coverage. Native tooling runs in the selected application's
PHP environment. Browser coverage records its own engine and workflow evidence.

## Reuse

| Capability | Source | Transfer and owner |
| --- | --- | --- |
| Component contracts and dependencies | [UXor](https://github.com/xormania/uxor) manifests and READMEs | Generate references; UXor maintains the contracts |
| Application composition | UXor demo controllers, forms and configuration | Adapt practical workflows into an independent consumer |
| Kit metadata | Symfony UX Toolkit and the demo's KitReader | Prefer existing metadata and isolate compatibility adaptations |
| Framework operations | Installed Makers and Mate | Discover current definitions before invocation |
| Source work | [Prepared Serena](https://github.com/xormania/xorder/blob/97cb40b083f4ccf16148355c4e785ed0c6e4b00a/docs/serena.md) | Use the external v2 REPL provider and its public APIs |
| Environments and clean consumers | [xorder](https://github.com/xormania/xorder) | Select accepted resources, retain locks and verify readiness |
| Verification | Existing install scenarios and selected transition helpers | Adapt behavior checks, isolate mutable state and report failures |

Reference facts, observed project facts, executed evidence and suggested actions
remain distinct. An installed filename alone does not establish a component's
version. Updating companion knowledge does not overwrite application-owned source.
