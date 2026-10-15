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

The foundation is the first implementation slice. Subsequent PRs record completed
capabilities and their actual evidence here. Package publication is a later release
action; a repository alone does not establish Packagist availability.

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
and demonstrates search, sorting, pagination, modal editing, server validation,
save streams, feedback and browser history. A filtered-out record returns focus
to search; an ordinary browser form receives a successful HTTP 303 redirect.

The browser checks use Playwright 1.58.2 with Chromium 145.0.7632.6. The consuming
fixture uses PHP 8.4, Symfony FrameworkBundle 7.4, UX packages 3.5.1, Tailwind 4.3.3
and Flowbite stylesheet 4.0.2. The runtime smoke check renders the installed PHP
and Twig after development dependencies, including Toolkit and UXorscient, are
removed. These are selected integration cases; UXor retains its component suite.

The same composition is available to installed agents through the packaged
`uxorscient://workflow/customer-management` guide. Workflow source, browser tools
and application fixtures remain development material outside the Composer archive.
