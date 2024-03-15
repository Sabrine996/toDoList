import tkinter as tk
import json
import csv

class TaskManager:
    def __init__(self, master, filename):
        self.master = master
        master.title("Task Manager")
        self.tasks = []
        self.filtered_tasks = []  
        self.filename = filename
        
        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text='Add Task', command=self.add_task)
        self.add_button.pack()

        self.delete_button = tk.Button(master, text='Delete Task', command=self.delete_task)
        self.delete_button.pack()

        self.show_button = tk.Button(master, text='Show Tasks', command=self.show_tasks)
        self.show_button.pack()

        self.filter_entry = tk.Entry(master)  
        self.filter_entry.pack()

        self.filter_button = tk.Button(master, text='Filter Tasks', command=self.filter_tasks)
        self.filter_button.pack()

        self.export_button = tk.Button(master, text='Export to CSV', command=self.export_to_csv)
        self.export_button.pack()

        self.task_frame = tk.Frame(master)
        self.task_frame.pack()

        self.checkbox_vars = []

        self.load_tasks_from_json()  

    def add_task(self):
        task = self.task_entry.get()
        self.tasks.append((task, False))
        self.save_tasks_to_json()
        self.task_entry.delete(0, tk.END)

    def delete_task(self):
        if self.tasks:
            del self.tasks[-1]
            self.save_tasks_to_json()

    def show_tasks(self):
        self.show_tasks_in_interface(self.tasks)

    def filter_tasks(self):
        keyword = self.filter_entry.get().lower()  
        if not keyword:  
            self.show_tasks_in_interface(self.tasks)
        else:
            self.filtered_tasks = [task for task in self.tasks if keyword in task[0].lower()]  
            self.show_tasks_in_interface(self.filtered_tasks)  

    def save_tasks_to_json(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)

    def load_tasks_from_json(self):
        try:
            with open(self.filename, 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            print("No tasks found.")

    def export_to_csv(self):
        csv_filename = "tasks.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Tasks: '])
            for task, _ in self.tasks:
                writer.writerow([task])

    def show_tasks_in_interface(self, tasks):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars = []

        if tasks: 
            for i, (task, important) in enumerate(tasks):
                task_display_str = f"{task}{' (important)' if important else ''}"
                label = tk.Label(self.task_frame, text=task_display_str)
                label.grid(row=i, column=0, sticky=tk.W)
                cb = tk.Checkbutton(self.task_frame, text="Important", variable=tk.BooleanVar())
                cb.grid(row=i, column=1, sticky=tk.W)
                self.checkbox_vars.append(cb)
        else:
            label = tk.Label(self.task_frame, text="No tasks")
            label.grid(row=0, column=0, sticky=tk.W)

root = tk.Tk()
app = TaskManager(root, "tasks.json")
root.mainloop()