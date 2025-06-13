#!/usr/bin/env python3
"""
Floating Humanize AI Text Processor for macOS
A system-wide floating app that works everywhere with accessibility permissions
"""

import requests
import time
import subprocess
import sys
import json
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from typing import Optional, Tuple
import os
import pynput
from pynput import keyboard
try:
    import AppKit
    from AppKit import NSApplication, NSApp, NSWindow, NSFloatingWindowLevel, NSScreen
except ImportError:
    print("Warning: AppKit not available - some floating features may not work")

class FloatingHumanizeApp:
    def __init__(self):
        self.api_key = "sk_ljx30mzi36a2nb8jlfo0pd"
        self.api_base_url = "https://api.humanizeai.pro/v1"
        self.is_processing = False
        self.hotkey_listener = None
        self.check_accessibility_permissions()
        self.setup_gui()
        self.setup_global_hotkey()
        
    def check_accessibility_permissions(self):
        """Check and request accessibility permissions"""
        try:
            # Test accessibility by trying to create a keyboard listener
            with pynput.keyboard.Listener(suppress=False) as test_listener:
                pass  # If this works, we have permissions
            print("✅ Accessibility permissions granted")
            
        except Exception as e:
            print(f"⚠️  Accessibility permission issue: {e}")
            self.request_accessibility_permission()
    
    def request_accessibility_permission(self):
        """Request accessibility permissions from user"""
        message = """🔐 Accessibility Permission Required

This app needs accessibility permissions to:
• Read selected text from any application
• Work system-wide with global hotkeys
• Replace text automatically

Please:
1. Go to System Preferences > Security & Privacy > Privacy > Accessibility
2. Click the lock and enter your password
3. Add this app (Python or Terminal) to the list
4. Restart this app

The app will continue running with limited functionality until permissions are granted."""
        
        print(message)
        
        result = messagebox.askyesno("Permission Required", 
                                   message + "\n\nOpen System Preferences now?")
        
        if result:
            subprocess.run(['open', '-b', 'com.apple.preference.security'])
        
    def setup_gui(self):
        """Setup the floating GUI interface"""
        self.root = tk.Tk()
        self.root.title("Humanize AI")
        self.root.geometry("320x220")
        self.root.resizable(False, False)
        
        # Make window truly floating and always on top
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.96)  # Slight transparency
        
        # Try to set floating window level (macOS specific)
        try:
            # Get the Tk window's NSWindow
            from tkinter import _tkinter
            window_id = self.root.winfo_id()
            # This will make it float above all other windows
            self.root.lift()
            self.root.call('wm', 'attributes', '.', '-topmost', '1')
        except Exception as e:
            print(f"Note: Advanced floating features not available: {e}")
        
        # Position window in top-right corner, accounting for multiple screens
        self.position_window()
        
        # Configure window styling
        self.root.configure(bg='#1e2329')
        
        # Main frame with modern styling
        main_frame = tk.Frame(self.root, bg='#2b2f36', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True, padx=8, pady=8)
        
        # Title with emoji
        title_label = tk.Label(main_frame, text="🤖 Humanize AI", 
                              font=("SF Pro Display", 16, "bold"),
                              bg='#2b2f36', fg='#ffffff')
        title_label.pack(pady=(0, 15))
        
        # Status display with better styling
        self.status_frame = tk.Frame(main_frame, bg='#2b2f36')
        self.status_frame.pack(fill='x', pady=5)
        
        self.status_indicator = tk.Label(self.status_frame, text="🟢", 
                                        font=("SF Pro Display", 12),
                                        bg='#2b2f36')
        self.status_indicator.pack(side='left')
        
        self.status_label = tk.Label(self.status_frame, text="Ready • Press ⌘⇧H", 
                                    font=("SF Pro Display", 11),
                                    bg='#2b2f36', fg='#4ade80')
        self.status_label.pack(side='left', padx=(5, 0))
        
        # Progress bar with modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Modern.Horizontal.TProgressbar",
                       background='#3b82f6',
                       troughcolor='#374151',
                       relief='flat',
                       borderwidth=0)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', 
                                       style="Modern.Horizontal.TProgressbar")
        
        # Main button with modern styling
        self.humanize_btn = tk.Button(main_frame, text="✨ Humanize Selected Text", 
                                     command=self.humanize_selected_text,
                                     font=("SF Pro Display", 12, "bold"),
                                     bg='#3b82f6', fg='white',
                                     relief='flat', padx=20, pady=12,
                                     cursor='hand2',
                                     activebackground='#2563eb',
                                     activeforeground='white')
        self.humanize_btn.pack(pady=15, fill='x')
        
        # Info section
        info_frame = tk.Frame(main_frame, bg='#2b2f36')
        info_frame.pack(fill='x', pady=5)
        
        hotkey_label = tk.Label(info_frame, text="🔥 Global Hotkey: ⌘⇧H", 
                               font=("SF Pro Display", 10),
                               bg='#2b2f36', fg='#9ca3af')
        hotkey_label.pack()
        
        works_label = tk.Label(info_frame, text="Works in any app, any desktop", 
                              font=("SF Pro Display", 9),
                              bg='#2b2f36', fg='#9ca3af')
        works_label.pack()
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#2b2f36')
        control_frame.pack(fill='x', pady=(15, 0))
        
        # Minimize button
        minimize_btn = tk.Button(control_frame, text="−", 
                                command=self.minimize_app,
                                font=("SF Pro Display", 14, "bold"),
                                bg='#ef4444', fg='white',
                                relief='flat', width=3, height=1,
                                cursor='hand2',
                                activebackground='#dc2626')
        minimize_btn.pack(side='right', padx=(5, 0))
        
        # Always on top toggle
        self.topmost_var = tk.BooleanVar(value=True)
        topmost_btn = tk.Checkbutton(control_frame, text="Stay on top",
                                    variable=self.topmost_var,
                                    command=self.toggle_topmost,
                                    font=("SF Pro Display", 9),
                                    bg='#2b2f36', fg='#9ca3af',
                                    selectcolor='#2b2f36',
                                    activebackground='#2b2f36',
                                    activeforeground='#9ca3af')
        topmost_btn.pack(side='left')
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_app)
        
        # Make window stick to all desktops/spaces
        self.make_window_sticky()
        
    def position_window(self):
        """Position window in top-right corner"""
        self.root.update_idletasks()  # Ensure geometry is calculated
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Position in top-right corner with some margin
        x_position = screen_width - 340
        y_position = 60
        
        self.root.geometry(f"320x220+{x_position}+{y_position}")
        
    def make_window_sticky(self):
        """Make window appear on all desktops/spaces (macOS)"""
        try:
            # This AppleScript makes the window sticky across all spaces
            script = f'''
            tell application "System Events"
                set theWindows to windows of application process "Python"
                repeat with theWindow in theWindows
                    if name of theWindow contains "Humanize AI" then
                        set value of attribute "AXFullScreen" of theWindow to false
                        set subrole of theWindow to "AXFloatingWindow"
                    end if
                end repeat
            end tell
            '''
            subprocess.run(['osascript', '-e', script], capture_output=True)
        except Exception as e:
            print(f"Note: Could not make window sticky: {e}")
        
    def toggle_topmost(self):
        """Toggle always on top behavior"""
        self.root.attributes('-topmost', self.topmost_var.get())
        
    def setup_global_hotkey(self):
        """Setup global hotkey (Cmd+Shift+H)"""
        def on_hotkey():
            if not self.is_processing:
                self.root.after(0, self.humanize_selected_text)
        
        try:
            # Set up global hotkey listener
            self.hotkey_listener = keyboard.GlobalHotKeys({
                '<cmd>+<shift>+h': on_hotkey
            })
            
            # Start the listener
            self.hotkey_listener.start()
            print("✅ Global hotkey (⌘⇧H) registered successfully")
            
        except Exception as e:
            print(f"⚠️  Could not register global hotkey: {e}")
            self.update_status("Hotkey unavailable", "#ef4444")
        
    def minimize_app(self):
        """Minimize app to dock"""
        self.root.withdraw()
        
        # Show notification
        self.show_notification("Humanize AI minimized", 
                              "Press ⌘⇧H to humanize text or click dock icon to restore")
        
        # Set up restoration check
        self.root.after(1000, self.check_for_restore)
    
    def check_for_restore(self):
        """Check if app should be restored"""
        try:
            if not self.root.winfo_viewable():
                # Check if we should restore (simplified - user can click dock icon)
                self.root.after(1000, self.check_for_restore)
        except:
            pass
    
    def show_notification(self, title: str, message: str):
        """Show macOS notification"""
        try:
            script = f'''
            display notification "{message}" with title "{title}" sound name "Ping"
            '''
            subprocess.run(['osascript', '-e', script], check=False)
        except:
            pass
    
    def get_selected_text(self) -> Optional[str]:
        """Get selected text from the currently active application"""
        try:
            # Store current clipboard
            original_clipboard = subprocess.run(['pbpaste'], 
                                              capture_output=True, text=True).stdout
            
            # Copy selected text
            script = '''
            tell application "System Events"
                keystroke "c" using command down
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True, timeout=5)
            
            # Wait for clipboard to update
            time.sleep(0.3)
            
            # Get new clipboard content
            result = subprocess.run(['pbpaste'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                selected_text = result.stdout.strip()
                
                # Restore original clipboard if no new text was selected
                if selected_text == original_clipboard:
                    self.update_status("No text selected", "#ef4444", "🔴")
                    return None
                    
                if selected_text and len(selected_text.split()) >= 5:
                    return selected_text
                else:
                    self.update_status("Select more text (5+ words)", "#ef4444", "⚠️")
                    return None
            else:
                self.update_status("Failed to get text", "#ef4444", "❌")
                return None
                
        except Exception as e:
            self.update_status(f"Error: {str(e)[:20]}...", "#ef4444", "❌")
            return None
    
    def set_selected_text(self, text: str) -> bool:
        """Replace selected text with humanized version"""
        try:
            # Set clipboard to new text
            subprocess.run(['pbcopy'], input=text, text=True, check=True)
            
            # Small delay to ensure clipboard is set
            time.sleep(0.1)
            
            # Paste the new text
            script = '''
            tell application "System Events"
                keystroke "v" using command down
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=5)
            
            return result.returncode == 0
            
        except Exception as e:
            self.update_status(f"Paste error", "#ef4444", "❌")
            return False
    
    def submit_humanization_task(self, text: str) -> Optional[str]:
        """Submit text to Humanize AI API"""
        try:
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            data = {'text': text}
            
            response = requests.post(f"{self.api_base_url}/", 
                                   headers=headers, 
                                   json=data, 
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('id')
            else:
                self.update_status(f"API Error: {response.status_code}", "#ef4444", "❌")
                return None
                
        except Exception as e:
            self.update_status(f"Network error", "#ef4444", "🌐")
            return None
    
    def get_humanization_result(self, task_id: str) -> Optional[Tuple[str, str]]:
        """Get humanization result from API"""
        try:
            headers = {'x-api-key': self.api_key}
            max_attempts = 30
            attempt = 0
            
            while attempt < max_attempts:
                response = requests.get(f"{self.api_base_url}/?id={task_id}", 
                                      headers=headers, 
                                      timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if 'humanized_text' in result:
                        return result.get('original_text'), result.get('humanized_text')
                    elif result.get('status') == 'processing':
                        progress_msg = f"Processing... {attempt + 1}/30"
                        self.update_status(progress_msg, "#f59e0b", "⏳")
                        time.sleep(2)
                        attempt += 1
                    else:
                        self.update_status("Task failed", "#ef4444", "❌")
                        return None
                else:
                    self.update_status(f"API Error: {response.status_code}", "#ef4444", "❌")
                    return None
            
            self.update_status("Timeout - try again", "#ef4444", "⏰")
            return None
            
        except Exception as e:
            self.update_status("Processing error", "#ef4444", "❌")
            return None
    
    def update_status(self, message: str, color: str = "#4ade80", indicator: str = "🟢"):
        """Update status label with indicator"""
        def update():
            self.status_label.config(text=message, fg=color)
            self.status_indicator.config(text=indicator)
        
        if threading.current_thread() is threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def toggle_ui_state(self, enabled: bool):
        """Enable/disable UI during processing"""
        def toggle():
            state = tk.NORMAL if enabled else tk.DISABLED
            self.humanize_btn.config(state=state)
            
            if enabled:
                self.progress.pack_forget()
                self.humanize_btn.config(text="✨ Humanize Selected Text")
            else:
                self.progress.pack(fill='x', pady=(5, 10), before=self.humanize_btn)
                self.progress.start(10)
                self.humanize_btn.config(text="🔄 Processing...")
        
        if threading.current_thread() is threading.main_thread():
            toggle()
        else:
            self.root.after(0, toggle)
    
    def humanize_selected_text(self):
        """Main function to humanize selected text"""
        if self.is_processing:
            return
            
        def process():
            try:
                self.is_processing = True
                self.toggle_ui_state(False)
                self.update_status("Getting text...", "#3b82f6", "📋")
                
                # Get selected text
                selected_text = self.get_selected_text()
                if not selected_text:
                    return
                
                # Check word count
                word_count = len(selected_text.split())
                if word_count < 5:
                    self.update_status(f"Need 5+ words (got {word_count})", "#ef4444", "⚠️")
                    return
                
                self.update_status(f"Humanizing {word_count} words...", "#3b82f6", "🤖")
                
                # Submit to API
                task_id = self.submit_humanization_task(selected_text)
                if not task_id:
                    return
                
                # Get result
                result = self.get_humanization_result(task_id)
                if not result:
                    return
                
                original_text, humanized_text = result
                
                self.update_status("Replacing text...", "#3b82f6", "📝")
                
                # Replace text
                if self.set_selected_text(humanized_text):
                    self.update_status("✅ Humanized & Pasted!", "#4ade80", "✅")
                    self.show_notification("Humanize AI", 
                                         f"Text successfully humanized! ({word_count} words)")
                    
                    # Show ready for copy hint
                    self.root.after(2000, lambda: self.update_status(
                        "💾 Ready to copy/paste again", "#4ade80", "💾"))
                else:
                    self.update_status("Replace failed", "#ef4444", "❌")
                
            except Exception as e:
                self.update_status("Error occurred", "#ef4444", "❌")
                print(f"Processing error: {e}")
            finally:
                self.is_processing = False
                self.toggle_ui_state(True)
                # Reset status after 5 seconds
                self.root.after(5000, lambda: self.update_status(
                    "Ready • Press ⌘⇧H", "#4ade80", "🟢"))
        
        # Run in background thread
        threading.Thread(target=process, daemon=True).start()
    
    def run(self):
        """Start the floating app"""
        try:
            # Show initial notification
            self.show_notification("🚀 Humanize AI Started", 
                                  "Floating app ready! Press ⌘⇧H anywhere to humanize text")
            
            print("✅ Floating Humanize AI app is running!")
            print("   • Press ⌘⇧H anywhere to humanize selected text")
            print("   • The app floats on all desktops and stays on top")
            print("   • Click minimize (-) to hide to dock")
            
            self.root.mainloop()
        except KeyboardInterrupt:
            if self.hotkey_listener:
                self.hotkey_listener.stop()
            self.root.quit()
        finally:
            if self.hotkey_listener:
                self.hotkey_listener.stop()

def main():
    """Main entry point"""
    print("🚀 Starting Floating Humanize AI Text Processor...")
    
    # Check if required modules are available
    try:
        import pynput
    except ImportError:
        print("❌ Missing required module 'pynput'")
        print("Please install it with: pip install pynput")
        sys.exit(1)
    
    app = FloatingHumanizeApp()
    app.run()

if __name__ == "__main__":
    main() 