# 🤖 Humanize AI Text Processor for macOS

A fast, reliable, and hassle-free macOS app to humanize selected text in any application, especially Microsoft Word, using the [Humanize AI API](https://docs.humanizeai.pro/).

## ✨ Features

- **Universal Text Selection**: Works with any macOS app (Word, Pages, TextEdit, Safari, etc.)
- **One-Click Processing**: Simple GUI with one button to humanize selected text
- **Automatic Replacement**: Selected text is automatically replaced with humanized version
- **Keyboard Shortcut**: Use `Cmd+Shift+H` for quick access
- **Real-time Status**: Progress bar and status updates during processing
- **Stay-on-Top Window**: App window stays visible while working in other apps

## 🚀 Quick Start

### 1. Setup (One-time)

```bash
# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

### 2. Run the App

```bash
# Simple one-command launch
./run.sh
```

### 3. Use the App

1. **Select text** in any application (Word, Pages, etc.)
2. **Click "Humanize Selected Text"** in the app window
3. **Wait** for processing (usually 10-30 seconds)
4. **Text is automatically replaced** with humanized version

## 📋 Requirements

- **macOS**: Any recent version (tested on macOS 10.14+)
- **Python 3**: Usually pre-installed on macOS
- **Internet Connection**: Required for API access
- **Text Selection**: Minimum 30 words (API requirement)

## 🔧 Manual Installation

If the automatic setup doesn't work:

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install requests

# Run the app
python3 humanize_text_app.py
```

## 💡 Usage Tips

### For Microsoft Word

1. Select the paragraph you want to humanize
2. Keep the Humanize AI app window open
3. Click "Humanize Selected Text" or press `Cmd+Shift+H`
4. The selected text will be automatically replaced

### For Other Apps

- Works with any app that supports text selection
- Make sure text is properly selected before processing
- The app uses AppleScript to read/write text universally

### Best Practices

- **Select complete sentences/paragraphs** for better results
- **Ensure 30+ words** are selected (API requirement)
- **Keep app window visible** for status updates
- **Wait for completion** before making new selections

## ⚙️ How It Works

1. **Text Capture**: Uses AppleScript to copy selected text from any app
2. **API Submission**: Sends text to Humanize AI API for processing
3. **Status Polling**: Monitors processing status every 2 seconds
4. **Text Replacement**: Automatically pastes humanized text back

## 🔐 API Configuration

The app uses your API key: (from .env file)

To change the API key, edit line 18 in `humanize_text_app.py`:

```python
self.api_key = "your_new_api_key_here"
```

## 🚨 Troubleshooting

### "Failed to get selected text"

- Make sure text is properly selected
- Try selecting text again
- Ensure the source app is in focus

### "Text too short"

- Select at least 30 words (API requirement)
- Try selecting a longer paragraph

### "API Error" or "Network error"

- Check internet connection
- Verify API key is valid
- Check if you've hit rate limits (30 requests/minute)

### Permission Issues

- macOS may ask for accessibility permissions
- Go to System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal or Python to allowed apps

## 📁 Project Structure

```
├── humanize_text_app.py    # Main application
├── requirements.txt        # Python dependencies
├── setup.sh               # One-time setup script
├── run.sh                 # Launch script
└── README.md              # This file
```

## 🔄 Updates

To update the app:

1. Download new version files
2. No need to re-run setup if dependencies haven't changed
3. Just run `./run.sh` as usual or `./run_floating.sh` to run the app with the window floating on top of other windows

## 📞 Support

For issues related to:

- **API functionality**: Contact <support@humanizeai.pro>
- **App functionality**: Check this README or create an issue

---

**Made for macOS with ❤️ - Fast, Reliable, Hassle-Free Text Humanization**
