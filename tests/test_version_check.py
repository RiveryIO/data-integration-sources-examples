"""Test to ensure version was bumped for PRs."""
import subprocess
import sys


def test_version_bumped():
    """Verify version was bumped compared to main branch."""
    # Only run this check on CI, not locally
    if not subprocess.run(
        ["git", "rev-parse", "--verify", "origin/main"],
        capture_output=True
    ).returncode == 0:
        # origin/main doesn't exist (likely first commit or local dev)
        return

    result = subprocess.run(
        [sys.executable, "check_version.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Version check failed: {result.stdout}\n{result.stderr}"
