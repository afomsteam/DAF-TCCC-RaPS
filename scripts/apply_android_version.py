#!/usr/bin/env python3
from pathlib import Path
import re

VERSION_NAME = "2.19.3"
VERSION_CODE = 21903

candidates = [Path("android/app/build.gradle"), Path("android/app/build.gradle.kts")]
path = next((p for p in candidates if p.exists()), None)
if not path:
    raise SystemExit("android/app/build.gradle(.kts) not found")
text = path.read_text(encoding="utf-8")
text2, n1 = re.subn(r'versionCode\s+\d+', f'versionCode {VERSION_CODE}', text, count=1)
text2, n2 = re.subn(r'versionName\s+["\'][^"\']+["\']', f'versionName "{VERSION_NAME}"', text2, count=1)
if not n1:
    text2, n1 = re.subn(r'versionCode\s*=\s*\d+', f'versionCode = {VERSION_CODE}', text2, count=1)
if not n2:
    text2, n2 = re.subn(r'versionName\s*=\s*["\'][^"\']+["\']', f'versionName = "{VERSION_NAME}"', text2, count=1)
if not (n1 and n2):
    raise SystemExit(f"Unable to patch Android version in {path}")
path.write_text(text2, encoding="utf-8")
print(f"Applied Android version {VERSION_NAME} ({VERSION_CODE}) to {path}")
