import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

paused = False
after_id = None

# Define the reminder function
def reminder():
    global mode
    if mode == 'sit':
        stats['sit'] += sit_duration
        mode = 'stand'
        messagebox.showinfo('Time to stand', 'Please stand and press the button to confirm.')
    elif mode == 'stand':
        stats['stand'] += stand_duration
        mode = 'stretch'
        messagebox.showinfo('Time to stretch', 'Please take a break to stretch and press the button to confirm.')
    else:
        stats['stretch'] += stretch_duration
        mode = 'sit'
        messagebox.showinfo('Time to sit', 'Please sit and press the button to confirm.')
    update_label()
    schedule_next_reminder()

# Update the label text
def update_label():
    label.config(text=f'Current mode: {mode}')

# Schedule the next reminder
def schedule_next_reminder():
    if mode == 'sit':
        root.after(sit_duration * 60 * 1000, reminder)
    elif mode == 'stand':
        root.after(stand_duration * 60 * 1000, reminder)
    else:
        root.after(stretch_duration * 60 * 1000, reminder)

# Reset the app
def reset_app():
    global mode, stats
    mode = 'sit'
    stats = {'sit': 0, 'stand': 0, 'stretch': 0}
    update_label()
    schedule_next_reminder()

# Pause the app
def pause_app():
    global paused, after_id
    paused = not paused
    pause_button.config(text='Resume' if paused else 'Pause')
    if paused and after_id is not None:
        root.after_cancel(after_id)
    else:
        schedule_next_reminder()

# Load stats from the previous day
def load_previous_stats():
    if os.path.exists('stats.json'):
        with open('stats.json', 'r') as f:
            return json.load(f)
    else:
        default_stats = {'sit': 0, 'stand': 0, 'stretch': 0}
        with open('stats.json', 'w') as f:
            json.dump(default_stats, f)
        return default_stats


# Save stats at the end of the day
def save_stats():
    with open('stats.json', 'w') as f:
        json.dump(stats, f)

# Create the main window
root = tk.Tk()
root.title('Sit-Stand-Stretch Reminder')

# Initialize the mode and durations
mode = 'sit'
sit_duration = simpledialog.askinteger('Sit duration', 'How long do you want to sit (minutes)?', initialvalue=30)
stand_duration = simpledialog.askinteger('Stand duration', 'How long do you want to stand (minutes)?', initialvalue=30)
stretch_duration = simpledialog.askinteger('Stretch duration', 'How long do you want to stretch (minutes)?', initialvalue=5)

# Initialize the stats
stats = {'sit': 0, 'stand': 0, 'stretch': 0}
prev_stats = load_previous_stats()
messagebox.showinfo('Previous stats', f"Yesterday's stats:\nSit: {prev_stats['sit']} minutes\nStand: {prev_stats['stand']} minutes\nStretch: {prev_stats['stretch']} minutes")

# Create the label and buttons
label = tk.Label(root, text=f'Current mode: {mode}')
label.pack(pady=10)

button = tk.Button(root, text='Switch Mode', command=reminder)
button.pack(pady=10)

pause_button = tk.Button(root, text='Pause', command=pause_app)
pause_button.pack(pady=10)

reset_button = tk.Button(root, text='Reset', command=reset_app)
reset_button.pack(pady=10)

# Start the app
root.protocol("WM_DELETE_WINDOW", save_stats)
schedule_next_reminder()
root.mainloop()
