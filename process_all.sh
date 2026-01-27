#!/bin/bash
set -e

cd /Users/djparis/keeping-it-real-content-system
source venv/bin/activate

echo "=== STEP 1: Download remaining episodes ==="
python scripts/download_episodes.py

echo ""
echo "=== STEP 2: Transcribe new episodes ==="
python scripts/transcribe_episodes.py

echo ""
echo "=== STEP 3: Analyze with AI ==="
if [ -z "$OPENAI_API_KEY" ]; then
    echo "ERROR: OPENAI_API_KEY not set"
    exit 1
fi
python scripts/analyze_episodes.py --provider openai --generate-scripts

echo ""
echo "=== COMPLETE ==="
python scripts/analyze_episodes.py --status
