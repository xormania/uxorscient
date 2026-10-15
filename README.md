# UXorscient

Agent guidance and development tools for building with [UXor](https://github.com/xormania/uxor).

UXorscient is a Composer development companion for Symfony applications. It brings
UXor references, task guidance and project diagnostics into an agent's workflow.
The application owns its installed UXor source and business logic.

## Install in a Symfony application

Until a Packagist release is published, configure the source repository and select
the development branch:

```sh
composer config repositories.uxorscient vcs https://github.com/xormania/uxorscient
composer require --dev xormania/uxorscient:dev-master
```

Run commands in the application's actual PHP environment. For a new Mate setup:

```sh
vendor/bin/mate init
composer dump-autoload
vendor/bin/mate discover
vendor/bin/mate tools:list --format=json
```

An initialized Mate project discovers the extension through its Composer plugin;
run discover explicitly when the plugin is disabled. Existing project instructions
and configuration remain project-owned. Follow Mate's supported setup when its
installed version needs an additional step.

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
[reference maintenance](https://github.com/xormania/uxorscient/blob/master/docs/reference-maintenance.md) explains updates. Updating
the companion refreshes guidance; installed application components remain owned by
the consuming project.

## Development

The repository includes an independent consuming Symfony application. Follow
[development setup](https://github.com/xormania/uxorscient/blob/master/docs/development.md) for native PHP or
Docker, Mate, source inspection with Serena and application checks.

The package requires PHP 8.4 or newer. Actual development dependencies are recorded
in the Composer locks. [Implementation status](https://github.com/xormania/uxorscient/blob/master/docs/implementation.md) tracks the
companion capabilities and their validation.

## Contributing

Read [CONTRIBUTING.md](https://github.com/xormania/uxorscient/blob/master/CONTRIBUTING.md). Changes go through focused pull requests,
green checks and the owner's requested reviews before merging.

MIT licensed. Maintained by xormania.
