from __future__ import annotations

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

            self.assertTrue((workspace_root / ".nexus" / "config.yaml").exists())
            self.assertTrue((workspace_root / ".nexus" / "backups").exists())
            self.assertTrue((workspace_root / "documents" / "daily").exists())
            self.assertTrue((workspace_root / "documents" / "weekly").exists())
            self.assertTrue((workspace_root / "documents" / "monthly").exists())

            database_path = workspace_root / "nexus.duckdb"
            self.assertTrue(database_path.exists())

            connection = duckdb.connect(str(database_path))
            try:
                tables = {
                    row[0]
                    for row in connection.execute("SHOW TABLES").fetchall()
                }
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
            self.assertEqual(second_run.returncode, 0, second_run.stdout + second_run.stderr)
            self.assertIn("Nexus workspace ready", second_run.stdout)

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "nexus", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
