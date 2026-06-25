#!/bin/zsh
# Double-click this file in Finder to run the digest.
# It handles everything: goes to the project, turns on the environment, runs.
cd "$(dirname "$0")"
source .venv/bin/activate
python digest.py
echo ""
echo "Done. You can close this window."
