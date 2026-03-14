from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import duckdb
from fastapi.testclient import TestClient

from nexus.api import create_app
from nexus.activities import create_activity
from nexus.cycles import create_cycle
from nexus.documents import create_document
from nexus.entities import create_entity
from nexus.relations import create_relation
from nexus.workspace import initialize_workspace


class NexusApiSmokeTest(unittest.TestCase):
    def test_cockpit_root_serves_html_shell(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            create_entity(
                workspace_root,
                name="Projeto X",
                entity_type="project",
                context="Pesquisa em economia",
            )
            create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/html", response.headers["content-type"])
            self.assertIn("Nexus Cockpit", response.text)
            self.assertIn("/api/system/status", response.text)
            self.assertIn('id="entities-list"', response.text)
            self.assertIn('id="documents-list"', response.text)
            self.assertIn('id="cycles-list"', response.text)
            self.assertIn('id="activities-list"', response.text)
            self.assertIn('id="cycle-detail"', response.text)
            self.assertIn('id="activity-detail"', response.text)
            self.assertIn('id="cycle-focus-banner"', response.text)
            self.assertIn('id="cycle-documents"', response.text)
            self.assertIn('id="activities-breakdown"', response.text)
            self.assertIn('id="activities-cycle-filter"', response.text)
            self.assertIn('id="documents-cycle-filter"', response.text)
            self.assertIn('id="activity-status-controls"', response.text)
            self.assertIn('id="document-status-controls"', response.text)
            self.assertIn('id="documents-status-filter"', response.text)
            self.assertIn('id="cycles-status-filter"', response.text)
            self.assertIn('id="activities-status-filter"', response.text)
            self.assertIn("/api/cycles", response.text)
            self.assertIn("/api/activities", response.text)
            self.assertIn("/api/documents", response.text)
            self.assertIn("/api/document-integrity", response.text)

    def test_health_and_status_in_initialized_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            client = TestClient(create_app(workspace_root=workspace_root))

            health = client.get("/api/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json()["status"], "ok")
            self.assertEqual(health.json()["data"]["service"], "nexus-api")

            status = client.get("/api/system/status")
            self.assertEqual(status.status_code, 200)
            payload = status.json()
            self.assertEqual(payload["status"], "ok")
            self.assertTrue(payload["data"]["is_workspace"])
            self.assertTrue(payload["data"]["db_present"])
            self.assertEqual(payload["data"]["counts"]["entities"], 0)
            self.assertEqual(payload["data"]["counts"]["documents"], 0)

    def test_status_reports_non_workspace_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "outside"
            workspace_root.mkdir(parents=True, exist_ok=True)
            client = TestClient(create_app(workspace_root=workspace_root))

            status = client.get("/api/system/status")
            self.assertEqual(status.status_code, 200)
            payload = status.json()
            self.assertEqual(payload["status"], "ok")
            self.assertFalse(payload["data"]["is_workspace"])
            self.assertFalse(payload["data"]["db_present"])
            self.assertIn(
                "Current directory does not satisfy the minimal Nexus workspace contract.",
                payload["data"]["notes"],
            )

    def test_entity_list_and_read_expose_existing_local_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            entity = create_entity(
                workspace_root,
                name="Projeto X",
                entity_type="project",
                context="Pesquisa em economia",
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            list_response = client.get("/api/entities", params={"type": "project"})
            self.assertEqual(list_response.status_code, 200)
            list_payload = list_response.json()
            self.assertEqual(list_payload["status"], "ok")
            self.assertEqual(len(list_payload["data"]), 1)
            self.assertEqual(list_payload["data"][0]["id"], entity.id)

            read_response = client.get(f"/api/entities/{entity.id}")
            self.assertEqual(read_response.status_code, 200)
            read_payload = read_response.json()
            self.assertEqual(read_payload["status"], "ok")
            self.assertEqual(read_payload["data"]["name"], "Projeto X")
            self.assertEqual(read_payload["data"]["type"], "project")

    def test_entity_read_returns_404_for_missing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get("/api/entities/missing-entity")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Entity not found: missing-entity", response.json()["message"])

    def test_document_list_and_read_surface_metadata_and_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            list_response = client.get("/api/documents", params={"type": "daily"})
            self.assertEqual(list_response.status_code, 200)
            list_payload = list_response.json()
            self.assertEqual(list_payload["status"], "ok")
            self.assertEqual(len(list_payload["data"]), 1)
            self.assertEqual(list_payload["data"][0]["id"], document.id)

            read_response = client.get(f"/api/documents/{document.id}")
            self.assertEqual(read_response.status_code, 200)
            read_payload = read_response.json()
            self.assertEqual(read_payload["status"], "ok")
            self.assertEqual(read_payload["data"]["title"], "Daily 2026-03-13")
            self.assertEqual(read_payload["data"]["path"], "documents/daily/2026-03-13.md")
            self.assertEqual(read_payload["data"]["content"], "# Daily 2026-03-13\n\n")
            self.assertIn("# Daily 2026-03-13", read_payload["data"]["content_preview"])

    def test_document_read_returns_409_when_backing_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            (workspace_root / document.path).unlink()
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get(f"/api/documents/{document.id}")
            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Document backing file is missing:", response.json()["message"])

    def test_document_integrity_list_and_read_report_ok_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            list_response = client.get("/api/document-integrity")
            self.assertEqual(list_response.status_code, 200)
            list_payload = list_response.json()
            self.assertEqual(list_payload["status"], "ok")
            self.assertEqual(len(list_payload["data"]), 1)
            self.assertEqual(list_payload["data"][0]["document_id"], document.id)
            self.assertEqual(list_payload["data"][0]["integrity_state"], "ok")

            read_response = client.get(f"/api/document-integrity/{document.id}")
            self.assertEqual(read_response.status_code, 200)
            read_payload = read_response.json()
            self.assertEqual(read_payload["status"], "ok")
            self.assertTrue(read_payload["data"]["backing_file_exists"])
            self.assertTrue(read_payload["data"]["path_matches_expected"])
            self.assertTrue(read_payload["data"]["content_hash_matches"])
            self.assertEqual(read_payload["data"]["issues"], [])

    def test_document_integrity_read_reports_missing_backing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            (workspace_root / document.path).unlink()
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get(f"/api/document-integrity/{document.id}")
            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["data"]["integrity_state"], "error")
            self.assertFalse(payload["data"]["backing_file_exists"])
            self.assertIsNone(payload["data"]["content_hash_matches"])
            self.assertIn("missing_backing_file", payload["data"]["issues"])

    def test_document_integrity_read_reports_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            (workspace_root / document.path).write_text(
                "# Daily 2026-03-13\n\nChanged\n",
                encoding="utf-8",
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get(f"/api/document-integrity/{document.id}")
            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["data"]["integrity_state"], "error")
            self.assertFalse(payload["data"]["content_hash_matches"])
            self.assertIn("content_hash_mismatch", payload["data"]["issues"])

    def test_document_integrity_read_returns_404_for_missing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get("/api/document-integrity/missing-document")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Document not found: missing-document", response.json()["message"])

    def test_document_status_update_endpoint_updates_record_and_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.patch(
                f"/api/documents/{document.id}",
                json={"status": "approved"},
            )
            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["data"]["id"], document.id)
            self.assertEqual(payload["data"]["status"], "approved")
            self.assertEqual(payload["data"]["version"], "2.0")
            self.assertIsNotNone(payload["data"]["approved_at"])

            connection = duckdb.connect(str(workspace_root / "nexus.duckdb"))
            try:
                document_row = connection.execute(
                    "SELECT status, version, approved_at FROM documents WHERE id = ?",
                    [document.id],
                ).fetchone()
                self.assertEqual(document_row[0], "approved")
                self.assertEqual(document_row[1], "2.0")
                self.assertIsNotNone(document_row[2])

                audit_row = connection.execute(
                    """
                    SELECT action, entity_type, agent, reason
                    FROM audit_log
                    WHERE entity_type = 'document' AND entity_id = ? AND action = 'update'
                    ORDER BY timestamp DESC, id DESC
                    LIMIT 1
                    """,
                    [document.id],
                ).fetchone()
                self.assertEqual(
                    audit_row,
                    ("update", "document", "user", "API document status update"),
                )
            finally:
                connection.close()

    def test_document_status_update_rejects_invalid_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-13",
                cycle_id=None,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            approve_response = client.patch(
                f"/api/documents/{document.id}",
                json={"status": "approved"},
            )
            self.assertEqual(approve_response.status_code, 200)
            archive_response = client.patch(
                f"/api/documents/{document.id}",
                json={"status": "archived"},
            )
            self.assertEqual(archive_response.status_code, 200)

            response = client.patch(
                f"/api/documents/{document.id}",
                json={"status": "approved"},
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn(
                "Invalid document status transition: archived -> approved.",
                response.json()["message"],
            )

    def test_document_status_update_returns_404_for_missing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.patch(
                "/api/documents/missing-document",
                json={"status": "approved"},
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Document not found: missing-document", response.json()["message"])

    def test_relation_list_exposes_existing_local_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            create_entity(workspace_root, name="Projeto X", entity_type="project", context=None)
            create_entity(workspace_root, name="Alice", entity_type="person", context=None)
            relation = create_relation(
                workspace_root,
                from_entity="Projeto X",
                to_entity="Alice",
                relation_type="owner_of",
                context="Primary owner",
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get("/api/relations", params={"entity_a": "Projeto X", "type": "owner_of"})
            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(len(payload["data"]), 1)
            self.assertEqual(payload["data"][0]["id"], relation.id)
            self.assertEqual(payload["data"][0]["entity_b_id"], relation.entity_b_id)

    def test_cycle_list_and_read_expose_operational_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            cycle = create_cycle(
                workspace_root,
                cycle_type="daily",
                start="2026-03-13",
            )
            create_activity(
                workspace_root,
                title="Finish report",
                cycle_id=cycle.id,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            list_response = client.get("/api/cycles", params={"type": "daily"})
            self.assertEqual(list_response.status_code, 200)
            list_payload = list_response.json()
            self.assertEqual(list_payload["status"], "ok")
            self.assertEqual(len(list_payload["data"]), 1)
            self.assertEqual(list_payload["data"][0]["id"], cycle.id)
            self.assertEqual(list_payload["data"][0]["activity_count"], 1)

            read_response = client.get(f"/api/cycles/{cycle.id}")
            self.assertEqual(read_response.status_code, 200)
            read_payload = read_response.json()
            self.assertEqual(read_payload["status"], "ok")
            self.assertEqual(read_payload["data"]["type"], "daily")
            self.assertEqual(read_payload["data"]["pending_count"], 1)

    def test_cycle_read_returns_404_for_missing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get("/api/cycles/cycle-daily-missing")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Cycle not found: cycle-daily-missing", response.json()["message"])

    def test_activity_list_and_read_expose_existing_local_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            cycle = create_cycle(
                workspace_root,
                cycle_type="daily",
                start="2026-03-13",
            )
            activity = create_activity(
                workspace_root,
                title="Finish report",
                cycle_id=cycle.id,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            list_response = client.get("/api/activities", params={"cycle_id": cycle.id})
            self.assertEqual(list_response.status_code, 200)
            list_payload = list_response.json()
            self.assertEqual(list_payload["status"], "ok")
            self.assertEqual(len(list_payload["data"]), 1)
            self.assertEqual(list_payload["data"][0]["id"], activity.id)

            read_response = client.get(f"/api/activities/{activity.id}")
            self.assertEqual(read_response.status_code, 200)
            read_payload = read_response.json()
            self.assertEqual(read_payload["status"], "ok")
            self.assertEqual(read_payload["data"]["title"], "Finish report")
            self.assertEqual(read_payload["data"]["cycle_id"], cycle.id)

    def test_activity_read_returns_404_for_missing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.get("/api/activities/missing-activity")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Activity not found: missing-activity", response.json()["message"])

    def test_activity_status_update_endpoint_updates_record_and_audit_log(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            cycle = create_cycle(
                workspace_root,
                cycle_type="daily",
                start="2026-03-13",
            )
            activity = create_activity(
                workspace_root,
                title="Finish report",
                cycle_id=cycle.id,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.patch(
                f"/api/activities/{activity.id}",
                json={"status": "in_progress"},
            )
            self.assertEqual(response.status_code, 200)
            payload = response.json()
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["data"]["id"], activity.id)
            self.assertEqual(payload["data"]["status"], "in_progress")

            connection = duckdb.connect(str(workspace_root / "nexus.duckdb"))
            try:
                activity_row = connection.execute(
                    "SELECT status FROM activities WHERE id = ?",
                    [activity.id],
                ).fetchone()
                self.assertEqual(activity_row, ("in_progress",))

                audit_row = connection.execute(
                    """
                    SELECT action, entity_type, agent, reason
                    FROM audit_log
                    WHERE entity_type = 'activity' AND entity_id = ? AND action = 'update'
                    ORDER BY timestamp DESC, id DESC
                    LIMIT 1
                    """,
                    [activity.id],
                ).fetchone()
                self.assertEqual(
                    audit_row,
                    ("update", "activity", "user", "API activity status update"),
                )
            finally:
                connection.close()

    def test_activity_status_update_rejects_invalid_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            cycle = create_cycle(
                workspace_root,
                cycle_type="daily",
                start="2026-03-13",
            )
            activity = create_activity(
                workspace_root,
                title="Finish report",
                cycle_id=cycle.id,
            )
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.patch(
                f"/api/activities/{activity.id}",
                json={"status": "done"},
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Invalid activity status: done.", response.json()["message"])

    def test_activity_status_update_returns_404_for_missing_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            client = TestClient(create_app(workspace_root=workspace_root))

            response = client.patch(
                "/api/activities/missing-activity",
                json={"status": "completed"},
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["status"], "error")
            self.assertIn("Activity not found: missing-activity", response.json()["message"])

    def test_graph_endpoints_fail_cleanly_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "outside"
            workspace_root.mkdir(parents=True, exist_ok=True)
            client = TestClient(create_app(workspace_root=workspace_root))

            entity_response = client.get("/api/entities")
            self.assertEqual(entity_response.status_code, 409)
            self.assertEqual(entity_response.json()["status"], "error")
            self.assertIn("Current directory is not a Nexus workspace", entity_response.json()["message"])

            document_response = client.get("/api/documents")
            self.assertEqual(document_response.status_code, 409)
            self.assertEqual(document_response.json()["status"], "error")
            self.assertIn("Current directory is not a Nexus workspace", document_response.json()["message"])

            document_integrity_response = client.get("/api/document-integrity")
            self.assertEqual(document_integrity_response.status_code, 409)
            self.assertEqual(document_integrity_response.json()["status"], "error")
            self.assertIn(
                "Current directory is not a Nexus workspace",
                document_integrity_response.json()["message"],
            )

            document_update_response = client.patch(
                "/api/documents/document-123",
                json={"status": "approved"},
            )
            self.assertEqual(document_update_response.status_code, 409)
            self.assertEqual(document_update_response.json()["status"], "error")
            self.assertIn(
                "Current directory is not a Nexus workspace",
                document_update_response.json()["message"],
            )

            document_integrity_read_response = client.get("/api/document-integrity/document-123")
            self.assertEqual(document_integrity_read_response.status_code, 409)
            self.assertEqual(document_integrity_read_response.json()["status"], "error")
            self.assertIn(
                "Current directory is not a Nexus workspace",
                document_integrity_read_response.json()["message"],
            )

            relation_response = client.get("/api/relations")
            self.assertEqual(relation_response.status_code, 409)
            self.assertEqual(relation_response.json()["status"], "error")
            self.assertIn("Current directory is not a Nexus workspace", relation_response.json()["message"])

            cycle_response = client.get("/api/cycles")
            self.assertEqual(cycle_response.status_code, 409)
            self.assertEqual(cycle_response.json()["status"], "error")
            self.assertIn("Current directory is not a Nexus workspace", cycle_response.json()["message"])

            activity_response = client.get("/api/activities")
            self.assertEqual(activity_response.status_code, 409)
            self.assertEqual(activity_response.json()["status"], "error")
            self.assertIn("Current directory is not a Nexus workspace", activity_response.json()["message"])

            activity_update_response = client.patch(
                "/api/activities/activity-123",
                json={"status": "completed"},
            )
            self.assertEqual(activity_update_response.status_code, 409)
            self.assertEqual(activity_update_response.json()["status"], "error")
            self.assertIn(
                "Current directory is not a Nexus workspace",
                activity_update_response.json()["message"],
            )

            cockpit_response = client.get("/")
            self.assertEqual(cockpit_response.status_code, 200)
            self.assertIn("Nexus Cockpit", cockpit_response.text)


if __name__ == "__main__":
    unittest.main()
