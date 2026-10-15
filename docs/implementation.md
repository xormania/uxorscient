# Implementation status

UXorscient helps agents discover, install, compose, diagnose and verify UXor in a
Symfony application. Work has two deliverables: the environment used to develop
this package and the companion installed as a development dependency elsewhere.

| Work | Current deliverable | Evidence and limits |
| --- | --- | --- |
| Foundation | Composer library, independent Symfony fixture, prepared runtime, Mate and Serena setup | Native preparation, container/Twig checks and real Mate discovery; prepared provider receipts come from CI |
| Knowledge | Pinned references for 64 components and setup/build/verify skills | Reproducible generation, local reference hashes and actual archive installation |
| Project awareness | Shared catalog, inspection, selected wiring checks, CLI and Mate | Structured findings and unknowns; inspected native Maker/Mate definitions |
| Application workflow | Normally installed DataTable, modal form, streams and Toast | Browser cases cover Name/Email sorting, search/page/history, validation, save/feedback/focus and ordinary form submission |
| Composable access | Shared CLI/Mate operations composed through Serena's public APIs | Dedicated provider trace and partial-failure recovery check; this is scripted integration evidence |
| Release preparation | Archive install/update, preserved consumer content, no-dev rendering and a bounded agent task | Recorded runtime matrix and task result; registry publication remains a maintainer action |

The companion now includes pinned references for 64 components, three task skills,
seven CLI/Mate operations and selected-component static wiring checks. An actual
archive consumer verifies first setup, repeated initialization, Composer updates,
explicit Mate refresh and preservation of project instructions and a custom component.
It also boots and renders after development dependencies are removed.

CLI and Mate are the initial product interfaces. The composable-access check uses
Serena's public shell, LSP and edit APIs against the same mounted application;
[the access decision](composable-access.md) records its boundaries. The practical
browser workflow and [fresh-agent evaluation](agent-evaluation.md) provide separate
application and usability evidence.
Package publication is a later release action; a repository alone does not establish
Packagist availability.

## Exercised support combination

| Part | Executed combination |
| --- | --- |
| PHP and framework | PHP 8.4; Symfony 7.4 |
| Browser workflow UX and agent tooling | Symfony UX 3.5.1; Toolkit 3.5.1; Mate 0.14.0; native Makers |
| Independent archive lifecycle | UX 3.6.0 resolved during clean archive install/update with Toolkit 3.5.1; separate from browser coverage |
| Composer lifecycle | Composer 2; actual archive install/update and explicit Mate discovery |
| Assets | AssetMapper; Tailwind 4.3.3 and Flowbite stylesheet 4.0.2; custom profiles return explicit unknowns |
| Browser | Playwright 1.58.2; Chromium headless shell 145.0.7632.6; four selected consumer cases |
| Serena and composed tooling | Pinned provider; PHP 8.5.11, eight successful CLI/Mate/PHP commands and nine checks in [CI run 38711364548](https://github.com/xormania/uxorscient/actions/runs/38711364548) |

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

## Application workflow

The [independent customer workflow](consumer-workflow.md) installs selected UXor
sources through Toolkit, binds its PHP with the application's normal autoloading,
and demonstrates search, Name/Email sorting, pagination, modal editing, server validation,
save streams, feedback and browser history. A filtered-out record returns focus
to search; an ordinary browser form receives a successful HTTP 303 redirect.

The browser checks use Playwright 1.58.2 with Chromium 145.0.7632.6. The consuming
fixture uses PHP 8.4, Symfony FrameworkBundle 7.4, UX packages 3.5.1, Tailwind 4.3.3
and Flowbite stylesheet 4.0.2. The runtime smoke check renders the installed PHP
and Twig after development dependencies, including Toolkit and UXorscient, are
removed. The integrated four-case browser suite passed with zero retries on this
combination. These are selected integration cases; UXor retains its component suite.

The same composition is available to installed agents through the packaged
`uxorscient://workflow/customer-management` guide. Workflow source, browser tools
and application fixtures remain development material outside the Composer archive.

## Bounded agent result and release preparation

A fresh-context agent extended the consuming application with Email sorting using
the shipped skills, CLI and Mate operations, without implementation coaching.
It preserved an installed template customization, recovered from asset setup and
browser synchronization failures, and verified the added behavior alongside the
existing workflows. The [evaluation record](agent-evaluation.md) identifies the
starting revision, runtime, actual checks and limits. It is one successful bounded
task, not a general model-effectiveness result.

[Release preparation](releasing.md) connects reference regeneration, package and
archive-update checks, installed-component behavior, runtime dependency boundaries,
provider receipts and a recorded agent task. Versioning and registry publication
remain future maintainer actions.
