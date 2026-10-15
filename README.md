# UXorscient

Agent guidance and development tools for building with [UXor](https://github.com/xormania/uxor).

UXorscient is a Composer development companion for Symfony applications. It brings
UXor references, task guidance and project diagnostics into an agent's workflow.
The application owns its installed UXor source and business logic.

## Install in a Symfony application

Until a Packagist release is published, configure the source repository and select
the promoted `master` branch:

```sh
composer config repositories.uxorscient vcs https://github.com/xormania/uxorscient
composer require --dev xormania/uxorscient:dev-master
```

`master` is the default and promotion branch. Ongoing work integrates on `dev`;
select `dev-dev` explicitly only when testing that development work. Both branch
versions have Composer's development stability. Package publication remains a
separate release action.

Run commands in the application's actual PHP environment. For a new Mate setup:

```sh
vendor/bin/mate init
composer dump-autoload
vendor/bin/mate discover
vendor/bin/mate tools:list --format=json
```

After installing or updating the companion in an initialized Mate project,
refresh its instructions and skills explicitly:

```sh
composer update xormania/uxorscient
vendor/bin/mate discover
```

This sequence also works when Mate's Composer plugin does not refresh discovery.
With Mate 0.14 and Composer 2.10.3 running from a PHAR, the plugin resolved Composer's
own root instead of the consuming application. Explicit discovery uses the actual
application and preserves project-authored instructions and configuration.

UXorscient supplies three skills (setup, build, verify), references for 64 UXor
components and seven tools for discovery, project inspection, first-setup checks
and practical workflow guidance.
Search first, then load the relevant component detail and documentation:

```sh
vendor/bin/uxorscient catalog --query=dialog --format=json
vendor/bin/uxorscient component modal --format=json
vendor/bin/mate resources:read uxorscient://reference/modal/README.md --format=json
vendor/bin/uxorscient workflow customer-management --format=json
vendor/bin/mate tools:call uxorscient_workflow --name=customer-management --format=json
vendor/bin/uxorscient inspect --format=json
```

Use native Toolkit installation and the selected component's integration guide to
complete setup. Metadata inspection does not establish runtime behavior. See
[operations](OPERATIONS.md) for result limits, unknowns, exit statuses and
installed Maker/Mate discovery.

The customer-management workflow connects a searchable list, modal form,
validation, successful-save feedback and Turbo history. It is companion-authored
guidance alongside the pinned upstream component references.

The bundled reference identifies UXor revision
40d957cd1ea7766ac0dee742816948ce5ae05bc3. Its documentation is generated from UXor;
[reference maintenance](https://github.com/xormania/uxorscient/blob/master/docs/reference-maintenance.md) explains updates. Composer updates
the companion's code and references; Mate discovery refreshes the installed agent
guidance and skills. Installed application components remain owned by the consuming
project.

## Development

The repository includes an independent consuming Symfony application. Follow
[development setup](https://github.com/xormania/uxorscient/blob/master/docs/development.md) for native PHP or
Docker, Mate, source inspection with Serena and application checks.

The package requires PHP 8.4 or newer. Actual development dependencies are recorded
in the Composer locks. [Implementation status](https://github.com/xormania/uxorscient/blob/master/docs/implementation.md) tracks the
companion capabilities and their validation.

## Contributing

Read [CONTRIBUTING.md](https://github.com/xormania/uxorscient/blob/master/CONTRIBUTING.md). Changes go through focused pull requests,
green checks and the owner's requested reviews before merging. Start work from
`dev` and target `dev` explicitly; completed work is promoted to the default
`master` branch in a separate PR. The
[GitHub workflow](https://github.com/xormania/uxorscient/blob/master/docs/github.md)
describes ownership, branch settings and promotions.

For questions and bugs, read
[SUPPORT.md](https://github.com/xormania/uxorscient/blob/master/SUPPORT.md).
Report vulnerabilities using
[SECURITY.md](https://github.com/xormania/uxorscient/blob/master/SECURITY.md), and
follow the [code of conduct](https://github.com/xormania/uxorscient/blob/master/CODE_OF_CONDUCT.md)
when participating.

MIT licensed. Maintained by xormania.
