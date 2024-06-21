import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("700x700")
        self.root.config(bg="#f0f8ff")

        # Frame for the title
        self.title_frame = tk.Frame(self.root, bg="#4682b4")
        self.title_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.title_frame, text="To-Do List", font=("Helvetica", 20), bg="#4682b4", fg="#ffffff")
        self.title_label.pack(pady=10)

        # Frame for the task entry
        self.task_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.task_frame.pack(pady=10)

        tk.Label(self.task_frame, text="Task:", bg="#f0f8ff", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.task_entry = tk.Entry(self.task_frame, width=30, font=("Helvetica", 12))
        self.task_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.task_frame, text="Due Date (YYYY-MM-DD):", bg="#f0f8ff", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.date_entry = tk.Entry(self.task_frame, width=15, font=("Helvetica", 12))
        self.date_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.task_frame, text="Due Time (HH:MM):", bg="#f0f8ff", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.time_entry = tk.Entry(self.task_frame, width=10, font=("Helvetica", 12))
        self.time_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.task_frame, text="Priority:", bg="#f0f8ff", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.priority_combobox = ttk.Combobox(self.task_frame, values=["High", "Medium", "Low"], font=("Helvetica", 12), state="readonly")
        self.priority_combobox.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        self.priority_combobox.current(1)

        self.add_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task, bg="#32cd32", fg="#ffffff", font=("Helvetica", 12))
        self.add_button.grid(row=4, columnspan=2, pady=10)

        # Treeview for displaying tasks
        columns = ("task", "added", "due_date", "due_time", "priority")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("task", text="Task")
        self.tree.heading("added", text="Added")
        self.tree.heading("due_date", text="Due Date")
        self.tree.heading("due_time", text="Due Time")
        self.tree.heading("priority", text="Priority")

        self.tree.column("task", width=200)
        self.tree.column("added", width=100)
        self.tree.column("due_date", width=100)
        self.tree.column("due_time", width=100)
        self.tree.column("priority", width=100)

        self.tree.pack(pady=20)

        # Frame for action buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.button_frame.pack(pady=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="#ff6347", fg="#ffffff", font=("Helvetica", 12))
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.mark_button = tk.Button(self.button_frame, text="Mark as Completed", command=self.mark_task, bg="#4682b4", fg="#ffffff", font=("Helvetica", 12))
        self.mark_button.pack(side=tk.LEFT, padx=5)

        # Label for task count
        self.task_count_label = tk.Label(self.root, text="Total Tasks: 0", bg="#f0f8ff", font=("Helvetica", 12))
        self.task_count_label.pack(pady=10)

    def update_task_count(self):
        task_count = len(self.tree.get_children())
        self.task_count_label.config(text=f"Total Tasks: {task_count}")

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.date_entry.get()
        due_time = self.time_entry.get()
        priority = self.priority_combobox.get()

        if task == "" or due_date == "" or due_time == "":
            messagebox.showwarning("Warning", "You must enter a task, due date, and due time.")
            return
        
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            datetime.strptime(due_time, "%H:%M")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date or time format.")
            return

        current_date = datetime.now().strftime("%Y-%m-%d")
        self.tree.insert("", "end", values=(task, current_date, due_date, due_time, priority))
        self.sort_tasks()
        
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.priority_combobox.current(1)
        self.update_task_count()

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.update_task_count()
        else:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def mark_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_values = self.tree.item(selected_item, "values")
            if not task_values[0].endswith(" (completed)"):
                new_values = (task_values[0] + " (completed)", *task_values[1:])
                self.tree.item(selected_item, values=new_values)
        else:
            messagebox.showwarning("Warning", "You must select a task to mark as completed.")

    def sort_tasks(self):
        tasks = [(self.tree.set(k, "priority"), k) for k in self.tree.get_children("")]
        tasks.sort(key=lambda t: {"High": 1, "Medium": 2, "Low": 3}[t[0]])

        for index, (_, k) in enumerate(tasks):
            self.tree.move(k, "", index)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()