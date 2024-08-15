import tkinter as tk
import time
import threading
import winsound  # For sound notification (Windows)

# Initialize the stop flag and pause flag
stop_flag = False
pause_flag = False
remaining_seconds = 0

def countdown():
    global stop_flag, pause_flag, remaining_seconds
    while remaining_seconds and not stop_flag:
        if not pause_flag:
            mins, secs = divmod(remaining_seconds, 60)
            timer = f'{mins:02d}:{secs:02d}'
            timer_label.config(text=timer)
            root.update()
            time.sleep(1)
            remaining_seconds -= 1
        else:
            time.sleep(0.1)  # Sleep briefly to check pause_flag

    if not stop_flag:
        timer_label.config(text="Time's up!")
        winsound.Beep(1000, 1000)  # Play a sound notification

def start_timer():
    global stop_flag, pause_flag, remaining_seconds
    stop_flag = False
    pause_flag = False
    try:
        seconds = int(entry.get())
        if seconds > 0:
            remaining_seconds = seconds
            threading.Thread(target=countdown, daemon=True).start()
        else:
            timer_label.config(text="Enter a positive number!")
    except ValueError:
        timer_label.config(text="Invalid input!")

def end_timer():
    global stop_flag
    stop_flag = True
    timer_label.config(text="Stopped!")

def pause_timer():
    global pause_flag
    pause_flag = True

def resume_timer():
    global pause_flag
    pause_flag = False

def reset_timer():
    global stop_flag, pause_flag
    stop_flag = True
    pause_flag = False
    timer_label.config(text="00:00")
    entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Countdown Timer")
root.geometry("500x300")

# Create and place the timer label
timer_label = tk.Label(root, text="00:00", font=("Helvetica", 48))
timer_label.pack(pady=20)

# Create and place the entry widget for seconds input
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry_label = tk.Label(entry_frame, text="Enter seconds:", font=("Helvetica", 14))
entry_label.grid(row=0, column=0, padx=10)

entry = tk.Entry(entry_frame, font=("Helvetica", 24), width=10)
entry.grid(row=0, column=1, padx=10)

# Create and place the control buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start", command=start_timer, font=("Helvetica", 14))
start_button.grid(row=0, column=0, padx=10)

pause_button = tk.Button(button_frame, text="Pause", command=pause_timer, font=("Helvetica", 14))
pause_button.grid(row=0, column=1, padx=10)

resume_button = tk.Button(button_frame, text="Resume", command=resume_timer, font=("Helvetica", 14))
resume_button.grid(row=0, column=2, padx=10)

end_button = tk.Button(button_frame, text="Stop", command=end_timer, font=("Helvetica", 14))
end_button.grid(row=0, column=3, padx=10)

reset_button = tk.Button(button_frame, text="Reset", command=reset_timer, font=("Helvetica", 14))
reset_button.grid(row=0, column=4, padx=10)

# Run the main event loop
root.mainloop()
