from pathlib import Path
import runpy,json,hashlib,sys,contextlib
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'fetch_inputs.py'),run_name='__main__')
(ROOT/'results').mkdir(exist_ok=True)
(ROOT/'docs').mkdir(exist_ok=True)
for filename in ('01_normalize.py','02_combine.py','03_diagnostics.py','04_validate.py','05_report.py'):
 print('Running',filename,flush=True)
 with (ROOT/'results'/f'{filename}.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log):
  runpy.run_path(str(ROOT/'code'/filename),run_name='__main__')
outputs={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'results').iterdir()) if p.is_file() and p.suffix=='.csv'}
sources={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'code').glob('*.py'))}
runpy.run_path(str(ROOT/'verify_reproduction.py'),run_name='__main__')
run={'version':'empirical-20261023-v1','python':sys.version,'code_sha256':sources,'csv_output_sha256':outputs,'passed':True,'packaging_revision':'20261027'}
(ROOT/'run_manifest.json').write_text(json.dumps(run,ensure_ascii=False,indent=2),encoding='utf-8')
print('Completed. Results and verification records are in results/.')

