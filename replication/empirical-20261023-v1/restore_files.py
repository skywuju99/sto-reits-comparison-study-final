"""Losslessly restore packed inputs, or preserved detailed results on request."""
from pathlib import Path
import json,gzip,hashlib,sys
ROOT=Path(__file__).resolve().parent
def restore(include_results=False):
 count=0
 for item in json.loads((ROOT/'packed_files.json').read_text(encoding='utf-8')):
  if item['path'].startswith('results/') and not include_results:continue
  target=(ROOT/item['path']).resolve()
  if not target.is_relative_to(ROOT.resolve()):raise ValueError('Invalid packed path')
  if target.exists():
   if hashlib.sha256(target.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Existing file differs: '+item['path'])
   continue
  chunks=[]
  for part in item['parts']:
   pp=(ROOT/part['path']).resolve()
   if not pp.is_relative_to(ROOT.resolve()):raise ValueError('Invalid part path')
   chunk=pp.read_bytes()
   if hashlib.sha256(chunk).hexdigest()!=part['sha256']:raise ValueError('Packed part hash mismatch')
   chunks.append(chunk)
  raw=gzip.decompress(b''.join(chunks))
  if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:raise ValueError('Restored file mismatch')
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);count+=1
 return count
if __name__=='__main__':print('Restored files:',restore('--include-results' in sys.argv))
