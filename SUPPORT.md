# Getting help

Start with the [README](README.md), [operation reference](OPERATIONS.md),
[development setup](docs/development.md) and
[implementation status](docs/implementation.md). The status page distinguishes
tested combinations from dependency constraints and records the current limits.

## Questions and bugs

Use [GitHub issues](https://github.com/xormania/uxorscient/issues) for public
questions, reproducible bugs and feature requests. Search existing issues first.
Use the bug or feature form when it fits; a blank issue is available for questions
and documentation corrections. GitHub Discussions is not the support channel.

For a bug, provide the installed companion version or exact commit, PHP/Symfony/
Mate versions, relevant UXor source revision, native or Docker environment,
minimal reproduction, and expected and actual results. Attach only the relevant
sanitized command output. Never include credentials, customer data, private
repository URLs or complete environment dumps.

Use a small public or synthetic example where possible. Distinguish what the
companion reported from the application's actual behavior. Inspection metadata
alone does not prove that a component works in the browser.

## Choosing the project

| Problem | Starting point |
| --- | --- |
| Companion installation, CLI/Mate operations, references, skills or project findings | This repository |
| UXor component behavior or its documented contract | [UXor](https://github.com/xormania/uxor/issues); identify installed customizations |
| Prepared image or environment-provider behavior | [xorder](https://github.com/xormania/xorder/issues); identify the resource and observed failure |
| Application business rules, persistence or private configuration | The consuming application's maintainer |

If the cause is unclear, start here with the observed facts; do not guess which
project must be responsible. The maintainer can help narrow the reproduction.

## Private concerns

Follow [SECURITY.md](SECURITY.md) for vulnerabilities and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for conduct concerns. A public request to
arrange private contact must contain no sensitive details. Support is provided as
maintainer availability permits; there is no support service-level agreement.
