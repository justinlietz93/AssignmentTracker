# details_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from constants import DATE_FORMAT
from utils import parse_date

class DetailsWindow(tk.Toplevel):
    def __init__(self, master, assignment, save_callback):
        super().__init__(master)
        self.title("Assignment Details")
        self.assignment = assignment
        self.save_callback = save_callback # Callback function to save notes
        self.create_widgets()
        self.grab_set()  # Make the details window modal

    def create_widgets(self):
        # Assignment Title
        assignment_title = self.assignment[2]
        tk.Label(self, text=f"Title: {assignment_title}", font=("Helvetica", 12, "bold")).pack(anchor='w', padx=10, pady=5)

        # Due Date
        due_date_str = self.assignment[3]
        try:
            due_date = parse_date(due_date_str)
            formatted_due_date = due_date.strftime(DATE_FORMAT)
        except ValueError:
            formatted_due_date = due_date_str  # If parsing fails, display the original string
        tk.Label(self, text=f"Due Date: {formatted_due_date}", font=("Helvetica", 10)).pack(anchor='w', padx=10, pady=5)

        # Status
        status = self.assignment[4]
        tk.Label(self, text=f"Status: {status}", font=("Helvetica", 10)).pack(anchor='w', padx=10, pady=5)

        # Notes Label
        tk.Label(self, text="Notes:", font=("Helvetica", 10, "bold")).pack(anchor='w', padx=10, pady=(10, 0))

        # Notes Text Box
        self.notes_text = tk.Text(self, width=50, height=10)
        self.notes_text.pack(padx=10, pady=5)
        notes = self.assignment[5] or ''  # Handle None values
        self.notes_text.insert('1.0', notes)

        # Save Button
        save_button = tk.Button(self, text="Save", command=self.on_save)
        save_button.pack(pady=10)

    def on_save(self):
        # Handle the save action. Retrieve notes from the text box and invoke the save callback.
        notes = self.notes_text.get('1.0', 'end-1c').strip()
        if self.save_callback:
            success = self.save_callback(self.assignment[0], notes)
            if success:
                messagebox.showinfo("Success", "Notes saved successfully.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to save notes.")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to close the details window?"):
            self.destroy()
