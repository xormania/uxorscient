# Maintaining the UXor reference bundle

UXor owns the component contracts and documentation. UXorscient packages a selected snapshot so project agents can discover it locally without a sibling checkout or network request. The task skills add procedures for applying that knowledge to an actual application.

## Refreshing

Use a clean UXor checkout at the intended full commit SHA:

```bash
php tools/generate-reference.php --source=/path/to/uxor --revision=40d957cd1ea7766ac0dee742816948ce5ae05bc3
php tools/generate-reference.php --source=/path/to/uxor --revision=40d957cd1ea7766ac0dee742816948ce5ae05bc3 --check
```

The generator requires Git and PHP. It performs no network access, invokes no source-project scripts and adds no timestamps. The same tracked source bytes at the same revision produce identical output. `--check` reads the existing bundle and fails on missing, changed or obsolete generated files. Normal generation replaces generated output, so edit upstream documents rather than `resources/uxor/`.

Review the generated diff with component guidance and the three task skills. Run package checks and artifact installation checks before releasing the updated companion.

## Source selection and reuse

The generator copies UXor's root README, agent onboarding, installation guide, project instruction snippet, component catalog, usage guide, testing guide, every recipe README, license and notice. It discovers recipe manifests from their directories and cross-checks the existing `docs/RECIPES.md` tables, following UXor's `tools/llms-txt.mjs` approach. Categories and summaries come from those tables. Raw decoded recipe manifests are preserved; UXorscient does not implement Toolkit installation semantics or maintain another catalog.

The source revision presently packaged is a documented knowledge snapshot. It does not declare the provenance of a consuming application's installed or customized component files. A release refreshing this bundle updates guidance independently of those application-owned files.

## Bundle contract

`resources/uxor/index.json` has `schema_version: 1` and these fields:

| Field | Meaning |
| --- | --- |
| `source` | Upstream repository URL, full Git revision and kit license |
| `kit` | Upstream root manifest decoded without changing its values |
| `components` | Entries keyed by recipe directory name, sorted by name |
| `documents` | Entries keyed by upstream document path, sorted by path |

Each component contains `summary` and `category` derived from the existing catalog; `manifest`, preserving the upstream recipe manifest; `manifest_sha256` over its original bytes; `documentation`, naming a document key; and an immutable `source_url`.

Each document contains a `path` relative to the bundle directory, `sha256` over the packaged bytes, `source_sha256` over the upstream bytes, and immutable `source_url`. The paired hashes account for link transformations without obscuring the original source. The bundle includes the upstream `LICENSE` and `NOTICE`.

## Links and progressive disclosure

Packaged Markdown retains its upstream directory structure under `resources/uxor/docs/`. Relative links to selected documents remain local. Relative links to other existing source files, such as demo controllers or tests, become GitHub URLs pinned to the same source revision. Images not copied into this small bundle use pinned raw URLs. Moving `main`, `master` and `dev` documentation URLs for this repository are pinned; explicit historical commit links remain intact. Install command arguments remain upstream examples to adapt to the project's selected UXor version.

The three Mate skills contain their own procedures and refer to `uxorscient://catalog` and `uxorscient://reference/<upstream-path>` resources. They do not depend on relative paths escaping their copied skill directories. Resources read only requested reference pages. The skills also explain how to locate the same files under the application's actual Composer vendor directory when Mate is unavailable.

Companion-authored application workflow guides live separately under `resources/workflows/`, with `uxorscient://workflow/<name>` resources and bounded workflow reads. Their context identifies the UXor contract used while preserving UXorscient's ownership of the composition guidance. Reference generation does not replace these authored files.

## Verification

Focused tests exercise generation against a small real Git fixture, deterministic output, catalog/manifest parity, missing dependencies and revision/dirty-check failures. Bundle checks verify document hashes and packaged local link destinations. Distribution checks must inspect the actual Composer archive and install it independently, because path repositories can hide missing exported resources.

The package's tests cover delivery and project interpretation. UXor's component suite remains the source for broad component behavior coverage; selected application journeys provide consumer integration evidence.
