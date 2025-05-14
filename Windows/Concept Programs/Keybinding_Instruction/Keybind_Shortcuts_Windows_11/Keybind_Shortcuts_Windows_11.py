# Keybind_Shortcuts_Windows_11

# ⌨ Bind the default Windows 11 shortcut list to your keyboard.

# Displays a window with a list of Windows 11 keyboard shortcuts when CRTL + 1 are pressed.

# Copyright (C) 2023, Sourceduty - All Rights Reserved.
# THE CONTENTS OF THIS PROJECT ARE PROPRIETARY.

import tkinter as tk
from tkinter import Text, Scrollbar
import keyboard

# Function to display the shortcuts
def display_shortcuts():
    window = tk.Toplevel()
    window.title("Windows 11 Shortcuts")
    
    shortcuts = (
        "Win + A: Open Action Center.",
        "Win + C: Open Chat from Microsoft Teams.",
        "Win + D: Show or hide the desktop.",
        "Win + E: Open File Explorer.",
        "Win + I: Open Settings.",
        "Win + L: Lock your PC.",
        "Win + M: Minimize all windows.",
        "Win + R: Open the Run dialog box.",
        "Win + S: Open Search.",
        "Win + X: Open the Quick Link menu (also right-clicking the Start button does this).",
        "Win + Tab: Open Task View.",
        "Win + ,: Peek at the desktop.",
        "Win + . or Win + ;: Open the emoji panel.",
        "Win + Shift + S: Take a screenshot using Snip & Sketch.",
        "Win + H: Open voice typing.",
        "Win + Space: Switch input language and keyboard layout."
    )
    
    text_widget = Text(window, wrap=tk.WORD, height=20, width=50)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    for shortcut in shortcuts:
        text_widget.insert(tk.END, shortcut + "\n")
    
    text_widget.config(state=tk.DISABLED)
    
    scrollbar = Scrollbar(window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

# Create the main window and hide it
root = tk.Tk()
root.withdraw()

# Set the hotkey to display the shortcuts
keyboard.add_hotkey('ctrl+1', display_shortcuts)

# Start the main loop
root.mainloop()
