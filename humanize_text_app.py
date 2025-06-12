#!/usr/bin/env python3
"""
Humanize AI Text Processor for macOS
A fast and reliable app to humanize selected text in any macOS application (especially MS Word)
"""

import os
import requests
import time
import subprocess
import sys
import json
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from typing import Optional, Tuple

class HumanizeAIApp:
    def __init__(self):
        self.api_key = os.getenv("HUMANIZE_API_KEY")
        self.api_base_url = os.getenv("HUMANIZE_API_BASE_URL")
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Humanize AI - Text Processor")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Humanize AI Text Processor", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, text="1. Select text in any app (Word, Pages, etc.)\n2. Click 'Humanize Selected Text'\n3. Text will be automatically replaced",
                                justify=tk.CENTER, font=("Arial", 10))
        instructions.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Main button
        self.humanize_btn = ttk.Button(main_frame, text="🤖 Humanize Selected Text", 
                                      command=self.humanize_selected_text,
                                      style='Accent.TButton')
        self.humanize_btn.grid(row=2, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to humanize text", 
                                     font=("Arial", 9), foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Keyboard shortcut info
        shortcut_label = ttk.Label(main_frame, text="💡 Tip: Use Cmd+Shift+H for quick access", 
                                  font=("Arial", 8), foreground="gray")
        shortcut_label.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        # Bind keyboard shortcut
        self.root.bind('<Command-Shift-h>', lambda e: self.humanize_selected_text())
        self.root.bind('<Command-Shift-H>', lambda e: self.humanize_selected_text())
        
    def get_selected_text(self) -> Optional[str]:
        """Get selected text from the currently active application using AppleScript"""
        try:
            # AppleScript to get selected text from any application
            script = '''
            tell application "System Events"
                set activeApp to name of first application process whose frontmost is true
            end tell
            
            -- Copy selected text to clipboard
            tell application "System Events"
                keystroke "c" using command down
            end tell
            
            delay 0.1
            
            -- Get clipboard content
            return the clipboard
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                selected_text = result.stdout.strip()
                if selected_text and len(selected_text.split()) >= 5:  # Minimum 5 words
                    return selected_text
                else:
                    self.update_status("Please select more text (at least 30 words for API)", "orange")
                    return None
            else:
                self.update_status("Failed to get selected text", "red")
                return None
                
        except Exception as e:
            self.update_status(f"Error getting text: {str(e)}", "red")
            return None
    
    def set_selected_text(self, text: str) -> bool:
        """Replace selected text with humanized version using AppleScript"""
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
            self.update_status(f"Error setting text: {str(e)}", "red")
            return False
    
    def submit_humanization_task(self, text: str) -> Optional[str]:
        """Submit text to Humanize AI API"""
        try:
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            data = {
                'text': text
            }
            
            response = requests.post(f"{self.api_base_url}/", 
                                   headers=headers, 
                                   json=data, 
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('id')  # Return task ID
            else:
                self.update_status(f"API Error: {response.status_code}", "red")
                return None
                
        except Exception as e:
            self.update_status(f"Network error: {str(e)}", "red")
            return None
    
    def get_humanization_result(self, task_id: str) -> Optional[Tuple[str, str]]:
        """Get humanization result from API"""
        try:
            headers = {
                'x-api-key': self.api_key
            }
            
            max_attempts = 30  # 30 attempts with 2-second intervals = 1 minute max
            attempt = 0
            
            while attempt < max_attempts:
                response = requests.get(f"{self.api_base_url}/?id={task_id}", 
                                      headers=headers, 
                                      timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if 'humanized_text' in result:
                        # Task completed successfully
                        return result.get('original_text'), result.get('humanized_text')
                    elif result.get('status') == 'processing':
                        # Still processing, wait and try again
                        self.update_status(f"Processing... ({attempt + 1}/30)", "blue")
                        time.sleep(2)
                        attempt += 1
                    else:
                        # Task failed
                        self.update_status(f"Task failed: {result.get('error', 'Unknown error')}", "red")
                        return None
                else:
                    self.update_status(f"API Error: {response.status_code}", "red")
                    return None
            
            # Timeout
            self.update_status("Processing timeout - please try again", "red")
            return None
            
        except Exception as e:
            self.update_status(f"Error getting result: {str(e)}", "red")
            return None
    
    def update_status(self, message: str, color: str = "black"):
        """Update status label"""
        def update():
            self.status_label.config(text=message, foreground=color)
        
        if threading.current_thread() is threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def toggle_ui_state(self, enabled: bool):
        """Enable/disable UI elements during processing"""
        def toggle():
            state = tk.NORMAL if enabled else tk.DISABLED
            self.humanize_btn.config(state=state)
            
            if enabled:
                self.progress.stop()
            else:
                self.progress.start(10)
        
        if threading.current_thread() is threading.main_thread():
            toggle()
        else:
            self.root.after(0, toggle)
    
    def humanize_selected_text(self):
        """Main function to humanize selected text"""
        def process():
            try:
                self.toggle_ui_state(False)
                self.update_status("Getting selected text...", "blue")
                
                # Get selected text
                selected_text = self.get_selected_text()
                if not selected_text:
                    return
                
                # Check minimum word count (API requires 30+ words)
                word_count = len(selected_text.split())
                if word_count < 30:
                    self.update_status(f"Text too short ({word_count} words). Need 30+ words.", "orange")
                    return
                
                self.update_status(f"Submitting {word_count} words for humanization...", "blue")
                
                # Submit to API
                task_id = self.submit_humanization_task(selected_text)
                if not task_id:
                    return
                
                self.update_status("Waiting for AI processing...", "blue")
                
                # Get result
                result = self.get_humanization_result(task_id)
                if not result:
                    return
                
                original_text, humanized_text = result
                
                self.update_status("Replacing text...", "blue")
                
                # Replace selected text
                if self.set_selected_text(humanized_text):
                    self.update_status("✅ Text successfully humanized!", "green")
                else:
                    self.update_status("Failed to replace text", "red")
                
            except Exception as e:
                self.update_status(f"Unexpected error: {str(e)}", "red")
            finally:
                self.toggle_ui_state(True)
        
        # Run in background thread to keep UI responsive
        threading.Thread(target=process, daemon=True).start()
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

def main():
    """Main entry point"""
    print("Starting Humanize AI Text Processor...")
    app = HumanizeAIApp()
    app.run()

if __name__ == "__main__":
    main() 