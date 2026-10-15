# A complete consuming application

The development application exposes `/customers` as a small application task:
search, sort and page customer records, edit a record, correct validation errors,
and save it with feedback. Its application code uses the real installed UXor
DataTable, Modal, form theme and Toast. The reference source is pinned to UXor
`40d957cd1ea7766ac0dee742816948ce5ae05bc3`.

Prepare the normal development environment first, then install the selected
components through Symfony UX Toolkit from the repository root:

```sh
python3 dev/run.py --native prepare
python3 dev/install-uxor.py
```

`install-uxor.py` runs `ux:install` with the pinned GitHub kit reference, downloads
Importmap assets, locks the icons and builds Tailwind through TailwindBundle. It
uses the application's installed Toolkit. Component PHP lands in
`dev/app/src/UXor/` and uses the application's normal `App` PSR-4 mapping and service
configuration. There is no sibling UXor autoload or recipe directory mapping.
Set `TAILWIND_BINARY` to an existing compatible CLI (the prepared UXor image provides
`/usr/local/bin/tailwindcss`) to reuse it; otherwise TailwindBundle downloads the
UXor demo's pinned v4.3.3 binary. The fixture's regular Composer requirements contain the runtime dependencies;
Toolkit and UXorscient are development dependencies.

The installer records component source hashes under `var/workflow-uxor.json`.
Repeated installation verifies these files and avoids replacing them. Missing or
customized files stop setup with an inspection instruction. After a failed first
installation, inspect the files already created before retrying; the normal
Toolkit invocation never uses `--force`. This is a development fixture installer,
not an automatic component upgrade mechanism for applications.

Run `python3 dev/run.py --native serve` and open `/customers`. The basic development
page remains available before this selected workflow is installed. Workflow CSS
is separate from the basic fixture stylesheet. Container users can execute the
installer through their container's Python environment, or run its documented
Symfony commands in `dev/app`; the prepared native CI job exercises the complete
installation.

## Application responsibilities

`CustomerStore` initializes a few records in each browser's session. Each test
context gets isolated mutable state. This removes a database prerequisite for the
example while preserving actual server-side validation and saved state across
requests. It is a reference application with no authentication or multi-user
persistence; a production application supplies its own repository and access
control.

`CustomersTable` provides business querying and sorting. Installed UXor code owns
query normalization, pagination controls and the promoted Turbo Frame. Table
searches and page changes advance browser history. The edit frame does not add a
history entry. A failed Symfony form submission returns HTTP 422 with accessible
field errors. A successful Turbo submission replaces the table and editor frame
with streams and appends one Toast to its permanent region. An application
Stimulus controller restores focus to the edited row, or to search when the row
no longer matches. A direct non-JavaScript edit request renders an ordinary form
and uses HTTP 303 after a successful save.

The security header listener adapts the UXor demo's request-scoped nonce pattern.
The application enforces CSP with nonce-based scripts, strict-dynamic and no
inline event handlers or style attributes. Nonces belong to each request so a
long-running PHP worker does not share one between requests.

## Browser proof

```sh
npm ci
npx playwright install --with-deps chromium
npm run test:workflow
```

The check starts a local PHP server on port 8765. Set `UXORSCIENT_BASE_URL` to test
an already served instance instead. A local environment with an existing browser
can set `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`; CI uses Playwright's pinned Chromium.

The main journey checks table Back/Forward in the same document, search state,
modal focus, server validation, accessible errors, stream updates, saved data,
feedback, restored focus and history after saving. A second journey verifies
ordinary browser form validation and the successful redirect. A focused third
case verifies that a row leaving the active search disappears and focus returns
to search. Console errors,
page errors, failed requests and CSP violations fail the main journey. Frame and
stream completion is verified from the resulting state; these interactions do
not wait for an unrelated `turbo:load` event. This suite checks application
composition rather than reproducing UXor's comprehensive component tests.
