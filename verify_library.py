#!/usr/bin/env python3
"""Verify library structure and importability."""

import sys


def verify_library():
    """Verify library can be imported and is properly structured."""
    try:
        import data_integration_sources_examples
        from data_integration_sources_examples import helpers
    except ImportError as e:
        print(f"Import failed: {e}")
        return False

    validation = helpers.validate_library_structure()

    if not validation["valid"]:
        print("Library structure validation failed")
        for err in validation["errors"]:
            print(f"  {err}")
        return False

    print(f"Library v{data_integration_sources_examples.__version__} - OK")
    print(f"Integration types: {', '.join(validation['integration_types'])}")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify_library() else 1)
