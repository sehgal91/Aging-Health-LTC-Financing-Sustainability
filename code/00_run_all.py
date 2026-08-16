"""Run repository consistency checks without refitting unverified models."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
for script in ("01_data_cleaning_and_merging.py", "02_variable_construction.py", "03_reported_output_tables.py"):
    subprocess.run([sys.executable, str(ROOT / "code" / script)], cwd=ROOT, check=True)

