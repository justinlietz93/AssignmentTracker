import tkinter as tk
from tkinter import ttk
import datetime

from constants import DATE_FORMAT, TREEVIEW_COLUMNS
from utils import parse_date

class Dashboard(tk.Toplevel):
    def __init__(self, master, db, open_assignment_callback):
        super().__init__(master)
        self.title("Upcoming Assignments Dashboard")
        self.db = db
        self.open_assignment_callback = open_assignment_callback
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Create a Treeview to display assignments
        columns = ('Course Name', 'Assignment Title', 'Due Date')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=50, width=200)
        self.tree.pack(expand=True, fill='both')

        # Add a Refresh button
        refresh_button = tk.Button(self, text="Refresh", command=self.load_data)
        refresh_button.pack(side=tk.TOP, padx=5, pady=5)

        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_item_double_click)

    def load_data(self):
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get today's date
        today = datetime.date.today()

        # Query the database for pending assignments due after today
        pending_assignments = self.db.get_upcoming_assignments(today)

        # Parse due dates and filter assignments due after today
        assignments_with_dates = []
        for assignment in pending_assignments:
            due_date_str = assignment[3]
            try:
                due_date = parse_date(due_date_str)
                if due_date >= today:
                    assignments_with_dates.append((assignment[0], assignment[1], assignment[2], due_date))
            except ValueError:
                continue  # Skip assignments with invalid date format

        # Sort assignments by due date
        sorted_assignments = sorted(assignments_with_dates, key=lambda x: x[3])  # x[3] is due_date

        # Take the top 10 assignments
        top_assignments = sorted_assignments[:10]

        # Insert assignments into the Treeview
        for assignment in top_assignments:
            tab_name = assignment[1]          # tab_name
            assignment_title = assignment[2]  # assignment_title
            due_date = assignment[3].strftime(DATE_FORMAT)  # Convert date back to string
            self.tree.insert('', tk.END, values=(tab_name, assignment_title, due_date))

    def on_item_double_click(self, event):
        item = self.tree.selection()
        if item:
            values = self.tree.item(item, 'values')
            tab_name = values[0]
            assignment_title = values[1]
            self.open_assignment_callback(tab_name, assignment_title)
            self.focus()
