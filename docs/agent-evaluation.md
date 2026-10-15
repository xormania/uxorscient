# Bounded consuming-application evaluation

On 2026-10-15, a fresh-context agent received one product task: make the customer
list sortable by Email while retaining search, pagination, Turbo history, Name
sorting, validation and saving. The task began from UXorscient
`0d56aa1177c3309c021dbcd575bfddda5e746482` in an isolated worktree, with no
implementation steps supplied. This records one bounded task, not a general
model-performance assessment.

The local starting commit has a published, byte-identical counterpart:
[`94f4da25623fe685b5e9f66b86010b1c4c0e63ce`](https://github.com/xormania/uxorscient/commit/94f4da25623fe685b5e9f66b86010b1c4c0e63ce).
Both committed trees were verified as
`52486e76d0c9f637ae1019e22743440614c78bdc` before publication. Use that remote
commit to reproduce the starting source without relying on the local worktree's
commit identity.

## Reproduction context

| Input | Exercised value |
| --- | --- |
| Companion | Local `dev-master` path dependency at the base revision above |
| UXor source and packaged reference | `40d957cd1ea7766ac0dee742816948ce5ae05bc3` |
| Installation | Installed Symfony UX Toolkit 3.5.1 via `python3 dev/install-uxor.py`; normal `App\` autoloading of copied `src/UXor/` source |
| Runtime | Linux, PHP 8.4.26, Composer 2.10.3, Symfony FrameworkBundle 7.4.21, Symfony UX 3.5.1, Mate 0.14.0 |
| Assets | Tailwind CLI/CSS 4.3.3, Flowbite stylesheet 4.0.2, Turbo 8.0.23 |
| Harness | Node 24.19.0, Python 3.12.14, Playwright 1.58.2, Chromium headless shell 145.0.7632.6 |
| Serving | Existing Playwright configuration, native PHP server at `127.0.0.1:8765`, one worker, zero retries |

Preparation used `COMPOSER_ALLOW_SUPERUSER=1 python3 dev/run.py --native prepare`
and `npm ci`. The browser executable was selected through
`PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`. No sibling UXor source/autoload shortcut was
used. Docker was unavailable; Serena was not invoked.

Before implementation, the installed
`dev/app/templates/components/DataTable.html.twig` received this deterministic
comment followed by a newline, prepended to its original bytes:

```twig
{# UXorscient agent evaluation: preserve application-owned DataTable customization. #}
```

Its SHA-256 changed from
`2a984fd8f5940cf1f266a843b6cd895b6fb307bacebc06a10a7728a1a3a8613e`
to `b4f963ac4d0bce36c3ba71007ca1fbf1501ea72ebde23e6d7e05896fc00eb342`.
That customized hash remained identical after implementation and browser checks.
The other 46 installed source files still matched the Toolkit installation
receipt. Installed sources and the local receipts remain ignored development
state; the template was not changed to implement sorting.

## Discovery and implementation

The agent read repository instructions, the shipped setup/build/verify skills,
and generated application Mate instructions. It used the UXorscient CLI's
`component data-table` and `inspect --project-root=dev/app`, then installed Mate's
`tools:list`, `tools:inspect` and `tools:call` commands. Actual calls covered
`uxorscient_reference` for DataTable and the Guide, `uxorscient_workflow` for
customer management, `uxorscient_project`, `symfony-service-detail` for the table
and `server-info`. Text search and source inspection checked the installed
normalization/rendering contracts and existing application/browser code.

The application table now declares Email sortable and uses the normalized
`TableQuery::sortField`, with the record ID breaking ties before pagination.
The installed table continues to own query validation, links and Turbo behavior.
An independent read-only agent review after implementation found no concrete
defects. There was no human implementation coaching or intervention during the
task; the PHP, Composer and browser provision was supplied before it began.

## Executed checks and failures

The new browser case changes an email through the real editor so Email and Name
orders differ. A selective search matches three records. It checks both sort
directions and exact row order, page reset, pagination, the retained search and
unrelated query parameter, same-document Back/Forward, and saving a row that moves
off the current sorted page with useful focus and persisted state.

- The focused browser case passed on its first run. A controlled negative check
  temporarily forced Name ordering; it failed on the expected Email row order.
  The source was restored before final verification.
- The first full browser run exposed a test synchronization race: visible rows
  and URL preceded completion of Turbo's promoted history visit. Back aborted a
  request. An attempted wait on the frame's `complete` JavaScript property also
  failed because that property stayed false after a GET form submission in this
  installed Turbo version. The final test awaits the frame's `loaded` promise
  and the document's cleared `aria-busy` state before continuing.
- Initial Tailwind execution through an npm CLI in another checkout could not
  resolve `tailwindcss` from this app. Installing
  `@tailwindcss/cli@4.3.3 tailwindcss@4.3.3` locally with
  `--no-save --package-lock=false` and setting `TAILWIND_BINARY` to that CLI
  completed the build. The repeat installer verified existing files without
  overwriting them. No dependency lock changed.

Final verification:

| Check | Observed result |
| --- | --- |
| `python3 dev/run.py --native check` | Passed container wiring, all 44 Twig files, native service inspection and Mate discovery |
| `php -l dev/app/src/Table/CustomersTable.php` and `git diff --check` | Passed |
| `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=<browser> npm run test:workflow` | All four cases passed, zero retries (6.4 seconds) |
| Browser failure collectors | No unexpected console errors, page errors, failed requests or CSP violations in the instrumented cases |
| Customized template and installation receipt | Marker/hash unchanged; all other 46 installed source hashes unchanged |

The existing browser cases retained Name sorting, validation with HTTP 422,
successful streams and feedback, ordinary no-JavaScript saving with HTTP 303,
history and focus restoration. This check covers the selected session-backed
development workflow on the stated runtime. It does not establish other browsers,
PHP/Symfony combinations, production persistence, Serena behavior or broad agent
effectiveness.
