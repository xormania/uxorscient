---
name: verify
description: Verify a UXor application interaction through its real Symfony runtime, including Turbo history and updates, validation, accessibility and interrupted-work recovery where relevant.
---

# Verify a UXor interaction

Use this skill after setup, a feature change, a component update or an integration failure.

## Load the applicable contract

Read the selected component's `uxorscient://reference/<recipe>/README.md` and the relevant sections of `uxorscient://reference/docs/GUIDE.md`. For existing reusable testing mechanisms, consult `uxorscient://reference/docs/TESTING.md` on demand. Its demo-specific routes, helpers and test counts are reference material to adapt to this application.

Read resources with the project's `vendor/bin/mate resources:read <uri> --format=json`. The local fallback is the application's Composer vendor directory at `xormania/uxorscient/resources/uxor/docs/`. `resources/uxor/index.json` identifies the reference revision. Inspect installed/customized files when their behavior differs.

The testing guide is large. Inspect and use the installed `uxorscient_reference` tool to read bounded relevant sections instead of loading the entire guide by default.

For the complete list/edit/save journey, read `uxorscient://workflow/customer-management` or the bounded `uxorscient_workflow` tool. Its verification steps connect server validation, frame/stream completion, feedback, focus, history and runtime dependencies. The same guide ships at `xormania/uxorscient/resources/workflows/customer-management.md` under the application's Composer vendor directory.

## Procedure

1. Identify the intended application root, PHP invocation and served URL. Establish which interaction changed and its expected behavior. Inspect available project checks and choose those that exercise this change. Record checks that cannot run and their concrete cause.
2. Check application wiring: required packages are in the correct dependency set, Twig/PHP services load, assets/controllers resolve, relevant CSS is imported and the application answers a real request. Existing Mate diagnostics can help; inspect their inputs and artifact freshness before interpreting their results.
3. Exercise the full changed journey in the browser. Cover applicable validation errors, successful submission, refreshed content, visible feedback, keyboard/focus behavior and intended Back/Forward state. Exercise the Turbo/Live transitions this page actually uses, including return visits and repeated mounting where relevant.
4. Wait for evidence specific to the transition. A Drive visit, a frame navigation, a stream response and a Live update have different completion signals. Use known project helpers or observable final state. Do not make every update wait for `turbo:load`, use arbitrary delays as completion evidence or treat a running container as application readiness.
5. Capture console errors, failed requests and CSP violations during the journey. A screenshot alone does not establish working behavior. If a test or REPL operation failed partway through, inspect the resulting application state and diff before rerunning a mutation.
6. Inspect the final diff and report actual results. Distinguish an operation executing successfully from its findings passing. Preserve bounded failure output or retained result locations so the next agent can continue.

## Choose evidence proportionate to the change

Reuse the application's existing tests and shared setup. A portable consumer check should address application integration; UXor's full component suite remains maintained by UXor. For an initial install or runtime-dependency change, verify the application can boot and render the selected components with development dependencies omitted in an isolated install.

For a complete feature, report the user journey tested, source/package revisions, environment, checks and results, any human intervention, and unresolved behavior. Do not infer full compatibility from one successful path or report skipped checks as passing.
