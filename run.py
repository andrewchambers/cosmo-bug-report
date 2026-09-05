"""Run each executable repeatedly and preserve raw results, including signals."""
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import sys


def main():
    results = []
    for filename in sys.argv[1:]:
        path = Path(filename).resolve()
        statuses = []
        for _ in range(10):
            try:
                # Some upstream APE build modes rewrite their own header.
                # Keep each trial and the cross-platform artifact pristine.
                with tempfile.TemporaryDirectory() as directory:
                    executable = Path(directory) / path.name
                    shutil.copy2(path, executable)
                    executable.chmod(executable.stat().st_mode | 0o111)
                    run = subprocess.run(["/bin/sh", str(executable)], capture_output=True, timeout=15)
                    statuses.append(run.returncode)
            except subprocess.TimeoutExpired:
                statuses.append("timeout")
        result = {"binary": path.name, "system": platform.platform(), "machine": platform.machine(), "exit_codes": statuses}
        results.append(result)
        print(json.dumps(result), flush=True)
    Path("results.json").write_text(json.dumps(results, indent=2) + "\n")
    return int(any(code != 0 for result in results for code in result["exit_codes"]))


if __name__ == "__main__":
    sys.exit(main())
