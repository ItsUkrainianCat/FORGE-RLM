from pathlib import Path

Path(".forge/AIDE_AUTONOMOUS").unlink(missing_ok=True)
print("AIDE autonomous mutation guard disarmed")
