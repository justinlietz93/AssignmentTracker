# database.py

import sqlite3
from constants import DATE_FORMAT

class Database:
    def __init__(self):
        # Connect to the SQLite database (it will be created if it doesn't exist)
        self.conn = sqlite3.connect('assignments.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.update_tables()

    def create_tables(self):
        # Create the assignments table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tab_name TEXT,
                assignment_title TEXT,
                due_date TEXT,
                status TEXT,
                notes TEXT
            )
        """)

        # Create the tabs table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tabs (
                name TEXT PRIMARY KEY
            )
        """)
        self.conn.commit()

    def update_tables(self):
        # Check if 'notes' column exists in assignments table
        self.cursor.execute("PRAGMA table_info(assignments)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if 'notes' not in columns:
            self.cursor.execute("ALTER TABLE assignments ADD COLUMN notes TEXT")
            self.conn.commit()

    def get_all_tabs(self):
        self.cursor.execute("SELECT name FROM tabs")
        tabs = [row[0] for row in self.cursor.fetchall()]
        return tabs

    def add_tab(self, tab_name):
        self.cursor.execute("INSERT OR IGNORE INTO tabs (name) VALUES (?)", (tab_name,))
        self.conn.commit()

    def rename_tab(self, old_name, new_name):
        # Update the tab name in the tabs table
        self.cursor.execute("UPDATE tabs SET name = ? WHERE name = ?", (new_name, old_name))
        # Update the tab_name in the assignments table
        self.cursor.execute("UPDATE assignments SET tab_name = ? WHERE tab_name = ?", (new_name, old_name))
        self.conn.commit()

    def delete_tab(self, tab_name):
        # Delete the tab from the tabs table
        self.cursor.execute("DELETE FROM tabs WHERE name = ?", (tab_name,))
        # Delete all assignments associated with the tab
        self.cursor.execute("DELETE FROM assignments WHERE tab_name = ?", (tab_name,))
        self.conn.commit()

    def add_assignment(self, tab_name, assignment_title, due_date, notes=''):
        self.cursor.execute("""
            INSERT INTO assignments (tab_name, assignment_title, due_date, status, notes)
            VALUES (?, ?, ?, 'Pending', ?)
        """, (tab_name, assignment_title, due_date, notes))
        self.conn.commit()

    def get_assignments(self, tab_name):
        self.cursor.execute("""
            SELECT id, tab_name, assignment_title, due_date, status, notes
            FROM assignments
            WHERE tab_name = ?
        """, (tab_name,))
        return self.cursor.fetchall()

    def get_assignment_by_id(self, assignment_id):
        self.cursor.execute("""
            SELECT id, tab_name, assignment_title, due_date, status, notes
            FROM assignments
            WHERE id = ?
        """, (assignment_id,))
        return self.cursor.fetchone()

    def update_notes(self, assignment_id, notes):
        try:
            self.cursor.execute("UPDATE assignments SET notes = ? WHERE id = ?", (notes, assignment_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error during update_notes: {e}")
            return False

    def mark_completed(self, assignment_id):
        self.cursor.execute("UPDATE assignments SET status = 'Completed' WHERE id = ?", (assignment_id,))
        self.conn.commit()

    def delete_assignment(self, assignment_id):
        self.cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
        self.conn.commit()

    def get_upcoming_assignments(self, today):
        try:
            self.cursor.execute("""
                SELECT id, tab_name, assignment_title, due_date, status, notes
                FROM assignments
                WHERE status = 'Pending' AND due_date >= ?
            """, (today.strftime(DATE_FORMAT),))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        self.conn.close()
