import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
import datetime
import csv
from database import Database
from event_handlers import EventHandlers
from details_window import DetailsWindow
from dashboard import Dashboard
from constants import COLORS, DATE_FORMAT
from utils import parse_date


class AssignmentTracker:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("College Assignment Tracker")
        # Initialize other components and load tabs
        self.create_widgets()
        # Initialize event handlers
        self.event_handlers = EventHandlers(self)
        self.load_tabs()


    def create_widgets(self):
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Tabs menu
        tab_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tabs", menu=tab_menu)
        tab_menu.add_command(label="Add Tab", command=self.add_tab)
        tab_menu.add_command(label="Rename Tab", command=self.rename_tab)
        tab_menu.add_command(label="Delete Tab", command=self.delete_tab)

        # Import menu
        import_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Import", menu=import_menu)
        import_menu.add_command(label="Import CSV", command=self.import_csv)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dashboard", command=self.open_dashboard)

        # Add a frame for action buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Add "Complete" button
        complete_button = tk.Button(button_frame, text="Complete", command=self.mark_selected_completed)
        complete_button.pack(side=tk.RIGHT, padx=(5,20), pady=5)

        # Add "Delete" button
        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_selected_assignments)
        delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        # Dictionaries to hold frames and Treeviews for each tab
        self.tab_frames = {}
        self.tab_trees = {}

        # Context Menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Mark as Completed", command=self.mark_completed)
        self.menu.add_command(label="Delete Assignment", command=self.delete_assignment)

        # Selected Treeview
        self.selected_tree = None


    def load_tabs(self):
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.tab_frames.clear()
        self.tab_trees.clear()

        # Get all tabs from the database
        tabs = self.db.get_all_tabs()
        if not tabs:
            # If no tabs, create a default tab
            self.add_tab("Default")
        else:
            for tab_name in tabs:
                self.create_tab(tab_name)


    def create_tab(self, tab_name):
        # Create a new frame for the tab
        tab_frame = tk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=tab_name)

        # Create a Treeview in the tab with multiple selection enabled
        columns = ('Assignment Title', 'Due Date', 'Status')
        tree = ttk.Treeview(tab_frame, columns=columns, show='headings', selectmode='extended')

        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(tree, _col, False))
            tree.column(col, minwidth=50, width=200)
        tree.pack(expand=True, fill='both')

        # Bind context menu to the Treeview
        tree.bind('<Button-3>', self.show_context_menu)
        # Bind double-click event to the Treeview
        tree.bind('<Double-1>', self.event_handlers.on_assignment_double_click)

        # Store the frame and tree
        self.tab_frames[tab_name] = tab_frame
        self.tab_trees[tab_name] = tree

        # Load assignments into the tree
        self.load_assignments(tab_name)


    def treeview_sort_column(self, tree, col, reverse):
        # Sorts the Treeview column when header is clicked.
        # Get all items in the Treeview
        data_list = [(tree.set(k, col), k) for k in tree.get_children('')]

        # Try to convert data to appropriate type for sorting
        try:
            # For date columns, parse the date string to datetime objects
            if col == 'Due Date':
                data_list.sort(key=lambda t: parse_date(t[0]), reverse=reverse)
            else:
                # For other columns, sort as strings (case-insensitive)
                data_list.sort(key=lambda t: t[0].lower(), reverse=reverse)
        except Exception as e:
            # If there is an error in conversion, sort as strings
            data_list.sort(key=lambda t: t[0].lower(), reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(data_list):
            tree.move(k, '', index)

        # Toggle the sort order for next click
        tree.heading(col, command=lambda: self.treeview_sort_column(tree, col, not reverse))


    def add_tab(self, tab_name=None):
        if not tab_name:
            # Ask for tab name
            tab_name = simpledialog.askstring("Add Tab", "Enter tab name:")
            if not tab_name:
                return
        if tab_name in self.tab_frames:
            messagebox.showerror("Error", f"Tab '{tab_name}' already exists.")
            return
        self.create_tab(tab_name)
        self.db.add_tab(tab_name)


    def rename_tab(self):
        current_tab = self.notebook.select()
        if not current_tab:
            return
        current_tab_index = self.notebook.index(current_tab)
        old_name = self.notebook.tab(current_tab, "text")
        new_name = simpledialog.askstring("Rename Tab", "Enter new tab name:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return
        if new_name in self.tab_frames:
            messagebox.showerror("Error", f"Tab '{new_name}' already exists.")
            return
        # Update the tab name in the notebook
        self.notebook.tab(current_tab, text=new_name)
        # Update the tab_frames and tab_trees dictionaries
        self.tab_frames[new_name] = self.tab_frames.pop(old_name)
        self.tab_trees[new_name] = self.tab_trees.pop(old_name)
        # Update the database
        self.db.rename_tab(old_name, new_name)


    def delete_tab(self):
        current_tab = self.notebook.select()
        if not current_tab:
            return
        tab_name = self.notebook.tab(current_tab, "text")
        confirm = messagebox.askyesno("Delete Tab", f"Are you sure you want to delete the tab '{tab_name}' and all its assignments?")
        if confirm:
            # Remove tab from notebook
            self.notebook.forget(current_tab)
            # Remove from tab_frames and tab_trees
            del self.tab_frames[tab_name]
            del self.tab_trees[tab_name]
            # Delete assignments from database
            self.db.delete_tab(tab_name)


    def import_csv(self):
        # Open a file dialog to select the CSV file
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

        if not file_path:
            return  # User cancelled the file dialog

        current_tab = self.notebook.select()
        if not current_tab:
            messagebox.showerror("No Tab Selected", "Please select a tab to import assignments into.")
            return
        tab_name = self.notebook.tab(current_tab, "text")

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                required_fields = {'assignment_title', 'due_date'}

                # Check if the CSV has the required headers
                if not required_fields.issubset(reader.fieldnames):
                    messagebox.showerror("CSV Error", f"CSV file must contain headers: {', '.join(required_fields)}")
                    return

                imported_count = 0
                for row in reader:
                    assignment_title = row['assignment_title'].strip()
                    due_date = row['due_date'].strip()
                    notes = row.get('notes', '').strip()

                    if not assignment_title or not due_date:
                        continue  # Skip incomplete rows

                    # Validate date format
                    try:
                        parse_date(due_date)
                    except ValueError:
                        continue  # Skip rows with invalid date format

                    # Add assignment to the database
                    self.db.add_assignment(tab_name, assignment_title, due_date, notes)
                    imported_count += 1

                self.load_assignments(tab_name)
                messagebox.showinfo("Import Complete", f"Successfully imported {imported_count} assignments into '{tab_name}' tab.")
        except Exception as e:
            messagebox.showerror("Import Error", f"An error occurred while importing: {e}")


    def load_assignments(self, tab_name):
        if tab_name not in self.tab_trees:
            return
        tree = self.tab_trees[tab_name]
        # Clear the tree
        for item in tree.get_children():
            tree.delete(item)
        # Get assignments from the database
        assignments = self.db.get_assignments(tab_name)
        for row in assignments:
            assignment_id = row[0]
            assignment_title = row[2]
            due_date = row[3]
            status = row[4]
            # Determine the color tag based on status and due date
            if status == 'Completed':
                color_tag = 'completed'
            else:
                color_tag = self.get_due_date_color_tag(due_date)
            # Insert the assignment into the Treeview with the color tag
            tree.insert('', tk.END, iid=assignment_id, values=(assignment_title, due_date, status), tags=(color_tag,))
        # Configure tags for background and foreground colors
        for tag, color in COLORS.items():
            tree.tag_configure(tag, background=color['background'], foreground=color['foreground'])


    def get_due_date_color_tag(self, due_date_str):
        # Returns the color tag based on how close the due date is.
        try:
            due_date = parse_date(due_date_str)
            today = datetime.date.today()
            delta_days = (due_date - today).days
            if delta_days < 0:
                return 'red'  # Past due dates
            elif delta_days <= 3:
                return 'red'
            elif 3 < delta_days <= 7:
                return 'orange'
            elif 7 < delta_days <= 14:
                return 'green'
            elif delta_days > 14:
                return 'blue'
            else:
                return 'blue'
        except ValueError:
            return ''


    def show_context_menu(self, event):
        widget = event.widget
        self.selected_tree = widget
        selected_item = widget.identify_row(event.y)
        if selected_item:
            if selected_item not in widget.selection():
                widget.selection_set(selected_item)
            self.menu.post(event.x_root, event.y_root)


    def mark_completed(self):
        selected_items = self.selected_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select one or more assignments to mark as completed.")
            return
        for item in selected_items:
            assignment_id = int(item)  # The iid is the assignment_id
            self.db.mark_completed(assignment_id)
        # Reload assignments in the current tab
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        self.load_assignments(tab_name)


    def delete_assignment(self):
        selected_items = self.selected_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select one or more assignments to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected assignments?")
        if not confirm:
            return
        for item in selected_items:
            assignment_id = int(item)  # The iid is the assignment_id
            self.db.delete_assignment(assignment_id)
        # Reload assignments in the current tab
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        self.load_assignments(tab_name)


    def mark_selected_completed(self):
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        tree = self.tab_trees[tab_name]
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select one or more assignments to mark as completed.")
            return
        for item in selected_items:
            assignment_id = int(item)  # The iid is the assignment_id
            self.db.mark_completed(assignment_id)
        self.load_assignments(tab_name)


    def delete_selected_assignments(self):
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        tree = self.tab_trees[tab_name]
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select one or more assignments to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected assignments?")
        if not confirm:
            return
        for item in selected_items:
            assignment_id = int(item)  # The iid is the assignment_id
            self.db.delete_assignment(assignment_id)
        self.load_assignments(tab_name)


    def open_dashboard(self):
        if hasattr(self, 'dashboard_window') and self.dashboard_window.winfo_exists():
            self.dashboard_window.focus()
        else:
            self.dashboard_window = Dashboard(self.root, self.db, self.open_assignment_from_dashboard)


    def open_assignment_from_dashboard(self, tab_name, assignment_title):
        # Switch to the corresponding tab
        for idx in range(len(self.notebook.tabs())):
            tab = self.notebook.tabs()[idx]
            if self.notebook.tab(tab, "text") == tab_name:
                self.notebook.select(idx)
                break

        # Highlight the assignment in the Treeview
        tree = self.tab_trees.get(tab_name)
        if tree:
            # Find the item with the matching assignment title
            for child in tree.get_children():
                if tree.item(child)['values'][0] == assignment_title:
                    tree.selection_set(child)
                    tree.see(child)
                    break


    def open_details_window(self, assignment_id):
        # Retrieve assignment data from the database
        assignment = self.db.get_assignment_by_id(assignment_id)
        if assignment:
            DetailsWindow(self.root, assignment, self.save_notes)


    def save_notes(self, assignment_id, notes):
        # Update notes in the database
        success = self.db.update_notes(assignment_id, notes)
        if success:
            # Reload assignments in the current tab
            current_tab = self.notebook.select()
            tab_name = self.notebook.tab(current_tab, "text")
            self.load_assignments(tab_name)
        return success