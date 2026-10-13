#!/usr/bin/env python3
"""Verify exact author-file bytes against the independent audit binding."""
import hashlib
import json
import pathlib
import sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
manifest = json.loads((root / 'CODE-AUDIT.manifest.json').read_text(encoding='utf-8'))
for row in manifest['reviewed_files']:
    data = (root / row['path']).read_bytes()
    git_blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256'] or git_blob != row['git_blob_sha1']:
        raise SystemExit('MISMATCH: ' + row['path'])
    print('Verified:', row['path'])
print('PASS:', len(manifest['reviewed_files']), 'reviewed files match the audit binding.')
