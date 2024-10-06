# add_assignment_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from constants import DATE_FORMAT
from utils import parse_date


class AssignmentWindow(tk.Toplevel):
    def __init__(self, master, save_callback):
        # Initialize the AssignmentWindow for adding a new assignment.

        # Args:
        #     master (tk.Widget): The parent window.
        #     save_callback (function): A callback function to save the new assignment.
        #                               Expected to accept four parameters:
        #                               title (str), due_date (str), status (str), notes (str).
        super().__init__(master)
        self.title("Add Assignment")
        self.save_callback = save_callback  # Callback function to save the assignment
        self.create_widgets()
        self.grab_set()  # Make the window modal

    def create_widgets(self):
        # Frame for form inputs
        form_frame = tk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Assignment Title
        tk.Label(form_frame, text="Assignment Title:", font=("Helvetica", 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = tk.Entry(form_frame, width=50)
        self.title_entry.grid(row=0, column=1, pady=5)

        # Due Date
        tk.Label(form_frame, text="Due Date (YYYY-MM-DD):", font=("Helvetica", 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.due_date_entry = tk.Entry(form_frame, width=50)
        self.due_date_entry.grid(row=1, column=1, pady=5)

        # Status
        tk.Label(form_frame, text="Status:", font=("Helvetica", 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(form_frame, textvariable=self.status_var, state="readonly", width=47)
        self.status_combobox['values'] = ("Pending", "Completed")
        self.status_combobox.current(0)  # Set default to "Pending"
        self.status_combobox.grid(row=2, column=1, pady=5)

        # Notes
        tk.Label(form_frame, text="Notes:", font=("Helvetica", 10)).grid(row=3, column=0, sticky='nw', pady=5)
        self.notes_text = tk.Text(form_frame, width=38, height=10)
        self.notes_text.grid(row=3, column=1, pady=5)

        # Save Button
        save_button = tk.Button(self, text="Save", command=self.on_save, width=15)
        save_button.pack(pady=10)

    def on_save(self):
        title = self.title_entry.get().strip()
        due_date_str = self.due_date_entry.get().strip()
        status = self.status_var.get()
        notes = self.notes_text.get('1.0', 'end-1c').strip()

        # Validate input fields
        if not title:
            messagebox.showerror("Input Error", "Assignment title is required.")
            return

        if not due_date_str:
            messagebox.showerror("Input Error", "Due date is required.")
            return

        # Validate due date format
        try:
            due_date = parse_date(due_date_str)
        except ValueError:
            messagebox.showerror("Input Error", f"Due date must be in {DATE_FORMAT} format.")
            return

        # Invoke the save callback with the collected data
        if self.save_callback:
            success = self.save_callback(title, due_date_str, status, notes)
            if success:
                messagebox.showinfo("Success", "Assignment added successfully.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to add assignment.")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to close the add assignment window?"):
            self.destroy()
