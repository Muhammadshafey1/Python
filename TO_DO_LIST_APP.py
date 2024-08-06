import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
import datetime

# Function to add a task
def add_task():
    task = entry_task.get()
    priority = combo_priority.get()
    due_date = cal_due_date.get_date()

    if not task or not priority:
        messagebox.showwarning("Warning", "Task and Priority are required.")
        return

    task_info = f"{task} | Priority: {priority} | Due: {due_date.strftime('%Y-%m-%d')}"
    listbox_tasks.insert(tk.END, task_info)
    clear_task_entry()

def clear_task_entry():
    entry_task.delete(0, tk.END)
    combo_priority.set('Low')
    cal_due_date.set_date(datetime.date.today())

# Function to delete a selected task
def delete_task():
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(selected_task_index)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

# Function to edit a selected task
def edit_task():
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        current_task = listbox_tasks.get(selected_task_index)
        task, priority, due_date = parse_task_info(current_task)

        new_task = simpledialog.askstring("Edit Task", "Enter new task:", initialvalue=task)
        if new_task:
            listbox_tasks.delete(selected_task_index)
            new_task_info = f"{new_task} | Priority: {priority} | Due: {due_date}"
            listbox_tasks.insert(selected_task_index, new_task_info)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to edit.")

# Function to mark a task as completed
def mark_completed():
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        task = listbox_tasks.get(selected_task_index)
        listbox_tasks.delete(selected_task_index)
        listbox_tasks.insert(tk.END, task, {'bg': 'darkgreen', 'fg': 'gray', 'font': ('Arial', 12, 'italic')})
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to mark as completed.")

# Function to save tasks to a file
def save_tasks():
    with open('tasks.txt', 'w') as file:
        for task in listbox_tasks.get(0, tk.END):
            file.write(task + '\n')
    messagebox.showinfo("Info", "Tasks saved to tasks.txt")

# Function to load tasks from a file
def load_tasks():
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
            listbox_tasks.delete(0, tk.END)
            for task in tasks:
                listbox_tasks.insert(tk.END, task.strip())
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved tasks found.")

# Function to clear all tasks
def clear_tasks():
    listbox_tasks.delete(0, tk.END)

# Function to search for tasks
def search_tasks():
    query = entry_search.get().lower()
    for i in range(listbox_tasks.size()):
        task = listbox_tasks.get(i).lower()
        listbox_tasks.itemconfig(i, {'bg': 'black', 'fg': 'white'})
        if query in task:
            listbox_tasks.itemconfig(i, {'bg': 'yellow', 'fg': 'black'})

# Function to parse task info
def parse_task_info(task_info):
    parts = task_info.split(" | ")
    task = parts[0]
    priority = parts[1].split(": ")[1]
    due_date = parts[2].split(": ")[1]
    return task, priority, due_date

# Function to sort tasks by priority
def sort_tasks_by_priority():
    tasks = listbox_tasks.get(0, tk.END)
    tasks_sorted = sorted(tasks, key=lambda x: x.split(" | ")[1].split(": ")[1])
    listbox_tasks.delete(0, tk.END)
    for task in tasks_sorted:
        listbox_tasks.insert(tk.END, task)

# Function to sort tasks by due date
def sort_tasks_by_due_date():
    tasks = listbox_tasks.get(0, tk.END)
    tasks_sorted = sorted(tasks, key=lambda x: datetime.datetime.strptime(x.split(" | ")[2].split(": ")[1], '%Y-%m-%d'))
    listbox_tasks.delete(0, tk.END)
    for task in tasks_sorted:
        listbox_tasks.insert(tk.END, task)

# Function to filter completed tasks
def filter_completed_tasks():
    tasks = listbox_tasks.get(0, tk.END)
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        if 'completed' in task.lower():
            listbox_tasks.insert(tk.END, task)

# Function to filter incomplete tasks
def filter_incomplete_tasks():
    tasks = listbox_tasks.get(0, tk.END)
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        if 'completed' not in task.lower():
            listbox_tasks.insert(tk.END, task)

# Function to manage tasks
def manage_tasks():
    manage_window = tk.Toplevel(root)
    manage_window.title("Manage Tasks")
    manage_window.configure(bg='black')

    button_sort_priority = tk.Button(manage_window, text="Sort by Priority", command=sort_tasks_by_priority, bg='#1e1e1e', fg='white')
    button_sort_priority.pack(pady=5)

    button_sort_due_date = tk.Button(manage_window, text="Sort by Due Date", command=sort_tasks_by_due_date, bg='#1e1e1e', fg='white')
    button_sort_due_date.pack(pady=5)

    button_filter_completed = tk.Button(manage_window, text="Show Completed Tasks", command=filter_completed_tasks, bg='#1e1e1e', fg='white')
    button_filter_completed.pack(pady=5)

    button_filter_incomplete = tk.Button(manage_window, text="Show Incomplete Tasks", command=filter_incomplete_tasks, bg='#1e1e1e', fg='white')
    button_filter_incomplete.pack(pady=5)

# Set up the main window
root = tk.Tk()
root.title("Enhanced To-Do List Application")
root.configure(bg='black')

# Create and pack the widgets
frame_tasks = tk.Frame(root, bg='black')
frame_tasks.pack(pady=10)

entry_task = tk.Entry(frame_tasks, width=40, bg='#333333', fg='white')
entry_task.pack(side=tk.LEFT, padx=10)

combo_priority = ttk.Combobox(frame_tasks, values=['Low', 'Medium', 'High'], width=8)
combo_priority.set('Low')
combo_priority.pack(side=tk.LEFT, padx=10)

cal_due_date = DateEntry(frame_tasks, width=12, background='darkblue', foreground='white', borderwidth=2)
cal_due_date.pack(side=tk.LEFT, padx=10)

button_add_task = tk.Button(frame_tasks, text="Add Task", command=add_task, bg='#4caf50', fg='white')
button_add_task.pack(side=tk.LEFT)

button_frame = tk.Frame(root, bg='black')
button_frame.pack(pady=10)

button_edit_task = tk.Button(button_frame, text="Edit Task", command=edit_task, bg='#1e1e1e', fg='white')
button_edit_task.pack(side=tk.LEFT, padx=5, pady=5)

button_mark_completed = tk.Button(button_frame, text="Mark as Completed", command=mark_completed, bg='#1e1e1e', fg='white')
button_mark_completed.pack(side=tk.LEFT, padx=5, pady=5)

button_delete_task = tk.Button(button_frame, text="Delete Task", command=delete_task, bg='#f44336', fg='white')
button_delete_task.pack(side=tk.LEFT, padx=5, pady=5)

button_clear_tasks = tk.Button(button_frame, text="Clear All Tasks", command=clear_tasks, bg='#1e1e1e', fg='white')
button_clear_tasks.pack(side=tk.LEFT, padx=5, pady=5)

button_save_tasks = tk.Button(button_frame, text="Save Tasks", command=save_tasks, bg='#1e1e1e', fg='white')
button_save_tasks.pack(side=tk.LEFT, padx=5, pady=5)

button_load_tasks = tk.Button(button_frame, text="Load Tasks", command=load_tasks, bg='#1e1e1e', fg='white')
button_load_tasks.pack(side=tk.LEFT, padx=5, pady=5)

entry_search = tk.Entry(root, width=50, bg='#333333', fg='white')
entry_search.pack(pady=5)

button_search_tasks = tk.Button(root, text="Search Tasks", command=search_tasks, bg='#1e1e1e', fg='white')
button_search_tasks.pack(pady=5)

button_manage_tasks = tk.Button(root, text="Manage Tasks", command=manage_tasks, bg='#1e1e1e', fg='white')
button_manage_tasks.pack(pady=5)

listbox_tasks = tk.Listbox(root, width=80, height=15, bg='black', fg='white')
listbox_tasks.pack(pady=(0, 10))

# Start the GUI event loop
root.mainloop()
