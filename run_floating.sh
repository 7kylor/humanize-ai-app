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
    pip install pynput pyobjc-framework-Cocoa pyobjc-framework-ApplicationServices
}

# Make floating app executable
chmod +x floating_humanize_app.py

# Show accessibility permission notice
echo ""
echo "🔐 IMPORTANT: Accessibility Permissions Required"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "This app needs accessibility permissions to work system-wide."
echo ""
echo "📋 What the app does:"
echo "   • Monitors global hotkey (⌘⇧H) across all apps"
echo "   • Reads selected text from any application"
echo "   • Replaces text with humanized version"
echo "   • Floats above all windows on every desktop/space"
echo ""
echo "🔧 How to grant permissions:"
echo "   1. System Preferences → Security & Privacy → Privacy"
echo "   2. Click 'Accessibility' in the left sidebar"
echo "   3. Click the lock icon and enter your password"
echo "   4. Add 'Python' or 'Terminal' to the list"
echo "   5. Restart this app if needed"
echo ""
echo "✨ Once permissions are granted:"
echo "   • Press ⌘⇧H anywhere to humanize selected text"
echo "   • The floating window works on all desktops"
echo "   • Click the (-) button to minimize to dock"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This app is designed for macOS."
    echo "   Some features may not work on other platforms."
    echo ""
fi

# Run the floating app with error handling
echo "🤖 Starting Floating Humanize AI..."
echo "   Press Ctrl+C to stop the app"
echo ""

# Trap Ctrl+C for clean shutdown
trap 'echo ""; echo "🛑 Shutting down Floating Humanize AI..."; exit 0' INT

# Run with error handling
if python3 floating_humanize_app.py; then
    echo "✅ Floating Humanize AI stopped normally"
else
    exit_code=$?
    echo ""
    echo "❌ Floating Humanize AI stopped with error (exit code: $exit_code)"
    echo ""
    echo "🔍 Common issues and solutions:"
    echo "   • Missing accessibility permissions → Follow setup instructions above"
    echo "   • Python modules missing → Run: pip install pynput pyobjc"
    echo "   • Network issues → Check internet connection"
    echo "   • API key issues → Check your Humanize AI account"
    echo ""
    exit $exit_code
fi 