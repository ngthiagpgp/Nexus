from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

WORKSPACE_MARKER_DIRNAME = ".nexus"
WORKSPACE_CONFIG_FILENAME = "config.yaml"
DATABASE_FILENAME = "nexus.duckdb"
DOCUMENTS_DIRNAME = "documents"
BACKUPS_DIRNAME = "backups"
DOCUMENT_CYCLE_DIRS = ("daily", "weekly", "monthly")


@dataclass(frozen=True)
class WorkspaceLayout:
    root: Path
    marker_dir: Path
    backups_dir: Path
    config_path: Path
    database_path: Path
    documents_dir: Path
    document_cycle_dirs: tuple[Path, ...]

    @property
    def required_directories(self) -> tuple[Path, ...]:
        return (
            self.marker_dir,
            self.backups_dir,
            self.documents_dir,
            *self.document_cycle_dirs,
        )


def workspace_layout(root: Path) -> WorkspaceLayout:
    resolved_root = root.expanduser().resolve()
    marker_dir = resolved_root / WORKSPACE_MARKER_DIRNAME
    documents_dir = resolved_root / DOCUMENTS_DIRNAME
    document_cycle_dirs = tuple(
        documents_dir / dirname for dirname in DOCUMENT_CYCLE_DIRS
    )
    return WorkspaceLayout(
        root=resolved_root,
        marker_dir=marker_dir,
        backups_dir=marker_dir / BACKUPS_DIRNAME,
        config_path=marker_dir / WORKSPACE_CONFIG_FILENAME,
        database_path=resolved_root / DATABASE_FILENAME,
        documents_dir=documents_dir,
        document_cycle_dirs=document_cycle_dirs,
    )
