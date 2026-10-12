#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8 TZ=UTC
{
  printf '$ PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8 TZ=UTC python independent-review/check_documents.py\n'
  python independent-review/check_documents.py
  printf '\nexit_code=0\n'
} > independent-review/documents.log 2>&1
