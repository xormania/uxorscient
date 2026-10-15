# GitHub workflow

## Branches

| Branch | Purpose | Pull request target |
| --- | --- | --- |
| Feature or fix branch from `dev` | One reviewable change | `dev` |
| `dev` | Integrated development | `master` when promoting completed work |
| `master` | Default branch and promoted code | Never an ordinary work branch |
| Sync branch from `dev` with `master` merged into it | Bring the promotion or urgent fix back into development | `dev` |

GitHub offers `master` by default when opening a PR. Choose `dev` explicitly for
ordinary work. Use merge commits throughout; preserve review commits and shared
history. Do not force-push `dev` or `master`, squash a promotion, or delete either
long-lived branch. An urgent fix may target `master` only when the maintainer
authorizes it, and must return to `dev` through a sync PR.

A single change uses one work branch and PR. If a task needs several dependent
parts, agree its integration branch and merge order with the maintainer; do not
import another project's work-order automation or branch names by assumption.

## Ownership and reviews

[CODEOWNERS](../.github/CODEOWNERS) assigns the entire repository to its maintainer,
with explicit entries for workflow, agent, contribution, security and release
controls. GitHub reads that file from the PR's base branch. Ownership becomes an
enforced review requirement only where the applicable ruleset requires it.

Use the PR template and plain `type(scope): what changes` titles. After CI is green,
request one Codex code review and one Codex security review. Address actionable
findings, rerun affected checks and resolve their threads; do not request repeated
reviews unless the owner changes the instruction. Automated reviews do not stand
in for GitHub's required code-owner approval.

Never approve your own change or bypass the rules. If GitHub cannot accept an
approval because the code owner also authored the PR, report that exact constraint
to the maintainer. Do not switch identities, change ownership or weaken protection
to make the merge pass. Current owner instructions determine whether an agent is
authorized to merge once every applicable gate is satisfied.

## Repository settings

These are the settings the maintainer should keep aligned with the workflow.
Versioned files do not create GitHub rulesets or enable reporting features.

| Setting | Intended configuration |
| --- | --- |
| Default branch | `master` |
| Allowed PR merge method | Merge commit |
| `dev` and `master` | Require PRs; prevent deletion and force pushes |
| Reviews | Require resolved conversations and the maintainer's configured ownership reviews |
| Required checks | Select the actual successful job/check names; enabling the option with an empty list selects no required checks |
| Code scanning | Require the configured CodeQL results; the workflow runs for every PR |
| Automatic branch deletion | May delete finished work branches; protect `dev` and `master` before using it for promotion PRs |
| Private vulnerability reporting | Enable before relying on the private advisory form; SECURITY.md includes a fallback request if it is unavailable |

The package/application, prepared-environment and consumer-workflow jobs supply
different evidence. CodeQL covers the Python tools, not PHP. The current workflows
run on PRs and on pushes to both integration and promotion branches. A later
change that makes a required workflow conditional must still provide a result
for every affected PR; a missing result must not leave unrelated work blocked.

Keep `dev` and `master` explicitly covered by their intended rules. A selector for
the default branch covers `master` while that remains default; it does not also
protect `dev`. Inspect GitHub's live settings before describing a protection as
active. Do not infer enforcement from this document or a green CI run.

## Promotions and synchronization

1. Finish the selected work through reviewed PRs into `dev`.
2. Open a `dev` to `master` PR using the same template. Link included PRs, state
   the outcome and record checks on the actual proposed revision.
3. Satisfy CI, code scanning, requested reviews, required ownership approval and
   resolved conversations, then merge with the owner's authorization.
4. Keep `dev`. Open a sync PR based on `dev` containing the merge of `master` back
   into it, and complete that PR through the same applicable gates.

Version tags, GitHub Releases and Packagist publication require a separate release
decision. [Release preparation](releasing.md) documents the existing evidence
checks; repository setup does not trigger publication.

## Community entry points

The README links [support](../SUPPORT.md), [security reporting](../SECURITY.md),
[contribution guidance](../CONTRIBUTING.md) and the
[code of conduct](../CODE_OF_CONDUCT.md). Issue forms live in
`.github/ISSUE_TEMPLATE`; blank issues remain available for questions,
documentation corrections and requests to arrange private contact without details.
Templates must be on the default branch to appear in GitHub's interface.

Use the security policy's private route for vulnerability details. Conduct reports
follow the code of conduct. Do not invent a private email address, publish private
project references, or promise a response deadline the maintainer has not adopted.

This workflow adapts UXor's development/promotion split, merge commits, PR evidence,
human ownership and private reporting conventions to the companion. Its package
release mechanism and CI scope remain UXorscient's own.
