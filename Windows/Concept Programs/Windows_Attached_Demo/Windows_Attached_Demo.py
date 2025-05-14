# Windows Attach Demo
# Copyright (C) 2024, Sourceduty - All Rights Reserved.

import tkinter as tk

# Function to create the first window
def create_window1():
    window1 = tk.Tk()
    window1.geometry("500x250+100+100")  # Set size to 500x250
    window1.title("Windows Attach Demo")

    # Dark Mode - Window 1
    window1.configure(bg='#2e2e2e')  # Dark background
    label1 = tk.Label(window1, text="This is Window 1", fg="white", bg="#2e2e2e")
    label1.pack(padx=20, pady=20)

    # Buttons with larger size and different colors, center-aligned
    attach_button = tk.Button(window1, text="Attach", command=lambda: attach_window(window2))
    attach_button.config(bg="#4CAF50", fg="white", height=2, width=15)
    detach_button = tk.Button(window1, text="Detach", command=lambda: detach_window(window2))
    detach_button.config(bg="#F44336", fg="white", height=2, width=15)

    # Pack buttons centered horizontally
    attach_button.pack(side="top", pady=10)
    detach_button.pack(side="top", pady=10)

    # Bind the configure event to detect when window1 is moved
    window1.bind("<Configure>", lambda event: update_window2_position(window1, window2))

    return window1

# Function to create the second window
def create_window2():
    window2 = tk.Toplevel()  # Use Toplevel for the second window
    window2.geometry("500x250+620+100")  # Set size to 500x250
    window2.title("Windows Attach Demo")

    # Dark Mode - Window 2
    window2.configure(bg='#2e2e2e')  # Dark background
    label2 = tk.Label(window2, text="This is Window 2", fg="white", bg="#2e2e2e")
    label2.pack(padx=20, pady=20)

    # Create a Text widget for the description in Window 2
    description = tk.Text(window2, fg="white", bg="#2e2e2e", wrap="word", height=6, width=50, bd=0, font=("Helvetica", 10))
    description.insert(tk.END, "This program demonstrates how two windows can be attached and detached.\n"
                               "When attached, Window 2 follows Window 1's movement. When detached, "
                               "Window 2 can move independently.\n\nPress Attach to make Window 2 follow Window 1.\n"
                               "Press Detach to allow Window 2 to move freely.")
    description.config(state=tk.DISABLED)  # Disable editing, just for display
    description.pack(padx=20, pady=10)

    return window2

# Function to attach window 2 to window 1
def attach_window(window2):
    window2.geometry("500x250+620+100")  # Attach by setting its position next to window 1
    window2.bind("<Configure>", lambda event: update_window2_position(window1, window2))

# Function to detach window 2
def detach_window(window2):
    window2.geometry("500x250+1000+100")  # Detach by moving it far from window 1
    window2.unbind("<Configure>")  # Unbind the event, allowing the window to move freely

# Function to update the position of window 2 when window 1 is moved
def update_window2_position(window1, window2):
    if window2.winfo_rootx() == 1000:  # Check if window2 has been detached
        return  # Don't update window2 position if it's detached
    # Get the current position of window1
    x1, y1 = window1.winfo_rootx(), window1.winfo_rooty()
    # Attach window2 to the right side of window1
    window2.geometry(f"500x250+{x1 + 500}+{y1}")

# Create the main window
root = tk.Tk()  # The main window needs to exist first
root.withdraw()  # Hide the root window (it won't be visible)

# Create the two separate windows
window1 = create_window1()
window2 = create_window2()

# Start the Tkinter event loop
root.mainloop()
