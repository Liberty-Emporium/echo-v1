#!/bin/bash
# Echo's App Test Runner
# Run all tests or target specific apps
# Usage: ./run_tests.sh [app-name]
# Example: ./run_tests.sh ai-agent-widget

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🤖 Echo App Test Suite"
echo "======================"

# Install dependencies if needed
if ! python3 -c "import playwright" 2>/dev/null; then
  echo "📦 Installing dependencies..."
  pip install -r requirements.txt -q
  playwright install chromium --with-deps -q
fi

# Run tests
if [ -n "$1" ]; then
  echo "🎯 Testing: $1"
  python3 -m pytest test_all_apps.py -v -k "$1" --tb=short
else
  echo "🌐 Testing ALL apps..."
  python3 -m pytest test_all_apps.py -v --tb=short
fi
