import tkinter as tk
from tkinter import messagebox
import time

# Define the reminder function
def reminder():
    global mode
    if mode == 'sit':
        mode = 'stand'
        messagebox.showinfo('Time to stand', 'Please stand up and press the button to confirm.')
    elif mode == 'stand':
        mode = 'stretch'
        messagebox.showinfo('Time to stretch', 'Please take a break to stretch and press the button to confirm.')
    else:
        mode = 'sit'
        messagebox.showinfo('Time to sit', 'Please sit down and press the button to confirm.')
    update_label()

# Update the label text
def update_label():
    label.config(text=f'Current mode: {mode}')

# Create the main window
root = tk.Tk()
root.title('Sit-Stand-Stretch Reminder')

# Initialize the mode
mode = 'sit'

# Create the label and button
label = tk.Label(root, text=f'Current mode: {mode}')
label.pack(pady=10)

button = tk.Button(root, text='Switch Mode', command=reminder)
button.pack(pady=10)

# Start the main loop
root.mainloop()
