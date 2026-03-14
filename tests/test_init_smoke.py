from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import duckdb


REPO_ROOT = Path(__file__).resolve().parents[1]


class NexusInitSmokeTest(unittest.TestCase):
    def test_nexus_init_bootstraps_workspace_and_is_safe_to_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"

            first_run = self.run_cli("init", str(workspace_root))
            self.assertEqual(first_run.returncode, 0, first_run.stdout + first_run.stderr)
            self.assertIn("Nexus workspace ready", first_run.stdout)
            self.assertIn("Schema note:", first_run.stdout)

            self.assertTrue((workspace_root / ".nexus" / "config.yaml").exists())
            self.assertTrue((workspace_root / ".nexus" / "backups").exists())
            self.assertTrue((workspace_root / "documents" / "daily").exists())
            self.assertTrue((workspace_root / "documents" / "weekly").exists())
            self.assertTrue((workspace_root / "documents" / "monthly").exists())

            database_path = workspace_root / "nexus.duckdb"
            self.assertTrue(database_path.exists())

            connection = duckdb.connect(str(database_path))
            try:
                tables = {row[0] for row in connection.execute("SHOW TABLES").fetchall()}
                self.assertIn("system_state", tables)
                self.assertIn("audit_log", tables)
                self.assertIn("documents", tables)

                schema_version = connection.execute(
                    "SELECT value FROM system_state WHERE key = 'schema_version'"
                ).fetchone()
                self.assertEqual(schema_version[0], "1.0")

                workspace_root_value = connection.execute(
                    "SELECT value FROM system_state WHERE key = 'workspace_root'"
                ).fetchone()
                self.assertEqual(workspace_root_value[0], str(workspace_root.resolve()))
            finally:
                connection.close()

            second_run = self.run_cli("init", str(workspace_root))
            self.assertEqual(
                second_run.returncode, 0, second_run.stdout + second_run.stderr
            )
            self.assertIn("Nexus workspace ready", second_run.stdout)
            self.assertIn("Schema note:", second_run.stdout)

    def test_nexus_status_reports_initialized_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"

            init_run = self.run_cli("init", str(workspace_root))
            self.assertEqual(init_run.returncode, 0, init_run.stdout + init_run.stderr)

            status_run = self.run_cli("status", cwd=workspace_root)
            self.assertEqual(status_run.returncode, 0, status_run.stdout + status_run.stderr)
            self.assertIn("Initialized: yes", status_run.stdout)
            self.assertIn("Schema version: 1.0", status_run.stdout)
            self.assertIn(
                f"Database: {workspace_root / 'nexus.duckdb'} (present)",
                status_run.stdout,
            )

    def test_nexus_status_reports_uninitialized_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            outside_root = Path(temp_dir) / "outside"
            outside_root.mkdir(parents=True, exist_ok=True)

            status_run = self.run_cli("status", cwd=outside_root)
            self.assertEqual(status_run.returncode, 0, status_run.stdout + status_run.stderr)
            self.assertIn("Initialized: no", status_run.stdout)
            self.assertIn("Missing paths:", status_run.stdout)
            self.assertIn(
                "Current directory does not satisfy the minimal Nexus workspace contract.",
                status_run.stdout,
            )

    def run_cli(
        self, *args: str, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        python_path_entries = [str(REPO_ROOT)]
        if env.get("PYTHONPATH"):
            python_path_entries.append(env["PYTHONPATH"])
        env["PYTHONPATH"] = os.pathsep.join(python_path_entries)
        return subprocess.run(
            [sys.executable, "-m", "nexus", *args],
            cwd=cwd or REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )


if __name__ == "__main__":
    unittest.main()
