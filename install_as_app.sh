#!/bin/bash

echo "📱 Installing Humanize AI as macOS App..."

APP_NAME="Humanize AI"
APP_DIR="/Applications/Humanize AI.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

# Create app bundle structure
echo "🏗️  Creating app bundle..."
sudo mkdir -p "$MACOS_DIR"
sudo mkdir -p "$RESOURCES_DIR"

# Copy main app file
echo "📄 Copying app files..."
sudo cp floating_humanize_app.py "$MACOS_DIR/HumanizeAI"
sudo chmod +x "$MACOS_DIR/HumanizeAI"

# Create Info.plist
echo "📝 Creating app info..."
sudo tee "$CONTENTS_DIR/Info.plist" > /dev/null <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>HumanizeAI</string>
    <key>CFBundleIdentifier</key>
    <string>com.humanizeai.textprocessor</string>
    <key>CFBundleName</key>
    <string>Humanize AI</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSUIElement</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.productivity</string>
</dict>
</plist>
EOF

# Create launch script that activates Python environment
sudo tee "$MACOS_DIR/HumanizeAI" > /dev/null <<EOF
#!/bin/bash
cd "\$(dirname "\$0")"
if [ -f "/usr/bin/python3" ]; then
    PYTHON="/usr/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    PYTHON="/usr/local/bin/python3"
else
    PYTHON="python3"
fi

# Install dependencies if needed
\$PYTHON -m pip install --user requests pynput pyobjc-framework-Cocoa 2>/dev/null

# Run the app
\$PYTHON -c "
import sys
sys.path.insert(0, '/Applications/Humanize AI.app/Contents/MacOS')
exec(open('/Applications/Humanize AI.app/Contents/MacOS/floating_humanize_app.py').read())
"
EOF

sudo chmod +x "$MACOS_DIR/HumanizeAI"

# Copy Python script with a different name to avoid conflicts
sudo cp floating_humanize_app.py "$MACOS_DIR/floating_humanize_app.py"

echo "✅ App installed successfully!"
echo ""
echo "🎉 Humanize AI is now available in your Applications folder"
echo "💡 To use:"
echo "   1. Open 'Humanize AI' from Applications"
echo "   2. Grant accessibility permissions when prompted"
echo "   3. Use ⌘⇧H anywhere to humanize selected text"
echo ""
echo "🔐 Remember to grant accessibility permissions in:"
echo "   System Preferences → Security & Privacy → Privacy → Accessibility" 