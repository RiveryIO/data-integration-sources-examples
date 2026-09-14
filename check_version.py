#!/usr/bin/env python3
import subprocess
import sys

def get_version(ref):
    try:
        cmd = f"git show {ref}:data_integration_sources_examples/__init__.py"
        content = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True)
        return [line for line in content.split('\n') if '__version__' in line][0]
    except Exception:
        return None

def validate():
    try:
        head_sha = subprocess.check_output("git rev-parse HEAD", shell=True, text=True).strip()
        main_sha = subprocess.check_output("git rev-parse origin/main", shell=True, text=True).strip()
        if head_sha == main_sha:
            print(f"Version matches! {head_sha} == {main_sha}")
            return  # Same commit, skip check
    except Exception:
        return  # Can't check, allow build

    current = get_version("HEAD")
    remote = get_version("origin/main")

    if current == remote:
        print("Error: Version in __init__.py must be updated before committing.")
        sys.exit(1)

    print("Version bump detected")

if __name__ == "__main__":
    validate()
