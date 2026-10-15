# Security policy

## Supported versions

UXorscient has not published a versioned release. Reports affecting the current
`master` or `dev` branches are accepted; include the exact commit or Composer
lock reference. Development branches do not promise a stable API. This table is
updated when a release and its support policy are selected.

| Reference | Report handling |
| --- | --- |
| Current `master` | Maintained, promoted code |
| Current `dev` | Maintained development work |
| Older commits or private modifications | Include the base revision and whether the issue reproduces on a maintained branch |

## Reporting a vulnerability

Use GitHub's private reporting route: **Security** > **Report a vulnerability**
at <https://github.com/xormania/uxorscient/security/advisories/new>.
Do not disclose vulnerability details in a public issue or pull request.

If GitHub does not offer private reporting, open a public issue asking the
maintainer to enable it or arrange private contact. Include no exploit details,
affected private project information, credentials or sensitive logs in that
request. Wait for the private channel before sending the report.

Include the companion version or commit, PHP/Symfony/Mate versions, relevant UXor
revision, native or Docker environment, minimal reproduction, expected and actual
behavior, and impact. Use synthetic data and remove credentials from examples.
State whether invoking project PHP was explicitly trusted and which tool or
command was involved when that matters to the report.

## Scope and trust boundaries

The distributed companion contains its PHP services, CLI/Mate adapters, references,
instructions and skills. The development application, environment runners,
packaging tools and workflows are repository tooling; report issues in those
surfaces here as well and identify the affected surface.

Project inspection distinguishes static observations from operations that execute
the selected application's PHP. Native metadata discovery requires explicit
project-code trust; fixed command arguments are not a sandbox. See
[operation boundaries](OPERATIONS.md) and
[development isolation](docs/development.md).

Installed UXor component source and application business logic belong to the
consuming project. A companion update does not patch those files. For an issue
in UXor itself, follow [UXor's security policy](https://github.com/xormania/uxor/security/policy).
If the source is uncertain, describe that uncertainty in the private report.

No fixed response or resolution deadline is promised. The maintainer coordinates
reproduction, fixes and disclosure through the private reporting channel.
