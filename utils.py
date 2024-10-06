import datetime
from constants import DATE_FORMAT
from tkinter import messagebox

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, DATE_FORMAT).date()
    except ValueError as ve:
        raise ValueError(f"Date '{date_str}' does not match format {DATE_FORMAT}.") from ve

def validate_date(date_str):
    try:
        parse_date(date_str)
        return True
    except ValueError:
        return False

def show_error(message):
    messagebox.showerror("Error", message)

def show_info(message):
    messagebox.showinfo("Information", message)

def format_date(date_obj):
    return date_obj.strftime(DATE_FORMAT)
