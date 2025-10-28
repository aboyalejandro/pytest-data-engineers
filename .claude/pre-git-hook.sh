#!/bin/bash

# Claude Code Pre-Git Hook Handler
# Reads JSON from stdin and runs tests if a git commit/push is detected

# Read JSON input from stdin
INPUT=$(cat)

# Extract the bash command from the JSON
BASH_COMMAND=$(echo "$INPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('parameters', {}).get('command', ''))" 2>/dev/null || echo "")

# Check if this is a git commit or push operation
if echo "$BASH_COMMAND" | grep -qE "(git commit|git push)"; then
    echo "🔍 Detected git operation: running pre-commit tests..."

    # Change to project directory
    cd "$CLAUDE_PROJECT_DIR" || exit 0

    # Check if virtual environment exists and activate it
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi

    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo "⚠️  pytest not found. Installing dependencies..."
        python3 -m pip install -q -r requirements.txt 2>&1
    fi

    # Run pytest with verbose output
    echo ""
    echo "🧪 Running tests..."
    echo ""

    if pytest -v main.py 2>&1; then
        echo ""
        echo "✅ All tests passed! Allowing git operation to proceed."
        exit 0
    else
        echo ""
        echo "❌ Tests failed! Blocking git operation."
        echo ""
        echo "Fix the failing tests before committing or pushing."
        # Exit 2 = blocking error; Claude will process this
        exit 2
    fi
fi

# Not a git command, allow it to proceed
exit 0
