"""Use existing local embedding credentials without copying or printing secrets."""
import os
from pathlib import Path
import sys

for line in Path('/Users/chasoik/Projects/image-prompt/.env').read_text().splitlines():
 if '=' not in line or line.lstrip().startswith('#'):continue
 key,value=line.split('=',1);key=key.strip()
 if key in {'GEMINI_API_KEY','GOOGLE_API_KEY'} and key not in os.environ:
  os.environ[key]=value.strip().strip('"').strip("'")
os.execvpe(sys.executable,[sys.executable,*sys.argv[1:]],os.environ)
