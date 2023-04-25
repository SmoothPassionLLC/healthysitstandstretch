# Sit-Stand-Stretch Reminder

This application helps you maintain a healthy balance between sitting, standing, and stretching throughout the day by providing reminders to switch between these modes at user-defined intervals.

## Features

- Customizable sit, stand, and stretch durations
- Pause and resume functionality
- Reset the app
- Saves previous day's stats in a JSON file

## How to Use

1. Run the Python script or the provided .exe file.
2. Enter the desired duration (in minutes) for each mode sitting, standing, and stretching.
3. The application will start with the sitting mode by default and display the current mode.
4. Press the "Switch Mode" button to manually switch between the modes when you're ready.
5. The application will also automatically switch between the modes based on the configured durations.
6. You can pause the timer by clicking the "Pause" button, which will then display "Resume." Click "Resume" to continue the timer.
7. To reset the app, click the "Reset" button. This will reset all the modes and start from the sitting mode again.
8. When you close the application, it saves the day's stats in a JSON file, which will be loaded and displayed the next time you open the app.

## Requirements

- Python 3.6 or later
- tkinter library

## Code

The application is built using the tkinter library for the graphical user interface. It consists of several functions to manage and control the app's behavior, such as `reminder()`, `start_next_mode()`, `update_label()`, `schedule_next_reminder()`, `reset_app()`, `pause_app()`, `load_previous_stats()`, and `save_stats()`. These functions handle the app's logic and interface elements, such as labels, buttons, and timers.
