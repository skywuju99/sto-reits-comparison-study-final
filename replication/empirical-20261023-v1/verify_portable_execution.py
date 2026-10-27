"""Rebuild in a fresh directory without copying any preserved result CSVs."""
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime, timezone
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify():
    expected = json.loads((ROOT / 'docs/expected_results_sha256.json').read_text(encoding='utf-8'))
    if len(expected) != 27:
        raise ValueError('Expected exactly 27 preserved CSV hashes.')
    report = {
        'analysis_version': 'empirical-20261023-v1',
        'verification_revision': '20261027',
        'verified_at_utc': datetime.now(timezone.utc).isoformat(),
        'environment': {'os': platform.system(), 'release': platform.release(),
                        'machine': platform.machine(), 'python': platform.python_version(),
                        'pandas': pd.__version__, 'numpy': np.__version__},
        'fresh_working_directory': True,
        'preserved_results_copied': False,
        'intermediate_outputs_copied': False,
        'cached_input_files_may_be_copied': True,
        'input_sha256_verified_by_pipeline': False,
        'expected_csv_count': len(expected),
        'expected_manifest_sha256': sha(ROOT / 'docs/expected_results_sha256.json'),
        'code_sha256': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p)
                       for p in sorted(list((ROOT / 'code').glob('*.py')) +
                                       list(ROOT.glob('*.py')))},
        'scope': 'Fresh-directory execution in the recorded environment; not validation on every OS, live source recollection, or proof of realized cash flow and legal rights.',
        'passed': False,
    }
    with TemporaryDirectory(prefix='sto-reits-verify-', dir=ROOT.parents[1]) as temp:
        work = Path(temp) / 'replication'
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(
            'results', 'intermediate', '__pycache__', '*.pyc'))
        report['results_absent_before_run'] = not (work / 'results').exists()
        proc = subprocess.run([sys.executable, '-X', 'utf8', str(work / 'run_all.py')],
                              cwd=temp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, encoding='utf-8', errors='replace')
        actual = {p.name: sha(p) for p in sorted((work / 'results').glob('*.csv'))}
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(set(actual) - set(expected))
        changed = sorted(n for n in expected if n in actual and expected[n] != actual[n])
        report.update({'return_code': proc.returncode,
                       'actual_csv_count': len(actual), 'missing': missing,
                       'unexpected': unexpected, 'changed': changed,
                       'csv_sha256': actual,
                       'passed': proc.returncode == 0 and not (missing or unexpected or changed)})
        report['input_sha256_verified_by_pipeline'] = report['passed']
        (ROOT / 'results').mkdir(exist_ok=True)
        (ROOT / 'results/portable_execution_verification.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
        if not report['passed']:
            print(proc.stdout)
            raise RuntimeError('Fresh-directory reproduction failed; see verification JSON.')
        print(f'Fresh-directory verification passed: {len(actual)} / {len(expected)} CSV hashes match on {platform.system()}.')
    return report

if __name__ == '__main__':
    verify()
