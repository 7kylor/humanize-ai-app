#!/bin/bash

# Navigate to the script directory
cd "$(dirname "$0")"

echo "🚀 Launching Floating Humanize AI App..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup first..."
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Check for required dependencies
echo "🔧 Checking dependencies..."
python3 -c "import pynput, requests" 2>/dev/null || {
    echo "📦 Installing additional dependencies for floating app..."
    pip install pynput pyobjc-framework-Cocoa
}

# Make floating app executable
chmod +x floating_humanize_app.py

# Show accessibility permission notice
echo ""
echo "🔐 IMPORTANT: Accessibility Permissions Required"
echo "This app needs accessibility permissions to work system-wide."
echo "If prompted, please grant permissions in System Preferences."
echo ""

# Run the floating app
echo "🤖 Starting Floating Humanize AI..."
python3 floating_humanize_app.py 