"""Run the current thesis replication from any working directory."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/'replication/empirical-20261023-v1/run_all.py'),run_name='__main__')
