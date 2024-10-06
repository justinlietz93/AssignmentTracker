# constants.py

# Date format used throughout the application
DATE_FORMAT = '%Y-%m-%d'

# Color configurations for different assignment statuses and due date proximities
COLORS = {
    'completed': {
        'background': 'gray',
        'foreground': 'white'
    },
    'red': {
        'background': 'red',
        'foreground': 'white'
    },
    'orange': {
        'background': 'orange',
        'foreground': 'black'
    },
    'green': {
        'background': 'green',
        'foreground': 'black'
    },
    'blue': {
        'background': 'light blue',
        'foreground': 'black'
    }
}

# Required fields for CSV import
REQUIRED_CSV_FIELDS = {'assignment_title', 'due_date'}

# Default tab name if none exist
DEFAULT_TAB_NAME = 'Default'

# Column names for Treeview widgets
TREEVIEW_COLUMNS = ('Assignment Title', 'Due Date', 'Status')

# Status values
STATUS_PENDING = 'Pending'
STATUS_COMPLETED = 'Completed'
