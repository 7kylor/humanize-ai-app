# 🚀 Floating Humanize AI - System-Wide Text Processor

A **floating, system-wide** macOS app that works everywhere - in Microsoft Word, Safari, Pages, or any application. Uses the [Humanize AI API](https://docs.humanizeai.pro/) to humanize selected text with global hotkeys and accessibility permissions.

## ✨ **Key Features**

### 🌐 **Works Everywhere**

- **Microsoft Word** - Seamlessly humanize paragraphs
- **Safari/Chrome** - Humanize web content
- **Pages/TextEdit** - Any text editor
- **Slack/Teams** - Chat and messaging apps
- **Any macOS Application** - Universal compatibility

### 🎯 **Floating Interface**

- **Always-on-top** window that never gets lost
- **Positioned in top-right corner** - out of the way
- **Minimizes to dock** - click to restore
- **Semi-transparent** - doesn't obstruct your work
- **macOS-native design** - clean and modern

### ⚡ **Global Hotkey**

- **Press `⌘⇧H` anywhere** to humanize selected text
- **Works even when app is minimized**
- **No need to switch between applications**
- **Instant access from any window**

### 🔐 **Accessibility Integration**

- **Automatic permission detection**
- **Guided setup for macOS permissions**
- **System-level text access**
- **Secure and private processing**

## 🚀 **Quick Start**

### Method 1: Floating App (Recommended)

```bash
# Launch the floating app
./run_floating.sh
```

### Method 2: Install as Native macOS App

```bash
# Install to Applications folder
sudo ./install_as_app.sh
```

### Method 3: Basic Version

```bash
# Standard window version
./run.sh
```

## 🔐 **Setting Up Accessibility Permissions**

**CRITICAL**: The app needs accessibility permissions to work system-wide.

### Automatic Setup

1. **Run the app** - it will detect missing permissions
2. **Click "Open System Preferences"** when prompted
3. **Follow the guided setup**

### Manual Setup

1. **Open System Preferences** (⚙️)
2. **Go to Security & Privacy**
3. **Click Privacy tab**
4. **Select Accessibility** from left sidebar
5. **Click the lock** 🔒 and enter your password
6. **Click the "+" button**
7. **Add one of these:**
   - `Terminal` (if running from Terminal)
   - `Python` (if using Python directly)
   - `Humanize AI` (if installed as app)
8. **Check the checkbox** to enable
9. **Restart the app**

### Troubleshooting Permissions

```bash
# Test accessibility permissions
osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true'
```

If this returns an app name, permissions are working. If it shows an error, permissions need to be granted.

## 💡 **How to Use**

### **Basic Usage:**

1. **Select text** in any application (Word, Safari, etc.)
2. **Press `⌘⇧H`** or click the floating button
3. **Wait 10-30 seconds** for processing
4. **Text is automatically replaced** with humanized version

### **Best Practices:**

- **Select complete sentences/paragraphs** (30+ words required)
- **Keep the floating window visible** for status updates
- **Don't select text while processing** - wait for completion
- **Use in well-formatted documents** for best results

### **Supported Applications:**

- ✅ **Microsoft Word** - Full support
- ✅ **Pages** - Full support  
- ✅ **TextEdit** - Full support
- ✅ **Safari/Chrome** - Text fields and content
- ✅ **Slack/Teams** - Message composition
- ✅ **Mail** - Email composition
- ✅ **Notes** - Note taking
- ✅ **Any text input field** - Universal support

## 🎨 **Floating App Interface**

```
┌─────────────────────────┐
│ 🤖 Humanize AI         │
│                         │
│ Ready • Press ⌘⇧H      │
│ ████████████████████    │ ← Progress bar (when active)
│                         │
│ [Humanize Selected Text]│
│                         │
│ Global Hotkey: ⌘⇧H     │
│ Works in any app        │
│                    [−]  │ ← Minimize button
└─────────────────────────┘
```

## ⚙️ **Technical Details**

### **System Integration:**

- **AppleScript automation** for universal text access
- **Global hotkey listener** using `pynput`
- **macOS Accessibility API** for system-wide functionality
- **Native notification system** for user feedback

### **API Integration:**

- **Humanize AI API** with your key: `sk_ljx30mzi36a2nb8jlfo0pd`
- **Automatic polling** every 2 seconds until completion
- **Error handling** with user-friendly messages
- **Rate limit awareness** (30 requests/minute)

### **Security Features:**

- **Temporary clipboard usage** - original content restored
- **Local processing** - no permanent data storage
- **Secure API communication** - HTTPS only
- **Permission-based access** - user controlled

## 🚨 **Troubleshooting**

### **"NO_ACCESS" or Permission Errors:**

1. **Grant accessibility permissions** (see setup guide above)
2. **Restart the app** after granting permissions
3. **Try running as:** `sudo ./run_floating.sh` (temporary solution)

### **Global Hotkey Not Working:**

1. **Check accessibility permissions** are granted
2. **Restart the app** completely
3. **Try clicking the floating button** instead
4. **Ensure another app isn't using `⌘⇧H`**

### **Text Not Being Selected:**

1. **Make sure text is properly highlighted** before pressing hotkey
2. **Try selecting text again** and wait 1 second
3. **Use Cmd+A to select all** if having trouble with partial selection

### **"Text too short" Error:**

- **Select at least 30 words** (API requirement)
- **Include complete sentences** for better results
- **Try selecting a longer paragraph**

### **API Errors:**

- **Check internet connection**
- **Verify API key is valid**
- **Check rate limits** (max 30 requests/minute)
- **Try again** after a few seconds

### **App Won't Start:**

```bash
# Check Python installation
python3 --version

# Install missing dependencies
pip install requests pynput pyobjc-framework-Cocoa

# Run with debug output
python3 floating_humanize_app.py
```

## 📁 **Project Structure**

```
├── floating_humanize_app.py     # Main floating app
├── humanize_text_app.py         # Basic window version
├── run_floating.sh              # Launch floating app
├── install_as_app.sh            # Install as native app
├── setup.sh                     # One-time setup
├── requirements.txt             # Dependencies
└── FLOATING_README.md           # This file
```

## 🔄 **App Versions**

| Version | Description | Launch Command |
|---------|-------------|----------------|
| **Floating** | System-wide, always-on-top | `./run_floating.sh` |
| **Native App** | Installed in Applications | `./install_as_app.sh` |
| **Basic** | Standard window | `./run.sh` |

## 🎯 **Perfect for Microsoft Word**

This app is specifically optimized for Microsoft Word workflows:

1. **Open Word document**
2. **Keep Humanize AI floating window visible**
3. **Select paragraph you want to humanize**
4. **Press `⌘⇧H`** (works even when Word is active)
5. **Continue writing** - text is automatically replaced
6. **Repeat for any paragraph** - lightning fast workflow

## 🔮 **Advanced Usage**

### **Batch Processing:**

- Select multiple paragraphs
- Press `⌘⇧H` for each section
- Process large documents efficiently

### **Integration with Writing Workflow:**

- Write content naturally
- Humanize specific sections as needed
- Maintain writing flow without switching apps

### **Hotkey Customization:**

Edit `floating_humanize_app.py` line 165 to change hotkey:

```python
'<cmd>+<shift>+h': on_hotkey  # Change 'h' to your preferred key
```

## 📞 **Support**

- **API Issues**: <support@humanizeai.pro>
- **App Issues**: Check troubleshooting section above
- **Permissions Help**: Follow accessibility setup guide

---

**🎉 Experience hassle-free, system-wide text humanization on macOS!**
