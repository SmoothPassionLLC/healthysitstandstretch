import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import time
import os

paused = False
after_id = None
start_time = time.time()
remaining_time = 0
duration = 0

def reminder():
    global mode, start_time, duration
    start_time = time.time()
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
    start_next_mode()

def start_next_mode():
    global paused
    paused = False
    pause_button.config(text='Pause')
    schedule_next_reminder()

def update_label():
    label.config(text=f'Current mode: {mode}')

def schedule_next_reminder():
    global after_id, start_time, remaining_time, duration

    start_time = time.time()

    if mode == 'sit':
        duration = sit_duration
    elif mode == 'stand':
        duration = stand_duration
    else:
        duration = stretch_duration

    if remaining_time == 0:
        after_id = root.after(duration * 60 * 1000, reminder)
    else:
        after_id = root.after(remaining_time, reminder)
        remaining_time = 0

def reset_app():
    global mode, stats
    mode = 'sit'
    stats = {'sit': 0, 'stand': 0, 'stretch': 0}
    update_label()
    schedule_next_reminder()

def pause_app():
    global paused, after_id, start_time, remaining_time, duration
    paused = not paused
    pause_button.config(text='Resume' if paused else 'Pause')

    if paused and after_id is not None:
        elapsed_time = (time.time() - start_time) * 1000
        remaining_time = int(duration * 60 * 1000 - elapsed_time)  # Convert to int
        root.after_cancel(after_id)
    elif not paused:
        start_next_mode()

def load_previous_stats():
    if os.path.exists('stats.json'):
        with open('stats.json', 'r') as f:
            return json.load(f)
    else:
        default_stats = {'sit': 0, 'stand': 0, 'stretch': 0}
        with open('stats.json', 'w') as f:
            json.dump(default_stats, f)
        return default_stats

def save_stats():
    with open('stats.json', 'w') as f:
        json.dump(stats, f)

root = tk.Tk()
root.title('Sit-Stand-Stretch Reminder')

mode = 'sit'
sit_duration = simpledialog.askinteger('Sit duration', 'How long do you want to sit (minutes)?', initialvalue=30)
stand_duration = simpledialog.askinteger('Stand duration', 'How long do you want to stand (minutes)?', initialvalue=30)
stretch_duration = simpledialog.askinteger('Stretch duration', 'How long do you want to stretch (minutes)?', initialvalue=5)

stats = {'sit': 0, 'stand': 0, 'stretch': 0}
prev_stats = load_previous_stats()
messagebox.showinfo('Previous stats', f"Yesterday's stats:\nSit: {prev_stats['sit']} minutes\nStand: {prev_stats['stand']} minutes\nStretch: {prev_stats['stretch']} minutes")

label = tk.Label(root, text=f'Current mode: {mode}')
label.pack(pady=10)

button = tk.Button(root, text='Switch Mode', command=reminder)
button.pack(pady=10)

pause_button = tk.Button(root, text='Pause', command=pause_app)
pause_button.pack(pady=10)

reset_button = tk.Button(root, text='Reset', command=reset_app)
reset_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", save_stats)
schedule_next_reminder()
root.mainloop()
