# Student Management System

A command-line **Student Management System** built with **Python** and **SQLite**. You can add, view, search, update, and delete student records from a simple menu.

## Features

- Add a new student with input validation
- View all students in a table
- Search a student by Roll No or Name
- Update student details (press Enter to keep the old value)
- Delete a student with confirmation
- Duplicate Roll No check using a UNIQUE constraint
- Error handling with try/except
- Safe SQL queries using parameterized statements

## Tech Stack

- **Language:** Python 3
- **Database:** SQLite (built-in `sqlite3` module)
- **Validation:** `re` module for email check

## Validation Rules

| Field   | Rule                                      |
|---------|-------------------------------------------|
| Name    | Only letters and spaces                   |
| Roll No | Letters and numbers only, cannot be empty |
| Course  | Cannot be empty                           |
| Email   | Valid format, e.g. `example@gmail.com`    |
| Phone   | Exactly 10 digits                         |

## Project Structure

```
student_management_system/
│
├── main.py       # Main program
├── students.db   # SQLite database (created automatically)
├── .gitignore    # Files Git should ignore
└── README.md     # Project documentation
```

## How to Run

1. Make sure Python 3.8 or higher is installed.
2. Open the project folder in terminal.
3. Run:

```bash
python main.py
```

(On Mac/Linux, use `python3 main.py`)

The database and the `students` table are created automatically on the first run.

## Menu

```
=============================================
       STUDENT MANAGEMENT SYSTEM
=============================================
  1. Add Student
  2. View All Students
  3. Search Student
  4. Update Student
  5. Delete Student
  6. Exit
=============================================
```

## Concepts Used

- Functions
- `while` loop menu
- Conditionals and input handling
- SQLite CRUD operations (INSERT, SELECT, UPDATE, DELETE)
- Regular expressions for validation
- Exception handling

## Author

**Sejal Mishra**
BCA Final Year Student