"""Compatibility shim for workspace contract imports.

The explicit platform-core implementation now lives under ``nexus.core``.
"""

from nexus.core.workspace_contract import *  # noqa: F401,F403
