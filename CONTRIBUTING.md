# Contributing

Develop in a feature branch and open a focused PR to master. Use installed Symfony
capabilities, attributes, autowiring and autoconfiguration where they fit. Reuse
component contracts from UXor and keep generated references reproducible.

Run the checks relevant to the change locally. The development guide provides
the same application commands used by CI. State actual results and remaining
gaps in the PR; a definition or container startup alone is not application proof.
Keep tests tied to observable behavior and share setup, execution and cleanup.

Use the PR template's What, Why, Coverage map and Checks fields. A title has the
form `type(scope): what changes` and at most 72 characters. Write descriptions for
a reviewer unfamiliar with the conversation. Explain the resulting behavior,
reused support and material limitations. Attribute work to xormania only.

Before writing GitHub metadata, pass the exact text to:

```sh
node tools/check-github-mentions.mjs --allow-file .github/mention-allowlist < body.md
```

The empty allowlist prevents accidental account/team references. An owner-requested
bot command can use the checker's explicit allow option for that one write.

Keep application runtime dependencies outside development-only tooling. Test the
exported package in an independent consumer when packaging or installation changes.
Do not commit vendors, caches, generated application assets or browser reports.
