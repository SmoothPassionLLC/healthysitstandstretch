#<iframe src="http://your-flask-app-url.com" width="100%" height="600"></iframe>
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=8080)
#flask program
import json
import time
import os
from flask import Flask, render_template, request

app = Flask(__name__)

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
        # Replace messagebox.showinfo with code that displays a message to the user
        return render_template('stand.html')
    elif mode == 'stand':
        stats['stand'] += stand_duration
        mode = 'stretch'
        # Replace messagebox.showinfo with code that displays a message to the user
        return render_template('stretch.html')
    else:
        stats['stretch'] += stretch_duration
        mode = 'sit'
        # Replace messagebox.showinfo with code that displays a message to the user
        return render_template('sit.html')
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
        after_id = app.after(duration * 60 * 1000, reminder)
    else:
        after_id = app.after(remaining_time, reminder)
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
    # Replace pause_button.config with code that updates the button text in the web page
    if paused and after_id is not None:
        elapsed_time = (time.time() - start_time) * 1000
        remaining_time = int(duration * 60 * 1000 - elapsed_time)  # Convert to int
        app.after_cancel(after_id)
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

# Define the routes and views for the web application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stand')
def stand():
    return render_template('stand.html')

@app.route('/stretch')
def stretch():
    return render_template('stretch.html')

@app.route('/sit')
def sit():
    return render_template('sit.html')

@app.route('/pause')
def pause():
    pause_app()
    return 'OK'

@app.route('/reset')
def reset():
    reset_app()
    return 'OK'

# Initialize the app
if __name__ == '__main__':
    mode = 'sit'
    sit_duration = request.form.get('sit_duration') or 30
    stand_duration = request.form.get('stand_duration') or 30
    stretch_duration = request.form.get('stretch_duration') or 5

    stats = {'sit': 0, 'stand': 0, 'stretch': 0}
    prev_stats = load_previous_stats()
    # Replace messagebox.showinfo with code that displays a message to the user
    return render_template('previous_stats.html', prev_stats=prev_stats)

    app.run()
