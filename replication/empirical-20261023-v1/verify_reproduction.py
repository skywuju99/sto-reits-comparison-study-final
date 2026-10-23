"""Compare the rebuilt result files with the preserved final thesis outputs."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
expected=json.loads((ROOT/'docs/expected_results_sha256.json').read_text(encoding='utf-8'))
actual={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (ROOT/'results').glob('*.csv')}
if actual!=expected:
 raise AssertionError({'missing':sorted(set(expected)-set(actual)),'unexpected':sorted(set(actual)-set(expected)),'changed':[n for n in expected if n in actual and expected[n]!=actual[n]]})
print(f'Final thesis reproduction verified: {len(expected)} CSV files match.')
