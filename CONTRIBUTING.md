# Contributing

UXorscient is a Composer development companion for applications using UXor. Read
[the development guide](docs/development.md) for the native or prepared Docker
environment, and [validation](docs/testing.md) for the checks already available.

## Branches and ownership

`master` remains the default branch and holds promoted work. Start a feature or
fix branch from `dev` and target `dev` in its pull request. GitHub initially offers
the default branch as the target: select `dev` explicitly. Promote completed work
with a separate `dev` to `master` pull request. A promotion does not itself create
a version tag, GitHub Release or Packagist publication.

Use merge commits, as in UXor; do not squash or rebase shared branch history.
After promotion, merge `master` back through a sync branch and PR into `dev` so
both branches contain the promotion commit. Do not delete `dev` or `master`.
Work branches can be deleted once their work has merged.

The maintainer owns the repository through [.github/CODEOWNERS](.github/CODEOWNERS).
Required ownership reviews and branch rules are enforced by GitHub. Do not bypass
them or submit an approval of your own change. A maintainer-authorized urgent fix
may target `master`; bring it back into `dev` before continuing ordinary work.
See [GitHub workflow](docs/github.md) for branch settings and promotion checks.

## Changes and verification

Use installed Symfony capabilities, attributes, autowiring and autoconfiguration
where they fit. Reuse component contracts from UXor and keep generated references
reproducible. Keep the companion's services shared between CLI and Mate rather
than duplicating behavior in access adapters.

Run the checks relevant to the change locally. The development guide provides
the same application commands used by CI. State actual results and remaining
gaps in the PR; a definition or container startup alone is not application proof.
Keep tests tied to observable behavior and share setup, execution and cleanup.
Documentation and ownership changes do not need new behavior tests merely to
repeat their text. Workflow changes need syntax and trigger checks; installation
or packaging changes need the existing independent-consumer checks.

## Commits and pull requests

Use the PR template's What, Why, Coverage map and Checks fields. A title has the
form `type(scope): what changes` and at most 72 characters. Write descriptions for
a reviewer unfamiliar with the conversation. Explain the resulting behavior,
reused support and material limitations. Attribute work to xormania only.

Keep the title and description useful without prior chat context. For documentation
changes, the coverage map can state that no application behavior or test coverage
changed. For a promotion, link the included PRs, identify the commit checked and
record remaining gaps. Keep package publication separate unless the owner has
requested it.

After CI is green, request one Codex code review and one Codex security review for
the PR. Resolve actionable findings, rerun affected checks, and resolve the
corresponding threads. Do not request either review a second time unless the owner
explicitly changes that instruction. These reviews do not replace a required
GitHub code-owner approval. Merge only with the owner's authorization and all
applicable GitHub rules satisfied.

Before writing GitHub metadata, pass the exact text to:

```sh
node tools/check-github-mentions.mjs --allow-file .github/mention-allowlist < body.md
```

The empty allowlist prevents accidental account/team references. An owner-requested
bot command can use the checker's explicit allow option for that one write.
The owner entries in CODEOWNERS are repository configuration, not permission to
add account mentions to unrelated PR text. Keep private project names, links,
revisions and internal test references out of public contributions.

## Distribution and documentation

Keep application runtime dependencies outside development-only tooling. Test the
exported package in an independent consumer when packaging or installation changes.
Do not commit vendors, caches, generated application assets or browser reports.
Keep repository-only community files out of the Composer archive through
`.gitattributes`; retain the license and all runtime and agent resources.

Update the relevant documentation with the behavior it describes. User-visible
changes get an entry under `Unreleased` in [CHANGELOG.md](CHANGELOG.md). An earlier
evaluation remains a record of its original revision and runtime; do not rewrite
it to imply later work was tested there.

Use [SUPPORT.md](SUPPORT.md) for questions and reproducible bug reports,
[SECURITY.md](SECURITY.md) for private vulnerability reports, and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations. Release
preparation is documented in [docs/releasing.md](docs/releasing.md).
