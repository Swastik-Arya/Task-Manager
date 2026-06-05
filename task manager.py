import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT
)
""")
conn.commit()

def load_tasks():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks")
    for row in cursor.fetchall():
        listbox.insert(tk.END, row[1])

def add_task():
    task = entry.get()
    if task == "":
        messagebox.showwarning("Error", "Task cannot be empty!")
        return
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    entry.delete(0, tk.END)
    load_tasks()

def delete_task():
    try:
        selected = listbox.curselection()[0]
        task_text = listbox.get(selected)
        cursor.execute("DELETE FROM tasks WHERE task=?", (task_text,))
        conn.commit()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Error", "Select a task to delete!")

def edit_task():
    try:
        selected = listbox.curselection()[0]
        old_task = listbox.get(selected)
        new_task = entry.get()
        if new_task == "":
            messagebox.showwarning("Error", "Enter new task!")
            return
        cursor.execute("UPDATE tasks SET task=? WHERE task=?", (new_task, old_task))
        conn.commit()
        entry.delete(0, tk.END)
        load_tasks()
    except IndexError:
        messagebox.showwarning("Error", "Select a task to edit!")

root = tk.Tk()
root.title("Task Manager")
root.geometry("400x400")
root.resizable(False, False)

tk.Label(root, text="Task Manager", font=("Arial", 16)).pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)
tk.Button(root, text="Add Task", command=add_task, width=15, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Edit Task", command=edit_task, width=15, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Delete Task", command=delete_task, width=15, bg="red", fg="white").pack(pady=5)
listbox = tk.Listbox(root, width=40, height=10)
listbox.pack(pady=10)

load_tasks()
root.mainloop()
conn.close()