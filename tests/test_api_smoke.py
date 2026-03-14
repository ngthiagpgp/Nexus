from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from nexus.api import create_app
from nexus.activities import create_activity
from nexus.cycles import create_cycle
from nexus.documents import create_document
from nexus.entities import create_entity
from nexus.relations import create_relation
from nexus.workspace import initialize_workspace


class NexusApiSmokeTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
