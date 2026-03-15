from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexus.activities import create_activity, update_activity_status_mutation
from nexus.core.read_models import inspect_workspace_read_model
from nexus.core.registry import get_type_capabilities, list_registered_types
from nexus.cycles import create_cycle
from nexus.documents import (
    create_document,
    reconcile_document_mutation,
    update_document_status,
    update_document_status_mutation,
)
from nexus.entities import create_entity
from nexus.relations import create_relation
from nexus.workspace import initialize_workspace


class NexusCoreArchitectureTest(unittest.TestCase):
    def test_workspace_read_model_centralizes_operational_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            create_entity(
                workspace_root,
                name="Projeto X",
                entity_type="project",
                context="Pesquisa",
            )
            create_entity(
                workspace_root,
                name="Alice",
                entity_type="person",
                context=None,
            )
            create_relation(
                workspace_root,
                from_entity="Projeto X",
                to_entity="Alice",
                relation_type="owner_of",
                context=None,
            )
            cycle = create_cycle(
                workspace_root,
                cycle_type="daily",
                start="2026-03-15",
            )
            create_activity(
                workspace_root,
                title="Review workspace",
                cycle_id=cycle.id,
            )
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-15",
                cycle_id=cycle.id,
            )
            update_document_status(
                workspace_root,
                selector=document.id,
                status="approved",
                allow_title_lookup=False,
            )

            overview = inspect_workspace_read_model(workspace_root)

            self.assertTrue(overview.is_workspace)
            self.assertIsNotNone(overview.resource_counts)
            self.assertIsNotNone(overview.activity_summary)
            self.assertEqual(overview.resource_counts.entities, 2)
            self.assertEqual(overview.resource_counts.relations, 1)
            self.assertEqual(overview.resource_counts.cycles, 1)
            self.assertEqual(overview.resource_counts.activities, 1)
            self.assertEqual(overview.resource_counts.documents, 1)
            self.assertEqual(overview.resource_counts.approved_documents, 1)
            self.assertEqual(overview.activity_summary.pending, 1)
            self.assertEqual(overview.activity_summary.in_progress, 0)

    def test_type_capability_registry_describes_current_primitives(self) -> None:
        registry = {entry.type_name: entry for entry in list_registered_types()}

        self.assertEqual(set(registry), {"activity", "cycle", "document", "entity", "relation"})
        self.assertTrue(registry["document"].has_lifecycle)
        self.assertTrue(registry["document"].has_integrity)
        self.assertTrue(registry["document"].has_status_transitions)
        self.assertTrue(registry["activity"].has_status_transitions)
        self.assertFalse(registry["activity"].has_integrity)
        self.assertFalse(registry["entity"].has_lifecycle)
        self.assertTrue(registry["relation"].read_heavy)
        self.assertEqual(get_type_capabilities("DOCUMENT"), registry["document"])

    def test_controlled_mutations_return_explicit_mutation_results(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            initialize_workspace(workspace_root)
            cycle = create_cycle(
                workspace_root,
                cycle_type="daily",
                start="2026-03-15",
            )
            activity = create_activity(
                workspace_root,
                title="Review workspace",
                cycle_id=cycle.id,
            )
            document = create_document(
                workspace_root,
                document_type="daily",
                title="Daily 2026-03-15",
                cycle_id=cycle.id,
            )

            activity_result = update_activity_status_mutation(
                workspace_root,
                activity_id=activity.id,
                status="in_progress",
            )
            self.assertEqual(activity_result.entity_type, "activity")
            self.assertEqual(activity_result.entity_id, activity.id)
            self.assertEqual(activity_result.action, "update")
            self.assertEqual(activity_result.payload.status, "in_progress")

            document_status_result = update_document_status_mutation(
                workspace_root,
                selector=document.id,
                status="approved",
                allow_title_lookup=False,
            )
            self.assertEqual(document_status_result.entity_type, "document")
            self.assertEqual(document_status_result.entity_id, document.id)
            self.assertEqual(document_status_result.action, "update")
            self.assertEqual(document_status_result.payload.status, "approved")

            document_path = workspace_root / document_status_result.payload.path
            document_path.write_text("# Daily 2026-03-15\n\nChanged\n", encoding="utf-8")
            reconcile_result = reconcile_document_mutation(
                workspace_root,
                selector=document.id,
                allow_title_lookup=False,
            )
            self.assertEqual(reconcile_result.entity_type, "document")
            self.assertEqual(reconcile_result.entity_id, document.id)
            self.assertEqual(reconcile_result.action, "reconcile")
            self.assertEqual(reconcile_result.payload.record.id, document.id)
            self.assertEqual(reconcile_result.payload.integrity.integrity_state, "ok")
            self.assertEqual(reconcile_result.payload.reconciled_fields, ["content_hash"])


if __name__ == "__main__":
    unittest.main()
