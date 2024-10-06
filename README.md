# College Assignment Tracker

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
  - [Launching the Application](#launching-the-application)
  - [Managing Courses (Tabs)](#managing-courses-tabs)
  - [Managing Assignments](#managing-assignments)
  - [Importing Assignments via CSV](#importing-assignments-via-csv)
  - [Viewing the Dashboard](#viewing-the-dashboard)
  - [Editing Assignment Notes](#editing-assignment-notes)
- [Contributing](#contributing)
- [Contact](#contact)

## Introduction
welcome to the college assignment tracker, a custom desktop application designed to help students efficiently manage and track their college assignments. built with python and tkinter, this application offers a user-friendly interface to organize assignments by courses, monitor due dates, and keep detailed notes for each task.

## Features
- **course management**: create, rename, and delete tabs representing different courses.
- **assignment management**: add, view, edit, mark as completed, and delete assignments.
- **due date tracking**: visual indicators highlight assignments based on upcoming deadlines.
- **csv import**: easily import assignments from csv files to populate your tracker quickly.
- **dashboard**: view the top 10 closest pending assignments across all courses in a dedicated dashboard.
- **detailed notes**: add and edit detailed notes for each assignment, including file paths and links.
- **sorting and filtering**: sort assignments by title, due date, or status, and filter based on specific criteria.
- **multi-selection**: select multiple assignments for batch operations like marking as completed or deletion.
- **persistent storage**: all data is stored in a local sqlite database, ensuring your information is saved between sessions.

## Technologies Used
- **programming language**: python 3.x
- **gui framework**: tkinter
- **database**: sqlite
- **other libraries**: csv, datetime, logging

## Installation

### Prerequisites
- **python 3.x**: ensure you have python installed. you can download it from python's official website.
- **pip**: python's package installer should be available. it typically comes bundled with python installations.

### Steps
1. clone the repository:

    ```bash
    git clone https://github.com/justinlietz93/AssignmentTracker.git
    ```

2. navigate to the project directory:

    ```bash
    cd AssignmentTracker
    ```

3. (optional) create a virtual environment: it's good practice to use a virtual environment to manage dependencies.

    ```bash
    python -m venv venv
    ```

4. activate the virtual environment:

    - **windows**:

      ```bash
      venv\scripts\activate
      ```

    - **macos/linux**:

      ```bash
      source venv/bin/activate
      ```

5. install dependencies: since the application primarily uses standard libraries, there are no additional dependencies to install. however, if you add external libraries in the future, you can install them using:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Launching the Application
run the `main.py` file to start the assignment tracker application.

```bash
python main.py
```
## Managing Courses (Tabs)
tabs represent different courses or categories for your assignments.

- **add a new course**:
  - navigate to `tabs > add tab` in the menu bar.
  - enter the name of the new course and confirm.

- **rename an existing course**:
  - navigate to `tabs > rename tab`.
  - select the course you want to rename and provide a new name.

- **delete a course**:
  - navigate to `tabs > delete tab`.
  - select the course you wish to remove. note: deleting a course will also delete all assignments associated with it.

## Managing Assignments
within each course tab, you can manage your assignments.

- **add an assignment**:
  - click the `add assignment` button or navigate to `file > add assignment` (if available).
  - enter the assignment title and due date. optionally, add notes.

- **view assignments**:
  - assignments are listed in a table with columns for assignment title, due date, and status.

- **edit an assignment**:
  - double-click on an assignment to open the assignment details window.
  - modify the notes or other details and click `save`.

- **mark as completed**:
  - select one or more assignments and click the `complete` button.
  - alternatively, right-click on an assignment and select `mark as completed` from the context menu.

- **delete assignments**:
  - select one or more assignments and click the `delete` button.
  - alternatively, right-click on an assignment and select `delete assignment` from the context menu.

## Importing Assignments via CSV
you can import assignments from a csv file to populate your tracker quickly.

- **csv format**: the csv file should have headers: `assignment_title`, `due_date`, and optionally `notes`.

  example:

  ```csv
  assignment_title,due_date,notes
  math homework 1,2024-10-15,chapter 5 problems
  physics lab report,2024-10-20,include graphs and analysis
  ```
## Importing Assignments via CSV
- navigate to `import > import csv` in the menu bar.
- select your csv file.
- the assignments will be imported into the currently selected course tab.

## Viewing the Dashboard
the dashboard provides an overview of your top 10 upcoming pending assignments across all courses.

- **accessing the dashboard**:
  - navigate to `view > dashboard` in the menu bar.

- **features**:
  - **top 10 assignments**: displays the closest due assignments.
  - **refresh**: click the `refresh` button to update the dashboard with the latest data.
  - **navigate to assignment**: double-click on an assignment in the dashboard to jump directly to it in the main window.

## Editing Assignment Notes
each assignment can have detailed notes associated with it.

- **add/edit notes**:
  - double-click on an assignment to open the assignment details window.
  - in the notes section, enter or modify your notes.
  - click `save` to update the notes.

- **note features**:
  - supports multiline text.
  - useful for adding file paths, links, or additional information relevant to the assignment.

## Contributing
contributions are welcome! if you'd like to enhance the assignment tracker, please follow these steps:

1. fork the repository

2. create a new branch:

    ```bash
    git checkout -b feature/yourfeaturename
    ```

3. commit your changes:

    ```bash
    git commit -m "add a new feature"
    ```

4. push to the branch:

    ```bash
    git push origin feature/yourfeaturename
    ```

5. open a pull request

please ensure your contributions adhere to the project's coding standards and include appropriate documentation and tests.

## Contact
if you have any questions, suggestions, or feedback, feel free to reach out:

- **email**: jlietz93@gmail.com
- **github**: [https://github.com/justinlietz93](https://github.com/justinlietz93)
