import json
from pathlib import Path
import subprocess

commands = {
    "baseline": ["/bin/sh", "artifacts/repro.com"],
    "sigsys": ["/bin/sh", "artifacts/sigsys.com"],
    "lldb": [
        "lldb", "--batch",
        "-o", "settings set target.disable-aslr false",
        "-o", "run",
        "-k", "register read --all",
        "-k", "thread backtrace all",
        "-k", "disassemble --start-address `$pc-40` --count 25",
        "--", "artifacts/repro.macho",
    ],
}
for name, command in commands.items():
    try:
        result = subprocess.run(command, capture_output=True, timeout=120)
        output = result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace")
        output = json.dumps({"command": command, "exit_code": result.returncode}) + "\n" + output
    except subprocess.TimeoutExpired as error:
        output = f"timeout: {command}\n" + (error.stdout or b"").decode(errors="replace") + (error.stderr or b"").decode(errors="replace")
    Path(f"artifacts/{name}.txt").write_text(output)
    print(f"--- {name} ---\n{output}", flush=True)
