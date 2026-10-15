# Preparing a release

Use a clean reviewed checkout and the application's actual PHP environment. These
steps prepare evidence for a maintainer-selected release; version tags and registry
publication are separate maintainer actions.

## Promotion branches

`master` remains the default branch. Develop and review ordinary changes through
PRs into `dev`; prepare a promotion PR from `dev` to `master` when its selected
work is ready. Follow the existing PR template, link the included changes, record
the tested commit and satisfy the required reviews and GitHub rules. Merge with a
merge commit, preserving the history already reviewed on `dev`.

After promotion, use a sync branch based on `dev` to merge `master`, then merge
that sync PR into `dev`. This brings the promotion commit back without resetting
either shared branch. Keep both long-lived branches; only finished work branches
are candidates for deletion. See [GitHub workflow](github.md).

Promoting documentation or tooling does not publish a package. Only select a
version, tag the promoted commit and publish when the maintainer authorizes that
release. Never move a published version tag to different code; publish a new
version for a correction. The exact first version and registry setup remain
release decisions, not side effects of repository setup.

## Reference and package

Choose the UXor source revision deliberately. In a clean checkout of that revision,
regenerate and verify the bundle using the commands in
[reference maintenance](reference-maintenance.md). For the current snapshot:

```sh
php tools/generate-reference.php --source=/path/to/uxor --revision=40d957cd1ea7766ac0dee742816948ce5ae05bc3
php tools/generate-reference.php --source=/path/to/uxor --revision=40d957cd1ea7766ac0dee742816948ce5ae05bc3 --check
```

Review changed component contracts alongside the setup/build/verify skills and
companion-authored workflow guides. Generated source references and authored
application guidance have separate owners; refreshing knowledge does not update
application-owned components.

```sh
composer validate --strict
python3 dev/run.py --native prepare
composer validate --strict --working-dir=dev/app
vendor/bin/phpunit
python3 -m unittest discover -s dev/tests -p 'test_*.py'
python3 dev/run.py --native check
python3 tools/check-package.py --consumer
```

The last command verifies the actual Composer export, installs it without a source
symlink, exercises two archive versions, refreshes Mate explicitly, checks retained
consumer instructions and customized component code, and verifies a production
boot without development dependencies. A path-repository application alone does
not establish distribution behavior. Inspect retained failure directories before
removing them; [validation](testing.md) explains this check's boundaries.

## Installed components and application behavior

Use the disposable development fixture for the selected application journey:

```sh
python3 dev/install-uxor.py
npm ci
npx playwright install --with-deps chromium
npm run test:workflow
composer install --working-dir=dev/app --no-dev --prefer-dist --no-interaction --no-progress
php dev/app/bin/console cache:clear --env=prod --no-debug --no-interaction
php dev/check-workflow-runtime.php
```

This uses normal Toolkit source installation and verifies real browser behavior,
including server validation, streams, feedback, focus and Turbo history. Runtime
requirements remain ordinary application dependencies. Existing customized source
must be inspected rather than forced through the fixture installer. Restore the
fixture's development dependencies with `python3 dev/run.py --native prepare`
when continuing local work. See the [workflow guide](consumer-workflow.md) for
prepared Tailwind/browser executable options and the precise integration scope.

Where Serena support is included in the release evidence, run the prepared Docker
job or the same `dev/run.py up`, `dev/check-serena.py --companion`, and
`dev/run.py down` sequence. Retain the actual provider receipt. Scripted composition
and recovery checks establish interoperability; they do not establish fresh-agent
usability. The [access decision](composable-access.md) describes this distinction.

## Evidence and publication

Update [implementation status](implementation.md), the changelog and the tested
compatibility matrix from executed results. Record the package/source revisions,
PHP and Symfony/UX/Mate versions, asset profile, browser and provider identity,
commands, failures, remaining unknowns and links to CI evidence. Dependency
constraints alone do not demonstrate compatibility.

For a bounded fresh-agent task, record the task and starting revision, context and
infrastructure supplied, guidance/tools actually used, interventions, failed steps,
recovery, preserved application customizations and verified user-facing outcome.
[The email-sort evaluation](agent-evaluation.md) is one recorded example. Repeat a
comparable task when making a claim about improvement; one successful task does
not establish general agent effectiveness.

A maintainer then selects the release version, finalizes its changelog entry,
checks required CI and resolved reviews, and creates the corresponding version
tag and configured package publication. Verify the resulting distribution through
a clean consumer and refresh installation instructions when registry availability
changes. This repository's checks do not create a tag or publish a Packagist release.
