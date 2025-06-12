#!/bin/bash

# Navigate to the script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup first..."
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Run the app
echo "🤖 Starting Humanize AI Text Processor..."
python3 humanize_text_app.py 