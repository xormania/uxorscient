"""Exercise ownership, isolation and provider-check ordering without Docker."""
import importlib.util
import contextlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

SPEC = importlib.util.spec_from_file_location("uxorscient_development", Path(__file__).parents[1] / "run.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class DevelopmentRunnerTest(unittest.TestCase):
    def test_worktrees_have_separate_stack_names_and_default_ports(self):
        first = runner.workspace_identity(Path("/work/one"))
        second = runner.workspace_identity(Path("/work/two"))
        self.assertNotEqual(first, second)
        self.assertEqual(first, runner.workspace_identity(Path("/work/one")))
        self.assertTrue(20000 <= first[1] < 30000)

    def test_native_php_and_composer_overrides_keep_arguments_literal(self):
        with patch.dict(runner.os.environ, {"PHP_BIN": "/tools/php", "COMPOSER_BIN": "/tools/composer.phar"}):
            self.assertEqual(["/tools/php", "/tools/composer.phar", "install"], runner.native_command(["composer", "install"]))
            self.assertEqual(["/tools/php", "bin/console", "name;echo secret"], runner.native_command(["bin/console", "name;echo secret"]))

    def test_an_explicit_port_is_bounded(self):
        with patch.dict(runner.os.environ, {"UXORSCIENT_HTTP_PORT": "1"}):
            with self.assertRaisesRegex(ValueError, "between"):
                runner.environment(True)

    def test_secret_is_private_and_repeated_prepare_preserves_it(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(runner, "APP", Path(temporary)):
            runner.ensure_secret()
            secret = (Path(temporary) / ".env.local").read_bytes()
            runner.ensure_secret()
            self.assertEqual(secret, (Path(temporary) / ".env.local").read_bytes())
            self.assertEqual(0o600, (Path(temporary) / ".env.local").stat().st_mode & 0o777)

    def test_support_precheck_happens_before_pull_and_observation_after(self):
        events = []
        module = Mock()
        module.runner_precheck.side_effect = lambda *args: events.append("policy") or {"prepared": True}
        module.runner_check.side_effect = lambda *args, **kwargs: events.append("observed")
        with patch.object(runner, "require_docker"), patch.object(runner, "xorder_source", return_value=Path("/provider")), \
                patch.object(runner, "support_module", return_value=module), \
                patch.object(runner, "current_support", side_effect=lambda module, env: contextlib.nullcontext(env)), \
                patch.object(runner, "run", side_effect=lambda *args, **kwargs: events.append("pull")):
            runner.prepare_image(runner.environment())
        self.assertEqual(["policy", "pull", "observed"], events)

    def test_failed_support_precheck_never_pulls(self):
        module = Mock()
        module.runner_precheck.side_effect = ValueError("expired")
        with patch.object(runner, "require_docker"), patch.object(runner, "xorder_source", return_value=Path("/provider")), \
                patch.object(runner, "support_module", return_value=module), \
                patch.object(runner, "current_support", side_effect=lambda module, env: contextlib.nullcontext(env)), \
                patch.object(runner, "run") as command:
            with self.assertRaisesRegex(ValueError, "expired"):
                runner.prepare_image(runner.environment())
            command.assert_not_called()

    def test_completed_support_receipt_is_private_and_scoped_to_one_check(self):
        module = Mock(DEFAULT_POLICY_URL="https://canonical.example/policy")
        module.fetch_cli.side_effect = lambda args: args.output.write_text('{"policy": {}, "receipt": {}}')
        with tempfile.TemporaryDirectory() as temporary, patch.object(runner, "ROOT", Path(temporary)):
            with runner.current_support(module, {}) as env:
                snapshot = Path(env["XORDER_SUPPORT_POLICY_FILE"])
                self.assertTrue(snapshot.is_file())
                self.assertEqual(0o600, snapshot.stat().st_mode & 0o777)
                self.assertEqual(0o700, snapshot.parent.stat().st_mode & 0o777)
                module.fetch_cli.assert_called_once()
            self.assertFalse(snapshot.exists())

    def test_explicit_offline_receipt_is_checked_without_refresh_or_removal(self):
        module = Mock()
        env = {"XORDER_SUPPORT_POLICY_FILE": "/owned/policy.json"}
        with runner.current_support(module, env) as selected:
            self.assertEqual(env, selected)
        module.fetch_cli.assert_not_called()

    def test_native_prepare_never_uses_docker_and_preserves_local_ownership(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(runner, "APP", Path(temporary)), \
                patch.object(runner, "prepare_image") as image, patch.object(runner, "execute") as execute:
            runner.prepare(runner.environment(True), True, assets=False)
            image.assert_not_called()
            self.assertTrue((Path(temporary) / ".env.local").is_file())
            self.assertTrue(all(call.args[2] is True for call in execute.call_args_list))
            self.assertFalse(any("importmap:install" in call.args[0] for call in execute.call_args_list))

    def test_wrong_application_response_fails_readiness(self):
        response = Mock()
        response.status = 200
        response.read.return_value = b"an unrelated server"
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        opener = Mock()
        opener.open.return_value = response
        with patch.object(runner.urllib.request, "build_opener", return_value=opener):
            with self.assertRaisesRegex(ValueError, "not valid"):
                runner.readiness({"UXORSCIENT_HTTP_PORT": "21080"})


if __name__ == "__main__":
    unittest.main()
