import tkinter as tk
from tkinter import messagebox

class EventHandlers:
    def __init__(self, app):
        self.app = app


    def on_assignment_double_click(self, event):
        tree = event.widget
        # Identify the item that was double-clicked
        item_id = tree.identify_row(event.y)
        if item_id:
            try:
                assignment_id = int(item_id)  # The iid is the assignment_id
                self.app.open_details_window(assignment_id)
            except ValueError:
                messagebox.showerror("Error", "Invalid assignment ID.")


    def on_dashboard_item_double_click(self, event):
        tree = event.widget
        selected_items = tree.selection()
        if selected_items:
            item = selected_items[0]
            values = tree.item(item, 'values')
            if len(values) >= 2:
                tab_name = values[0]
                assignment_title = values[1]
                self.app.open_assignment_from_dashboard(tab_name, assignment_title)
            else:
                messagebox.showerror("Error", "Invalid assignment data.")

    
    def on_mark_completed(self):
        selected_items = self.app.selected_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select one or more assignments to mark as completed.")
            return
        for item in selected_items:
            try:
                assignment_id = int(item)  # The iid is the assignment_id
                self.app.db.mark_completed(assignment_id)
            except ValueError:
                messagebox.showerror("Error", f"Invalid assignment ID: {item}")
        # Reload assignments in the current tab
        current_tab = self.app.notebook.select()
        tab_name = self.app.notebook.tab(current_tab, "text")
        self.app.load_assignments(tab_name)

   
    def on_delete_assignment(self):
        selected_items = self.app.selected_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select one or more assignments to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected assignments?")
        if not confirm:
            return
        for item in selected_items:
            try:
                assignment_id = int(item)  # The iid is the assignment_id
                self.app.db.delete_assignment(assignment_id)
            except ValueError:
                messagebox.showerror("Error", f"Invalid assignment ID: {item}")
        # Reload assignments in the current tab
        current_tab = self.app.notebook.select()
        tab_name = self.app.notebook.tab(current_tab, "text")
        self.app.load_assignments(tab_name)

   
    def on_save_notes(self, assignment_id, notes, window):
        try:
            self.app.db.update_notes(assignment_id, notes)
            messagebox.showinfo("Success", "Notes saved successfully.")
            window.destroy()
            # Reload assignments in the current tab to reflect any changes
            current_tab = self.app.notebook.select()
            tab_name = self.app.notebook.tab(current_tab, "text")
            self.app.load_assignments(tab_name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving notes: {e}")


    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        tab_name = event.widget.tab(selected_tab, "text")
        self.current_tab = tab_name


    def on_open_assignment_from_dashboard(self, tab_name, assignment_title):
        # Switch to the corresponding tab
        for idx in range(len(self.app.notebook.tabs())):
            tab = self.app.notebook.tabs()[idx]
            if self.app.notebook.tab(tab, "text") == tab_name:
                self.app.notebook.select(idx)
                break

        # Highlight the assignment in the Treeview
        tree = self.app.tab_trees.get(tab_name)
        if tree:
            # Find the item with the matching assignment title
            for child in tree.get_children():
                if tree.item(child)['values'][0] == assignment_title:
                    tree.selection_set(child)
                    tree.focus(child)
                    tree.see(child)
                    break
