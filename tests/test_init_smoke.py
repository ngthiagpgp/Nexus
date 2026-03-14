from __future__ import annotations

import datetime
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import duckdb


REPO_ROOT = Path(__file__).resolve().parents[1]


class NexusCliSmokeTest(unittest.TestCase):
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

    def test_entity_create_persists_to_database_and_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "entity",
                "create",
                "--name",
                "Projeto X",
                "--type",
                "project",
                "--context",
                "Pesquisa em economia",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 0, create_run.stdout + create_run.stderr)
            self.assertIn("Entity created:", create_run.stdout)

            database_path = workspace_root / "nexus.duckdb"
            connection = duckdb.connect(str(database_path))
            try:
                entity_row = connection.execute(
                    "SELECT name, type, context FROM entities WHERE name = 'Projeto X'"
                ).fetchone()
                self.assertEqual(entity_row, ("Projeto X", "project", "Pesquisa em economia"))

                audit_row = connection.execute(
                    """
                    SELECT action, entity_type, agent
                    FROM audit_log
                    WHERE entity_type = 'entity'
                    ORDER BY timestamp DESC
                    LIMIT 1
                    """
                ).fetchone()
                self.assertEqual(audit_row, ("create", "entity", "user"))
            finally:
                connection.close()

    def test_entity_list_shows_created_entities_and_type_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "entity", "create", "--name", "Projeto X", "--type", "project", cwd=workspace_root
            )
            self.run_cli(
                "entity", "create", "--name", "Alice", "--type", "person", cwd=workspace_root
            )

            list_run = self.run_cli("entity", "list", cwd=workspace_root)
            self.assertEqual(list_run.returncode, 0, list_run.stdout + list_run.stderr)
            self.assertIn("ID | Name | Type | Context", list_run.stdout)
            self.assertIn("Projeto X | project", list_run.stdout)
            self.assertIn("Alice | person", list_run.stdout)

            filtered_run = self.run_cli("entity", "list", "--type", "project", cwd=workspace_root)
            self.assertEqual(filtered_run.returncode, 0, filtered_run.stdout + filtered_run.stderr)
            self.assertIn("Projeto X | project", filtered_run.stdout)
            self.assertNotIn("Alice | person", filtered_run.stdout)

    def test_entity_commands_fail_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            outside_root = Path(temp_dir) / "outside"
            outside_root.mkdir(parents=True, exist_ok=True)

            create_run = self.run_cli(
                "entity", "create", "--name", "Projeto X", "--type", "project", cwd=outside_root
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", create_run.stderr)

            list_run = self.run_cli("entity", "list", cwd=outside_root)
            self.assertEqual(list_run.returncode, 1, list_run.stdout + list_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", list_run.stderr)

    def test_entity_create_rejects_blank_required_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "entity",
                "create",
                "--name",
                "   ",
                "--type",
                "project",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Entity name is required and cannot be blank.", create_run.stderr)

    def test_document_create_writes_markdown_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "document",
                "create",
                "--type",
                "daily",
                "--title",
                "Daily 2026-03-13",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 0, create_run.stdout + create_run.stderr)
            self.assertIn("Document created:", create_run.stdout)
            self.assertIn("Path: documents/daily/2026-03-13.md", create_run.stdout)

            document_path = workspace_root / "documents" / "daily" / "2026-03-13.md"
            self.assertTrue(document_path.exists())
            self.assertEqual(document_path.read_text(encoding="utf-8"), "# Daily 2026-03-13\n\n")

            connection = duckdb.connect(str(workspace_root / "nexus.duckdb"))
            try:
                row = connection.execute(
                    """
                    SELECT title, type, status, path
                    FROM documents
                    WHERE title = 'Daily 2026-03-13'
                    """
                ).fetchone()
                self.assertEqual(
                    row,
                    ("Daily 2026-03-13", "daily", "draft", "documents/daily/2026-03-13.md"),
                )
            finally:
                connection.close()

    def test_document_list_shows_created_documents_and_filters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            self.run_cli(
                "document",
                "create",
                "--type",
                "daily",
                "--title",
                "Daily 2026-03-13",
                cwd=workspace_root,
            )
            self.run_cli(
                "document",
                "create",
                "--type",
                "note",
                "--title",
                "Research Notes",
                cwd=workspace_root,
            )

            list_run = self.run_cli("document", "list", cwd=workspace_root)
            self.assertEqual(list_run.returncode, 0, list_run.stdout + list_run.stderr)
            self.assertIn("ID | Title | Type | Status | Path", list_run.stdout)
            self.assertIn("Daily 2026-03-13 | daily | draft | documents/daily/2026-03-13.md", list_run.stdout)
            self.assertIn("Research Notes | note | draft | documents/note/research-notes.md", list_run.stdout)

            filtered_run = self.run_cli(
                "document", "list", "--type", "daily", cwd=workspace_root
            )
            self.assertEqual(filtered_run.returncode, 0, filtered_run.stdout + filtered_run.stderr)
            self.assertIn("Daily 2026-03-13 | daily | draft", filtered_run.stdout)
            self.assertNotIn("Research Notes | note | draft", filtered_run.stdout)

    def test_document_commands_fail_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            outside_root = Path(temp_dir) / "outside"
            outside_root.mkdir(parents=True, exist_ok=True)

            create_run = self.run_cli(
                "document", "create", "--type", "daily", cwd=outside_root
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", create_run.stderr)

            list_run = self.run_cli("document", "list", cwd=outside_root)
            self.assertEqual(list_run.returncode, 1, list_run.stdout + list_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", list_run.stderr)

    def test_document_create_rejects_blank_required_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "document",
                "create",
                "--type",
                "   ",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Document type is required and cannot be blank.", create_run.stderr)

    def test_relation_create_persists_to_database_and_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "entity",
                "create",
                "--name",
                "Projeto X",
                "--type",
                "project",
                cwd=workspace_root,
            )
            self.run_cli(
                "entity",
                "create",
                "--name",
                "Projeto Y",
                "--type",
                "project",
                cwd=workspace_root,
            )

            create_run = self.run_cli(
                "relation",
                "create",
                "--from",
                "Projeto X",
                "--to",
                "Projeto Y",
                "--type",
                "depende_de",
                "--context",
                "Projeto Y depende de Projeto X",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 0, create_run.stdout + create_run.stderr)
            self.assertIn("Relation created:", create_run.stdout)

            connection = duckdb.connect(str(workspace_root / "nexus.duckdb"))
            try:
                relation_row = connection.execute(
                    """
                    SELECT relation_type, weight, context
                    FROM relations
                    WHERE relation_type = 'depende_de'
                    """
                ).fetchone()
                self.assertEqual(
                    relation_row,
                    ("depende_de", 0.5, "Projeto Y depende de Projeto X"),
                )

                audit_row = connection.execute(
                    """
                    SELECT action, entity_type, agent
                    FROM audit_log
                    WHERE entity_type = 'relation'
                    ORDER BY timestamp DESC
                    LIMIT 1
                    """
                ).fetchone()
                self.assertEqual(audit_row, ("create", "relation", "user"))
            finally:
                connection.close()

    def test_relation_list_shows_created_relations_and_filters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "entity",
                "create",
                "--name",
                "Projeto X",
                "--type",
                "project",
                cwd=workspace_root,
            )
            self.run_cli(
                "entity",
                "create",
                "--name",
                "Projeto Y",
                "--type",
                "project",
                cwd=workspace_root,
            )
            self.run_cli(
                "entity",
                "create",
                "--name",
                "Alice",
                "--type",
                "person",
                cwd=workspace_root,
            )
            self.run_cli(
                "relation",
                "create",
                "--from",
                "Projeto X",
                "--to",
                "Projeto Y",
                "--type",
                "depende_de",
                cwd=workspace_root,
            )
            self.run_cli(
                "relation",
                "create",
                "--from",
                "Alice",
                "--to",
                "Projeto X",
                "--type",
                "trabalha_em",
                cwd=workspace_root,
            )

            list_run = self.run_cli("relation", "list", cwd=workspace_root)
            self.assertEqual(list_run.returncode, 0, list_run.stdout + list_run.stderr)
            self.assertIn("ID | From | To | Type | Weight | Context", list_run.stdout)
            self.assertIn("Projeto X | Projeto Y | depende_de | 0.5 | -", list_run.stdout)
            self.assertIn("Alice | Projeto X | trabalha_em | 0.5 | -", list_run.stdout)

            filtered_run = self.run_cli(
                "relation",
                "list",
                "--from",
                "Projeto X",
                cwd=workspace_root,
            )
            self.assertEqual(filtered_run.returncode, 0, filtered_run.stdout + filtered_run.stderr)
            self.assertIn("Projeto X | Projeto Y | depende_de", filtered_run.stdout)
            self.assertNotIn("Alice | Projeto X | trabalha_em", filtered_run.stdout)

    def test_relation_commands_fail_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            outside_root = Path(temp_dir) / "outside"
            outside_root.mkdir(parents=True, exist_ok=True)

            create_run = self.run_cli(
                "relation",
                "create",
                "--from",
                "Projeto X",
                "--to",
                "Projeto Y",
                "--type",
                "depende_de",
                cwd=outside_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", create_run.stderr)

            list_run = self.run_cli("relation", "list", cwd=outside_root)
            self.assertEqual(list_run.returncode, 1, list_run.stdout + list_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", list_run.stderr)

    def test_relation_create_rejects_missing_entities(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "entity",
                "create",
                "--name",
                "Projeto X",
                "--type",
                "project",
                cwd=workspace_root,
            )

            create_run = self.run_cli(
                "relation",
                "create",
                "--from",
                "Projeto X",
                "--to",
                "Projeto Y",
                "--type",
                "depende_de",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Entity not found: Projeto Y", create_run.stderr)

    def test_relation_create_rejects_blank_required_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "relation",
                "create",
                "--from",
                "   ",
                "--to",
                "Projeto Y",
                "--type",
                "depende_de",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("From entity is required and cannot be blank.", create_run.stderr)

    def test_activity_create_persists_to_database_and_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "cycle",
                "create",
                "--type",
                "daily",
                "--start",
                "2026-03-13",
                cwd=workspace_root,
            )

            create_run = self.run_cli(
                "activity",
                "create",
                "--title",
                "Finish report",
                "--cycle-id",
                "cycle-daily-2026-03-13",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 0, create_run.stdout + create_run.stderr)
            self.assertIn("Activity created:", create_run.stdout)

            connection = duckdb.connect(str(workspace_root / "nexus.duckdb"))
            try:
                activity_row = connection.execute(
                    """
                    SELECT title, cycle_id, status, priority
                    FROM activities
                    WHERE title = 'Finish report'
                    """
                ).fetchone()
                self.assertEqual(
                    activity_row,
                    ("Finish report", "cycle-daily-2026-03-13", "pending", 3),
                )

                audit_row = connection.execute(
                    """
                    SELECT action, entity_type, agent
                    FROM audit_log
                    WHERE entity_type = 'activity'
                    ORDER BY timestamp DESC
                    LIMIT 1
                    """
                ).fetchone()
                self.assertEqual(audit_row, ("create", "activity", "user"))
            finally:
                connection.close()

    def test_activity_list_shows_created_activities_and_filters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "cycle",
                "create",
                "--type",
                "daily",
                "--start",
                "2026-03-13",
                cwd=workspace_root,
            )
            self.run_cli(
                "cycle",
                "create",
                "--type",
                "weekly",
                "--start",
                "2026-03-10",
                cwd=workspace_root,
            )

            self.run_cli(
                "activity",
                "create",
                "--title",
                "Finish report",
                "--cycle-id",
                "cycle-daily-2026-03-13",
                cwd=workspace_root,
            )
            self.run_cli(
                "activity",
                "create",
                "--title",
                "Plan next week",
                "--cycle-id",
                "cycle-weekly-2026-03-10",
                cwd=workspace_root,
            )

            list_run = self.run_cli("activity", "list", cwd=workspace_root)
            self.assertEqual(list_run.returncode, 0, list_run.stdout + list_run.stderr)
            self.assertIn("ID | Title | Cycle | Status | Priority", list_run.stdout)
            self.assertIn("Finish report | cycle-daily-2026-03-13 | pending | 3", list_run.stdout)
            self.assertIn("Plan next week | cycle-weekly-2026-03-10 | pending | 3", list_run.stdout)

            filtered_run = self.run_cli(
                "activity",
                "list",
                "--cycle-id",
                "cycle-daily-2026-03-13",
                cwd=workspace_root,
            )
            self.assertEqual(filtered_run.returncode, 0, filtered_run.stdout + filtered_run.stderr)
            self.assertIn("Finish report | cycle-daily-2026-03-13 | pending | 3", filtered_run.stdout)
            self.assertNotIn("Plan next week | cycle-weekly-2026-03-10 | pending | 3", filtered_run.stdout)

    def test_activity_commands_fail_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            outside_root = Path(temp_dir) / "outside"
            outside_root.mkdir(parents=True, exist_ok=True)

            create_run = self.run_cli(
                "activity",
                "create",
                "--title",
                "Finish report",
                "--cycle-id",
                "cycle-daily-2026-03-13",
                cwd=outside_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", create_run.stderr)

            list_run = self.run_cli("activity", "list", cwd=outside_root)
            self.assertEqual(list_run.returncode, 1, list_run.stdout + list_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", list_run.stderr)

    def test_activity_create_rejects_blank_required_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "cycle",
                "create",
                "--type",
                "daily",
                "--start",
                "2026-03-13",
                cwd=workspace_root,
            )

            create_run = self.run_cli(
                "activity",
                "create",
                "--title",
                "   ",
                "--cycle-id",
                "cycle-daily-2026-03-13",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Activity title is required and cannot be blank.", create_run.stderr)

    def test_activity_create_rejects_missing_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "activity",
                "create",
                "--title",
                "Finish report",
                "--cycle-id",
                "cycle-daily-2026-03-13",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Cycle not found: cycle-daily-2026-03-13", create_run.stderr)

    def test_cycle_create_persists_to_database_and_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "cycle",
                "create",
                "--type",
                "daily",
                "--start",
                "2026-03-13",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 0, create_run.stdout + create_run.stderr)
            self.assertIn("Cycle created: cycle-daily-2026-03-13", create_run.stdout)

            connection = duckdb.connect(str(workspace_root / "nexus.duckdb"))
            try:
                cycle_row = connection.execute(
                    """
                    SELECT id, type, start_date, status
                    FROM cycles
                    WHERE id = 'cycle-daily-2026-03-13'
                    """
                ).fetchone()
                self.assertEqual(
                    cycle_row,
                    ("cycle-daily-2026-03-13", "daily", datetime.datetime(2026, 3, 13, 0, 0), "active"),
                )

                audit_row = connection.execute(
                    """
                    SELECT action, entity_type, agent
                    FROM audit_log
                    WHERE entity_type = 'cycle'
                    ORDER BY timestamp DESC
                    LIMIT 1
                    """
                ).fetchone()
                self.assertEqual(audit_row, ("create", "cycle", "user"))
            finally:
                connection.close()

    def test_cycle_list_shows_created_cycles_and_filters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))
            self.run_cli(
                "cycle",
                "create",
                "--type",
                "daily",
                "--start",
                "2026-03-13",
                cwd=workspace_root,
            )
            self.run_cli(
                "cycle",
                "create",
                "--type",
                "weekly",
                "--start",
                "2026-03-10",
                cwd=workspace_root,
            )

            list_run = self.run_cli("cycle", "list", cwd=workspace_root)
            self.assertEqual(list_run.returncode, 0, list_run.stdout + list_run.stderr)
            self.assertIn("ID | Type | Start | Status", list_run.stdout)
            self.assertIn("cycle-daily-2026-03-13 | daily | 2026-03-13 00:00:00 | active", list_run.stdout)
            self.assertIn("cycle-weekly-2026-03-10 | weekly | 2026-03-10 00:00:00 | active", list_run.stdout)

            filtered_run = self.run_cli("cycle", "list", "--type", "daily", cwd=workspace_root)
            self.assertEqual(filtered_run.returncode, 0, filtered_run.stdout + filtered_run.stderr)
            self.assertIn("cycle-daily-2026-03-13 | daily | 2026-03-13 00:00:00 | active", filtered_run.stdout)
            self.assertNotIn("cycle-weekly-2026-03-10 | weekly | 2026-03-10 00:00:00 | active", filtered_run.stdout)

    def test_cycle_commands_fail_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            outside_root = Path(temp_dir) / "outside"
            outside_root.mkdir(parents=True, exist_ok=True)

            create_run = self.run_cli(
                "cycle",
                "create",
                "--type",
                "daily",
                "--start",
                "2026-03-13",
                cwd=outside_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", create_run.stderr)

            list_run = self.run_cli("cycle", "list", cwd=outside_root)
            self.assertEqual(list_run.returncode, 1, list_run.stdout + list_run.stderr)
            self.assertIn("Current directory is not a Nexus workspace", list_run.stderr)

    def test_cycle_create_rejects_blank_required_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "cycle",
                "create",
                "--type",
                "   ",
                "--start",
                "2026-03-13",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Cycle type is required and cannot be blank.", create_run.stderr)

    def test_cycle_create_rejects_invalid_start(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            self.run_cli("init", str(workspace_root))

            create_run = self.run_cli(
                "cycle",
                "create",
                "--type",
                "daily",
                "--start",
                "13/03/2026",
                cwd=workspace_root,
            )
            self.assertEqual(create_run.returncode, 1, create_run.stdout + create_run.stderr)
            self.assertIn("Cycle start must be an ISO date or datetime: 13/03/2026", create_run.stderr)

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
