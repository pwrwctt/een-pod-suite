#!/usr/bin/env python3
from pathlib import Path
import subprocess, zipfile
ROOT=Path(__file__).resolve().parents[1]
VERSION=(ROOT/"VERSION").read_text().strip()
PACKAGE=Path("/home/oai/skills/skill-creator/scripts/package_skill.py")
chat=ROOT/"chatgpt"/"een-pod-suite"
chat_dist=ROOT/"dist"/"chatgpt"; chat_dist.mkdir(parents=True,exist_ok=True)
oc_dist=ROOT/"dist"/"opencode"; oc_dist.mkdir(parents=True,exist_ok=True)
subprocess.run(["python",str(PACKAGE),str(chat),str(chat_dist)],check=True)
out=oc_dist/f"een-pod-suite-opencode-v{VERSION}.zip"
if out.exists(): out.unlink()
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
    for p in (ROOT/"opencode").rglob("*"):
        if p.is_file(): z.write(p,p.relative_to(ROOT/"opencode"))
print(chat_dist/"skill.zip")
print(out)
