import sqlite3
import re

DB_NAME = "students.db"


# ---------- DATABASE HELPERS ----------

def get_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us access row values by column name
    return conn


def create_table():
    """Creates the students table if it does not already exist."""
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)
    conn.close()


def run_query(query, params=(), fetch=False):
    """Runs a query. If fetch=True, returns the rows."""
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(query, params)
            if fetch:
                return cursor.fetchall()
            return cursor.rowcount
    finally:
        conn.close()


# ---------- VALIDATION HELPERS ----------

def is_valid_name(value):
    return value.replace(" ", "").isalpha()


def is_valid_roll_no(value):
    return value.isalnum()


def is_valid_email(value):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) is not None


def is_valid_phone(value):
    return value.isdigit() and len(value) == 10


def is_not_empty(value):
    return len(value) > 0


def get_input(label, validator, error_msg, default=None):
    """
    Takes valid input from the user.
    If a default is given, pressing Enter keeps the old value (used for update).
    """
    while True:
        if default is not None:
            value = input(f"{label} [{default}]: ").strip()
            if value == "":
                return default
        else:
            value = input(f"{label}: ").strip()

        if validator(value):
            return value
        print("❌", error_msg)


# ---------- DISPLAY HELPER ----------

def print_table(rows):
    """Prints students in a formatted table."""
    line = "-" * 95
    print(line)
    print(f"{'ID':<5}{'Name':<20}{'Roll No':<12}{'Course':<15}{'Email':<26}{'Phone':<12}")
    print(line)
    for r in rows:
        print(f"{r['id']:<5}{r['name']:<20}{r['roll_no']:<12}{r['course']:<15}{r['email']:<26}{r['phone']:<12}")
    print(line)


# ---------- MAIN FEATURES ----------

def add_student():
    print("\n--- Add New Student ---")
    name = get_input("Name", is_valid_name, "Name can only contain letters and spaces.")
    roll_no = get_input("Roll No", is_valid_roll_no, "Roll No can only contain letters/numbers and cannot be empty.")
    course = get_input("Course", is_not_empty, "Course cannot be empty.")
    email = get_input("Email", is_valid_email, "Enter a valid email (example@gmail.com).")
    phone = get_input("Phone (10 digits)", is_valid_phone, "Phone number must be 10 digits.")

    try:
        run_query(
            "INSERT INTO students (name, roll_no, course, email, phone) VALUES (?, ?, ?, ?, ?)",
            (name, roll_no, course, email, phone),
        )
        print("✅ Student added successfully!")
    except sqlite3.IntegrityError:
        # roll_no is UNIQUE, so this error appears for a duplicate
        print(f"❌ Roll No '{roll_no}' already exists!")


def view_students():
    print("\n--- All Students ---")
    rows = run_query("SELECT * FROM students ORDER BY id", fetch=True)
    if not rows:
        print("No students found yet.")
        return
    print_table(rows)


def search_student():
    print("\n--- Search Student ---")
    print("1. By Roll No")
    print("2. By Name")
    choice = input("Choice (1/2): ").strip()

    if choice == "1":
        roll_no = input("Roll No: ").strip()
        rows = run_query("SELECT * FROM students WHERE roll_no = ?", (roll_no,), fetch=True)
    elif choice == "2":
        name = input("Name (or part of it): ").strip()
        rows = run_query("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",), fetch=True)
    else:
        print("❌ Invalid choice.")
        return

    if rows:
        print_table(rows)
    else:
        print("❌ No student found.")


def update_student():
    print("\n--- Update Student ---")
    roll_no = input("Enter the Roll No of the student to update: ").strip()
    rows = run_query("SELECT * FROM students WHERE roll_no = ?", (roll_no,), fetch=True)

    if not rows:
        print("❌ No student found with this Roll No.")
        return

    student = rows[0]
    print("(Press Enter to keep the current value)")
    name = get_input("Name", is_valid_name, "Name can only contain letters and spaces.", student["name"])
    course = get_input("Course", is_not_empty, "Course cannot be empty.", student["course"])
    email = get_input("Email", is_valid_email, "Enter a valid email.", student["email"])
    phone = get_input("Phone (10 digits)", is_valid_phone, "Phone must be 10 digits.", student["phone"])

    run_query(
        "UPDATE students SET name = ?, course = ?, email = ?, phone = ? WHERE roll_no = ?",
        (name, course, email, phone, roll_no),
    )
    print("✅ Student details updated successfully!")


def delete_student():
    print("\n--- Delete Student ---")
    roll_no = input("Enter the Roll No of the student to delete: ").strip()
    rows = run_query("SELECT * FROM students WHERE roll_no = ?", (roll_no,), fetch=True)

    if not rows:
        print("❌ No student found with this Roll No.")
        return

    print_table(rows)
    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()

    if confirm == "y":
        run_query("DELETE FROM students WHERE roll_no = ?", (roll_no,))
        print("✅ Student deleted successfully!")
    else:
        print("↩️  Deletion cancelled.")


# ---------- MENU ----------

def show_menu():
    print("\n" + "=" * 45)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("=" * 45)
    print("  1. Add Student")
    print("  2. View All Students")
    print("  3. Search Student")
    print("  4. Update Student")
    print("  5. Delete Student")
    print("  6. Exit")
    print("=" * 45)


def main():
    create_table()

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                print("👋 Exiting the program. Bye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number from 1 to 6.")
        except sqlite3.Error as e:
            print("❌ Database error:", e)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handles Ctrl+C so the program exits cleanly
        print("\n👋 Program stopped.")