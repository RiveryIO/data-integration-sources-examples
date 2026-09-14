"""Utilities for working with data integration source examples."""

import gzip
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_examples_root() -> Path:
    """Get the root directory of examples."""
    return Path(__file__).parent / "examples"


def list_integration_types() -> List[str]:
    """List all top-level integration type directories (e.g. 'custom_report')."""
    root = get_examples_root()
    if not root.exists():
        logger.warning(f"Examples root does not exist: {root}")
        return []
    return [d.name for d in root.iterdir() if d.is_dir() and not d.name.startswith(".")]


def list_sources(integration_type: str) -> List[str]:
    """List all source APIs for a given integration type (e.g. 'adobe_analytics')."""
    path = get_examples_root() / integration_type
    if not path.exists():
        return []
    return [d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]


def list_reports(integration_type: str, source: str) -> List[str]:
    """List all report/resource types for a given integration type + source."""
    path = get_examples_root() / integration_type / source
    if not path.exists():
        return []
    return [d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]


def list_targets(integration_type: str, source: str, report: str) -> List[str]:
    """List all target destinations for a given integration type + source + report."""
    path = get_examples_root() / integration_type / source / report
    if not path.exists():
        return []
    return [d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]


def load_example(relative_path: str) -> Any:
    """
    Load a JSON example file (supports .json and .json.gz).

    Args:
        relative_path: Path relative to the examples root.
                       e.g. "custom_report/adobe_analytics/users/snowflake/get.json"

    Returns:
        Parsed JSON content.
    """
    full_path = get_examples_root() / relative_path
    paths_to_try = [full_path.with_suffix(full_path.suffix + ".gz"), full_path]

    for path in paths_to_try:
        if not path.exists():
            continue
        try:
            if path.suffix == ".gz":
                with gzip.open(path, "rt", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path.name}: {e}")
            raise

    raise FileNotFoundError(f"Example not found: {relative_path}")


def validate_library_structure() -> Dict[str, Any]:
    """
    Validate that the examples directory exists and contains at least one JSON file.

    Returns:
        Dict with 'valid' (bool), 'examples_root_exists' (bool),
        'integration_types' (list), 'errors' (list).
    """
    root = get_examples_root()
    results: Dict[str, Any] = {
        "valid": True,
        "examples_root_exists": root.exists(),
        "integration_types": [],
        "errors": [],
    }

    if not root.exists():
        results["valid"] = False
        results["errors"].append("Examples root does not exist")
        return results

    json_files = list(root.rglob("*.json"))
    integration_types = list_integration_types()
    results["integration_types"] = integration_types

    if not integration_types:
        results["valid"] = False
        results["errors"].append("No integration type directories found under examples/")

    if not json_files:
        results["valid"] = False
        results["errors"].append("No JSON example files found")

    return results
