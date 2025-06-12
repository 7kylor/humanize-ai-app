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
import AppKit
from AppKit import NSApplication, NSApp, NSWindow, NSFloatingWindowLevel

class FloatingHumanizeApp:
    def __init__(self):
        self.api_key = "sk_ljx30mzi36a2nb8jlfo0pd"
        self.api_base_url = "https://api.humanizeai.pro/v1"
        self.is_processing = False
        self.check_accessibility_permissions()
        self.setup_gui()
        self.setup_global_hotkey()
        
    def check_accessibility_permissions(self):
        """Check and request accessibility permissions"""
        try:
            # Test accessibility by trying to get accessibility info
            script = '''
            tell application "System Events"
                try
                    set frontmostApp to name of first application process whose frontmost is true
                    return frontmostApp
                on error
                    return "NO_ACCESS"
                end try
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=5)
            
            if "NO_ACCESS" in result.stdout or result.returncode != 0:
                self.request_accessibility_permission()
            
        except Exception as e:
            print(f"Error checking accessibility: {e}")
            self.request_accessibility_permission()
    
    def request_accessibility_permission(self):
        """Request accessibility permissions from user"""
        message = """
🔐 Accessibility Permission Required

This app needs accessibility permissions to:
• Read selected text from any application
• Work system-wide with global hotkeys
• Replace text automatically

Please:
1. Click 'Open System Preferences'
2. Go to Security & Privacy → Privacy → Accessibility
3. Click the lock and enter your password
4. Add this app (Python or Terminal) to the list
5. Restart this app

Without these permissions, the app cannot function properly.
        """
        
        result = messagebox.askyesno("Permission Required", 
                                   message + "\n\nOpen System Preferences now?")
        
        if result:
            subprocess.run(['open', '-b', 'com.apple.preference.security'])
        
        # Exit gracefully if permissions not granted
        sys.exit(0)
        
    def setup_gui(self):
        """Setup the floating GUI interface"""
        self.root = tk.Tk()
        self.root.title("Humanize AI")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        # Make window floating and always on top
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)  # Slight transparency
        
        # Position window in top-right corner
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - 320
        self.root.geometry(f"300x200+{x_position}+20")
        
        # Configure window to be floating
        self.root.configure(bg='#2c3e50')
        
        # Main frame with rounded appearance
        main_frame = tk.Frame(self.root, bg='#34495e', padx=15, pady=15)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Title
        title_label = tk.Label(main_frame, text="🤖 Humanize AI", 
                              font=("SF Pro Display", 14, "bold"),
                              bg='#34495e', fg='white')
        title_label.pack(pady=(0, 10))
        
        # Status display
        self.status_frame = tk.Frame(main_frame, bg='#34495e')
        self.status_frame.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="Ready • Press ⌘⇧H", 
                                    font=("SF Pro Display", 10),
                                    bg='#34495e', fg='#1abc9c')
        self.status_label.pack()
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        self.progress.pack_forget()  # Hide initially
        
        # Main button
        self.humanize_btn = tk.Button(main_frame, text="Humanize Selected Text", 
                                     command=self.humanize_selected_text,
                                     font=("SF Pro Display", 11, "bold"),
                                     bg='#3498db', fg='white',
                                     relief='flat', padx=15, pady=8,
                                     cursor='hand2')
        self.humanize_btn.pack(pady=10, fill='x')
        
        # Info labels
        hotkey_label = tk.Label(main_frame, text="Global Hotkey: ⌘⇧H", 
                               font=("SF Pro Display", 9),
                               bg='#34495e', fg='#95a5a6')
        hotkey_label.pack(pady=2)
        
        works_label = tk.Label(main_frame, text="Works in any app", 
                              font=("SF Pro Display", 8),
                              bg='#34495e', fg='#95a5a6')
        works_label.pack()
        
        # Minimize button
        minimize_btn = tk.Button(main_frame, text="−", 
                                command=self.minimize_app,
                                font=("SF Pro Display", 12, "bold"),
                                bg='#e74c3c', fg='white',
                                relief='flat', width=3,
                                cursor='hand2')
        minimize_btn.pack(side='bottom', anchor='se', pady=(10, 0))
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_app)
        
    def setup_global_hotkey(self):
        """Setup global hotkey (Cmd+Shift+H)"""
        def on_hotkey():
            if not self.is_processing:
                self.humanize_selected_text()
        
        # Set up global hotkey listener
        def hotkey_listener():
            with keyboard.GlobalHotKeys({
                '<cmd>+<shift>+h': on_hotkey
            }):
                # Keep the listener running
                keyboard.Listener().join()
        
        # Start hotkey listener in background thread
        hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
        hotkey_thread.start()
        
    def minimize_app(self):
        """Minimize app to system tray equivalent"""
        self.root.withdraw()
        
        # Show notification
        self.show_notification("Humanize AI minimized", 
                              "Press ⌘⇧H to humanize text or click dock icon to restore")
        
        # Set up dock icon click handler to restore
        def restore_from_dock():
            self.root.after(1000, self.check_dock_click)
        
        threading.Thread(target=restore_from_dock, daemon=True).start()
    
    def check_dock_click(self):
        """Check if app was clicked in dock to restore"""
        try:
            # Check if window should be restored (simplified approach)
            if not self.root.winfo_viewable():
                # Set timer to check again
                self.root.after(1000, self.check_dock_click)
        except:
            pass
    
    def show_notification(self, title: str, message: str):
        """Show macOS notification"""
        try:
            script = f'''
            display notification "{message}" with title "{title}"
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
            time.sleep(0.2)
            
            # Get new clipboard content
            result = subprocess.run(['pbpaste'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                selected_text = result.stdout
                
                # Restore original clipboard if no new text was selected
                if selected_text == original_clipboard:
                    return None
                    
                if selected_text and len(selected_text.split()) >= 5:
                    return selected_text
                else:
                    self.update_status("Select more text (30+ words)", "#e74c3c")
                    return None
            else:
                self.update_status("Failed to get text", "#e74c3c")
                return None
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "#e74c3c")
            return None
    
    def set_selected_text(self, text: str) -> bool:
        """Replace selected text with humanized version"""
        try:
            # Set clipboard to new text
            subprocess.run(['pbcopy'], input=text, text=True, check=True)
            
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
            self.update_status(f"Paste error: {str(e)}", "#e74c3c")
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
                self.update_status(f"API Error: {response.status_code}", "#e74c3c")
                return None
                
        except Exception as e:
            self.update_status(f"Network error", "#e74c3c")
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
                        self.update_status(f"Processing... {attempt + 1}/30", "#f39c12")
                        time.sleep(2)
                        attempt += 1
                    else:
                        self.update_status("Task failed", "#e74c3c")
                        return None
                else:
                    self.update_status(f"API Error: {response.status_code}", "#e74c3c")
                    return None
            
            self.update_status("Timeout - try again", "#e74c3c")
            return None
            
        except Exception as e:
            self.update_status("Processing error", "#e74c3c")
            return None
    
    def update_status(self, message: str, color: str = "#1abc9c"):
        """Update status label"""
        def update():
            self.status_label.config(text=message, fg=color)
        
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
            else:
                self.progress.pack(fill='x', pady=5, before=self.humanize_btn)
                self.progress.start(10)
        
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
                self.update_status("Getting text...", "#3498db")
                
                # Get selected text
                selected_text = self.get_selected_text()
                if not selected_text:
                    return
                
                # Check word count
                word_count = len(selected_text.split())
                if word_count < 30:
                    self.update_status(f"Need 30+ words ({word_count})", "#e74c3c")
                    return
                
                self.update_status(f"Humanizing {word_count} words...", "#3498db")
                
                # Submit to API
                task_id = self.submit_humanization_task(selected_text)
                if not task_id:
                    return
                
                # Get result
                result = self.get_humanization_result(task_id)
                if not result:
                    return
                
                original_text, humanized_text = result
                
                self.update_status("Replacing text...", "#3498db")
                
                # Replace text
                if self.set_selected_text(humanized_text):
                    self.update_status("✅ Humanized!", "#1abc9c")
                    self.show_notification("Humanize AI", "Text successfully humanized!")
                else:
                    self.update_status("Replace failed", "#e74c3c")
                
            except Exception as e:
                self.update_status("Error occurred", "#e74c3c")
            finally:
                self.is_processing = False
                self.toggle_ui_state(True)
                # Reset status after 3 seconds
                self.root.after(3000, lambda: self.update_status("Ready • Press ⌘⇧H", "#1abc9c"))
        
        # Run in background thread
        threading.Thread(target=process, daemon=True).start()
    
    def run(self):
        """Start the floating app"""
        try:
            # Show initial notification
            self.show_notification("Humanize AI Started", 
                                  "Floating app ready! Press ⌘⇧H anywhere to humanize text")
            
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

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