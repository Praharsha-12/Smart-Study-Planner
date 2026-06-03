import tkinter as tk
from tkinter import ttk, messagebox
import database

class StudySyncGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StudySync – Smart Study Planner")
        self.root.geometry("550x550")
        
        # Connect to the database you created in Phase 2
        database.init_db()
        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        # --- INPUT FORM BOX ---
        form_frame = tk.LabelFrame(self.root, text=" Add New Task ", padx=10, pady=10)
        form_frame.pack(fill="x", padx=15, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(form_frame, text="Subject:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_subject = tk.Entry(form_frame)
        self.ent_subject.grid(row=0, column=1, sticky="we", pady=2)

        tk.Label(form_frame, text="Task:").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_task = tk.Entry(form_frame)
        self.ent_task.grid(row=1, column=1, sticky="we", pady=2)

        tk.Label(form_frame, text="Deadline:").grid(row=2, column=0, sticky="w", pady=2)
        self.ent_deadline = tk.Entry(form_frame)
        self.ent_deadline.insert(0, "YYYY-MM-DD")
        self.ent_deadline.grid(row=2, column=1, sticky="we", pady=2)

        tk.Label(form_frame, text="Priority:").grid(row=3, column=0, sticky="w", pady=2)
        self.cmb_priority = ttk.Combobox(form_frame, values=["High", "Medium", "Low"], state="readonly")
        self.cmb_priority.current(1)
        self.cmb_priority.grid(row=3, column=1, sticky="we", pady=2)

        tk.Label(form_frame, text="Duration (min):").grid(row=4, column=0, sticky="w", pady=2)
        self.ent_duration = tk.Entry(form_frame)
        self.ent_duration.insert(0, "25")
        self.ent_duration.grid(row=4, column=1, sticky="we", pady=2)

        # Clickable button to add a task
        btn_add = tk.Button(form_frame, text="✨ Add Task", command=self.add_task, bg="#4CAF50", fg="white")
        btn_add.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # --- TASK LIST DISPLAY ---
        view_frame = tk.LabelFrame(self.root, text=" Study Tasks Schedule ", padx=10, pady=10)
        view_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Big scrollable box to show items
        self.list_tasks = tk.Listbox(view_frame, font=("Courier", 10))
        self.list_tasks.pack(fill="both", expand=True, side="left")
        
        scrollbar = tk.Scrollbar(view_frame, orient="vertical", command=self.list_tasks.yview)
        scrollbar.pack(side="right", fill="y")
        self.list_tasks.config(yscrollcommand=scrollbar.set)

        # --- ACTION BUTTONS ---
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill="x", padx=15)

        btn_complete = tk.Button(btn_frame, text="✅ Complete Task", command=self.complete_task, bg="#2196F3", fg="white")
        btn_complete.pack(side="left", fill="x", expand=True, padx=5)

        # --- TASK TIMER BAR ---
        timer_frame = tk.LabelFrame(self.root, text=" Task Timer ", padx=10, pady=10)
        timer_frame.pack(fill="x", padx=15, pady=10)

        self.lbl_current_task = tk.Label(timer_frame, text="No task selected", font=("Helvetica", 10), fg="#555")
        self.lbl_current_task.pack(side="left", padx=(0,5))

        self.lbl_timer = tk.Label(timer_frame, text="00:00", font=("Helvetica", 16, "bold"))
        self.lbl_timer.pack(side="left", padx=20)

        self.btn_timer = tk.Button(timer_frame, text="⏱️ Start Focus", command=self.toggle_timer, bg="#FF5722", fg="white")
        self.btn_timer.pack(side="right", fill="x", expand=True, padx=5)
        
        self.timer_running = False
        self.timer_reset = True
        self.current_duration_minutes = 0
        self.seconds_left = 0
        self.current_task_id = None

    def add_task(self):
        """Grabs text from boxes and sends it to database.py"""
        sub = self.ent_subject.get().strip()
        tsk = self.ent_task.get().strip()
        dl = self.ent_deadline.get().strip()
        pr = self.cmb_priority.get()
        duration_text = self.ent_duration.get().strip()

        if not sub or not tsk:
            messagebox.showwarning("Missing Information", "Please enter both a Subject and a Task description.")
            return

        try:
            duration = int(duration_text)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Duration", "Please enter a positive number of minutes for the task duration.")
            return

        database.add_task_to_db(sub, tsk, dl, pr, duration)
        self.refresh_task_list()
        
        # Clear fields for the next entry
        self.ent_subject.delete(0, tk.END)
        self.ent_task.delete(0, tk.END)
        self.ent_duration.delete(0, tk.END)
        self.ent_duration.insert(0, "25")

    def refresh_task_list(self):
        """Fetches data from database.py and puts it in the Listbox"""
        self.list_tasks.delete(0, tk.END)
        self.task_mappings = {}  # Maps visual list index to actual database row ID
        self.tasks = []
        
        tasks = database.get_all_tasks()
        self.tasks = tasks
        for idx, t in enumerate(tasks):
            db_id = t[0]
            subject = t[1]
            task_desc = t[2]
            priority = t[4]
            duration = t[5]
            status = t[6]
            
            # Formats text into neat visual columns
            display_str = f"{subject[:10]:<12} | {task_desc[:15]:<18} | {duration:>3}m | {priority:<6} | {status}"
            self.list_tasks.insert(tk.END, display_str)
            self.task_mappings[idx] = db_id

    def complete_task(self):
        """Prevents manual completion until the timer finishes."""
        try:
            selected_index = self.list_tasks.curselection()[0]
            task = self.tasks[selected_index]
            status = task[6]
            if status == "Completed":
                messagebox.showinfo("Already Completed", "This task is already completed.")
            else:
                messagebox.showwarning("Timer Required", "Start the task timer and wait until your chosen duration ends. The task will be marked completed automatically.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please click on a task from the list first.")

    def get_selected_task(self):
        """Returns the currently selected task tuple or None."""
        try:
            selected_index = self.list_tasks.curselection()[0]
            return self.tasks[selected_index]
        except IndexError:
            return None

    def toggle_timer(self):
        """Starts or pauses the countdown clock for the selected task."""
        if self.timer_running:
            self.timer_running = False
            self.btn_timer.config(text="⏱️ Start Focus")
            return

        task = self.get_selected_task()
        if task is None:
            messagebox.showwarning("Selection Required", "Please select a task to start its timer.")
            return

        task_id, _, task_desc, _, _, duration, status = task
        if status == "Completed":
            messagebox.showinfo("Task Completed", "This task is already completed.")
            return

        if duration <= 0:
            messagebox.showwarning("Invalid Task Duration", "This task does not have a valid duration. Edit it and try again.")
            return

        if self.timer_reset or self.current_task_id != task_id:
            self.current_task_id = task_id
            self.current_duration_minutes = duration
            self.seconds_left = self.current_duration_minutes * 60
            self.lbl_current_task.config(text=f"{task_desc[:30]} ({duration} min)")
            self.lbl_timer.config(text=f"{self.current_duration_minutes:02d}:00")
            self.timer_reset = False

        self.timer_running = True
        self.btn_timer.config(text="⏸️ Pause")
        self.countdown()

    def countdown(self):
        """Ticks down every 1 second without freezing the app window"""
        if self.timer_running and self.seconds_left > 0:
            mins, secs = divmod(self.seconds_left, 60)
            self.lbl_timer.config(text=f"{mins:02d}:{secs:02d}")
            self.seconds_left -= 1
            self.root.after(1000, self.countdown)
        elif self.timer_running and self.seconds_left == 0:
            self.timer_running = False
            self.btn_timer.config(text="⏱️ Start Focus")
            self.timer_reset = True
            self.lbl_timer.config(text="00:00")
            self.lbl_current_task.config(text="No task selected")

            if self.current_task_id is not None:
                database.complete_task_in_db(self.current_task_id)
                self.refresh_task_list()
                messagebox.showinfo("Task Completed", "Well done! The selected task is now marked complete.")
                self.current_task_id = None

if __name__ == "__main__":
    window = tk.Tk()
    app = StudySyncGUI(window)
    window.mainloop()