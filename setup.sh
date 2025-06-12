#!/bin/bash

echo "🚀 Setting up Humanize AI Text Processor for macOS..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org or use Homebrew: brew install python3"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "🔧 Installing dependencies..."
pip install -r requirements.txt

# Make the main script executable
chmod +x humanize_text_app.py

echo "✅ Setup complete!"
echo ""
echo "To run the app:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python3 humanize_text_app.py" 