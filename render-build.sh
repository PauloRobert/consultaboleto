#!/usr/bin/env bash
set -euo pipefail

: "${PYTHON_VERSION:?PYTHON_VERSION must be configured in Render}"
expected_version="${PYTHON_VERSION%.*}"
actual_version="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

if [[ "${actual_version}" != "${expected_version}" ]]; then
  echo "Expected Python ${expected_version}, but Render started Python ${actual_version}."
  echo "Set PYTHON_VERSION before deploying and clear the Render build cache."
  exit 1
fi

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
