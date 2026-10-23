"""Retrieve only the preserved raw source archive, with pinned SHA-256 validation."""
from pathlib import Path
from urllib.request import Request,urlopen
from zipfile import ZipFile
import hashlib,json,shutil,tempfile,os,runpy
ROOT=Path(__file__).resolve().parent
URL='https://github.com/skywuju99/sto-reits-comparison-study-final/releases/download/v2.0.0/secondary_market_raw_sources_v2.0.zip'
ARCHIVE_SHA256='9c91153ae47fb3d8f9765aa1d677d17c3523abf0c10c7159b846ea4584b0a642'
def ensure_inputs():
 runpy.run_path(str(ROOT/'restore_files.py'))['restore'](False)
 entries=json.loads((ROOT/'inputs_manifest.json').read_text(encoding='utf-8'))
 missing=[e for e in entries if not (ROOT/e['path']).exists()]
 if missing:
  if any(not e['path'].startswith('inputs/raw/') for e in missing):
   raise FileNotFoundError('Non-raw input is missing: download the complete repository.')
  if os.environ.get('REPLICATION_OFFLINE')=='1':
   raise FileNotFoundError('Offline mode: place both original CSVs in inputs/raw/.')
  print('Downloading preserved raw sources from GitHub Release v2.0.0 ...',flush=True)
  with tempfile.TemporaryDirectory(dir=ROOT) as temp:
   archive=Path(temp)/'sources.zip'
   with urlopen(Request(URL,headers={'User-Agent':'sto-reits-replication'}),timeout=120) as response, archive.open('wb') as out:
    shutil.copyfileobj(response,out)
   if hashlib.sha256(archive.read_bytes()).hexdigest()!=ARCHIVE_SHA256:
    raise ValueError('Raw archive hash mismatch; do not substitute a changed release.')
   with ZipFile(archive) as z:
    for entry in missing:
     target=ROOT/entry['path'];data=z.read(target.name)
     if hashlib.sha256(data).hexdigest()!=entry['sha256']:raise ValueError('Raw file hash mismatch')
     target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 for entry in entries:
  if hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()!=entry['sha256']:
   raise ValueError('Input hash mismatch: '+entry['path'])
 return len(entries)
if __name__=='__main__': print('Verified input files:',ensure_inputs())
