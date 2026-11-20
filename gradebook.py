# Student Gradebook Manager - ICT102 Assessment 3
# Student: Noman Khan | ID: SM20254113 | Project B
# This program manages student records with marks, grades and ranking
# repo : https://github.com/Nomankhan-13/SM20254113_A3
import csv
import os

# ---------- File paths ----------
# Paths are built from the location of this .py file, so the program
# works no matter which folder it is run from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILENAME = os.path.join(DATA_DIR, "students.csv")
FIELDNAMES = ["student_id", "name", "mark1", "mark2", "mark3", "final_mark", "grade"]

# ---------- Global data list ----------
students = []   # list of dictionaries

# Grade boundaries (same as uni policy)
def get_grade(final_mark):
    if final_mark >= 85:
        return "HD"
    elif final_mark >= 75:
        return "DN"
    elif final_mark >= 65:
        return "CR"
    elif final_mark >= 50:
        return "PS"
    else:
        return "FL"

# ---------- Recursive function (FR10) ----------
# This function recursively calculates the total of all final marks
# used later for class average. Has clear base case and recursive case.
def recursive_sum(marks_list, index=0):
    # base case
    if index >= len(marks_list):
        return 0
    # recursive case
    return marks_list[index] + recursive_sum(marks_list, index + 1)

# ---------- File handling (FR9) ----------
def load_data():
    global students
    students = []

    # make sure the data folder exists (fixes crash when folder is missing)
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(FILENAME):
        # create empty file with header if not exist
        with open(FILENAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDNAMES)
        print("No existing data file found. New file created.")
        return

    skipped = 0
    with open(FILENAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            # check each row on its own, so one bad row does not
            # wipe out all the other records
            try:
                m1 = float(row["mark1"])
                m2 = float(row["mark2"])
                m3 = float(row["mark3"])
                if not (is_valid_mark(m1) and is_valid_mark(m2) and is_valid_mark(m3)):
                    raise ValueError("mark out of range")
                if row["student_id"].strip() == "" or row["name"].strip() == "":
                    raise ValueError("empty ID or name")
            except (ValueError, TypeError, KeyError, AttributeError):
                print(f"Warning: skipped invalid row on line {line_no}.")
                skipped += 1
                continue
            final = round((m1 + m2 + m3) / 3, 2)
            students.append({
                "student_id": row["student_id"].strip().upper(),
                "name": row["name"].strip(),
                "mark1": m1,
                "mark2": m2,
                "mark3": m3,
                "final_mark": final,
                "grade": get_grade(final)
            })
    print(f"Loaded {len(students)} student records successfully.")
    if skipped > 0:
        print(f"{skipped} invalid row(s) were skipped.")

def save_data():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(FILENAME, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for s in students:
                writer.writerow(s)
        print("Data saved to file.")
    except Exception as e:
        print("Error saving data:", e)

# ---------- Input helpers with validation (FR11) ----------
def get_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("Input cannot be empty. Please try again.")

def is_valid_mark(value):
    # value != value is only True for NaN ("not a number")
    return value == value and 0 <= value <= 100

def get_float(prompt, min_val=0, max_val=100):
    while True:
        try:
            value = float(input(prompt))
            if value != value:   # rejects "nan"
                print("Please enter a valid number.")
                continue
            if value < min_val or value > max_val:
                print(f"Value must be between {min_val} and {max_val}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def get_student_id():
    # IDs are stored in upper case so "s001" and "S001" match
    return get_non_empty("Enter Student ID: ").upper()

# ---------- Display helper (used by view and search) ----------
def print_table(records):
    print(f"{'ID':<12} {'Name':<20} {'M1':>6} {'M2':>6} {'M3':>6} {'Final':>7} {'Grade':>6}")
    print("-" * 70)
    for s in records:
        print(f"{s['student_id']:<12} {s['name']:<20} {s['mark1']:>6.1f} {s['mark2']:>6.1f} {s['mark3']:>6.1f} {s['final_mark']:>7.2f} {s['grade']:>6}")

# ---------- Core functions ----------
def add_student():
    print("\n--- Add New Student ---")
    sid = get_student_id()
    
    # check if ID already exists
    for s in students:
        if s["student_id"] == sid:
            print("Student ID already exists! Cannot add duplicate.")
            return
    
    name = get_non_empty("Enter student name: ")
    print("Enter marks for 3 assessments (0-100):")
    m1 = get_float("Assessment 1 mark: ")
    m2 = get_float("Assessment 2 mark: ")
    m3 = get_float("Assessment 3 mark: ")
    
    # calculate final mark (simple average)
    final = round((m1 + m2 + m3) / 3, 2)
    grade = get_grade(final)
    
    student = {
        "student_id": sid,
        "name": name,
        "mark1": m1,
        "mark2": m2,
        "mark3": m3,
        "final_mark": final,
        "grade": grade
    }
    students.append(student)
    print(f"Student {name} added successfully. Final mark is {final} and grade is {grade}")

def view_all():
    print("\n--- All Student Records ---")
    if len(students) == 0:
        print("No records found.")
        return

    print_table(students)

def search_student():
    print("\n--- Search Student ---")
    print("1. Search by Student ID")
    print("2. Search by Name")
    choice = input("Choose search type (1 or 2): ").strip()    
    results = []
    if choice == "1":
        sid = get_non_empty("Enter Student ID to search: ").upper()
        for s in students:
            if s["student_id"].upper() == sid:
                results.append(s)
    elif choice == "2":
        name = get_non_empty("Enter name (or part of name): ").lower()
        for s in students:
            if name in s["name"].lower():
                results.append(s)
    else:
        print("Invalid choice.")
        return
    
    if len(results) == 0:
        print("No matching records found.")
    else:
        print(f"\nFound {len(results)} record(s):")
        print_table(results)
        
def update_student():
    print("\n--- Update Student Record ---")
    sid = get_non_empty("Enter Student ID to update: ").upper()
    
    target = None
    for s in students:
        if s["student_id"] == sid:
            target = s
            break
    
    if target is None:
        print("Student ID not found.")
        return
    
    print(f"Current record: {target['name']} | Final: {target['final_mark']} | Grade: {target['grade']}")
    print("What do you want to update?")
    print("1. Name")
    print("2. Assessment 1 mark")
    print("3. Assessment 2 mark")
    print("4. Assessment 3 mark")
    print("5. Cancel")
    
    choice = input("Enter choice: ").strip()
    
    if choice == "1":
        target["name"] = get_non_empty("Enter new name: ")
    elif choice == "2":
        target["mark1"] = get_float("Enter new Assessment 1 mark: ")
    elif choice == "3":
        target["mark2"] = get_float("Enter new Assessment 2 mark: ")
    elif choice == "4":
        target["mark3"] = get_float("Enter new Assessment 3 mark: ")
    else:
        print("Update cancelled.")
        return
    
    # recalculate final and grade
    target["final_mark"] = round((target["mark1"] + target["mark2"] + target["mark3"]) / 3, 2)
    target["grade"] = get_grade(target["final_mark"])
    print(f"Record updated. New final mark: {target['final_mark']} | Grade: {target['grade']}")

def delete_student():
    print("\n--- Delete Student Record ---")
    sid = get_non_empty("Enter Student ID to delete: ").upper()
    
    target = None
    index = -1
    for i, s in enumerate(students):
        if s["student_id"] == sid:
            target = s
            index = i
            break
    
    if target is None:
        print("Student ID not found.")
        return
    
    print(f"Found: {target['name']} (Final: {target['final_mark']}, Grade: {target['grade']})")
    confirm = input("Are you sure you want to delete? (Y/N): ").strip().upper()
    if confirm == "Y":
        students.pop(index)
        print("Record deleted successfully.")
    else:
        print("Delete cancelled.")

# ---------- Topic specific operations (FR7) ----------
def calculate_and_rank():
    print("\n--- Calculate Grades & Rank Students ---")
    if len(students) == 0:
        print("No students to rank.")
        return
    
    # grades already calculated on add/update, but we can re-calc to be sure
    for s in students:
        s["final_mark"] = round((s["mark1"] + s["mark2"] + s["mark3"]) / 3, 2)
        s["grade"] = get_grade(s["final_mark"])
    
    # sort by final mark descending for ranking
    ranked = sorted(students, key=lambda x: x["final_mark"], reverse=True)
    
    print(f"{'Rank':<6} {'ID':<12} {'Name':<20} {'Final':>7} {'Grade':>6}")
    print("-" * 55)
    for i, s in enumerate(ranked, 1):
        print(f"{i:<6} {s['student_id']:<12} {s['name']:<20} {s['final_mark']:>7.2f} {s['grade']:>6}")

# ---------- Summary report (FR8) - using own loops + recursion ----------
def summary_report():
    print("\n--- Summary Report ---")
    if len(students) == 0:
        print("No data available for report.")
        return
    
    # collect final marks for recursion
    finals = []
    for s in students:
        finals.append(s["final_mark"])
    
    # use recursive sum for total
    total = recursive_sum(finals)
    average = total / len(finals)
    
    # find highest and lowest with own loop (not built-in max/min)
    highest = finals[0]
    lowest = finals[0]
    for m in finals:
        if m > highest:
            highest = m
        if m < lowest:
            lowest = m
    
    # count per grade with own loops
    hd = dn = cr = ps = fl = 0
    for s in students:
        g = s["grade"]
        if g == "HD":
            hd += 1
        elif g == "DN":
            dn += 1
        elif g == "CR":
            cr += 1
        elif g == "PS":
            ps += 1
        else:
            fl += 1
    
    print(f"Total students      : {len(students)}")
    print(f"Class average      : {average:.2f}")
    print(f"Highest final mark : {highest:.2f}")
    print(f"Lowest final mark  : {lowest:.2f}")
    print("\nGrade distribution:")
    print(f"  HD : {hd}")
    print(f"  DN : {dn}")
    print(f"  CR : {cr}")
    print(f"  PS : {ps}")
    print(f"  FL : {fl}")

# ---------- Main menu (FR1) ----------
def main_menu():
    load_data()
    
    while True:
        print("\n========== STUDENT GRADEBOOK ==========")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Calculate Grades & Rank")
        print("7. Summary Report")
        print("8. Exit")
        print("=======================================")
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == "1":
            add_student()
        elif choice == "2":
            view_all()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            calculate_and_rank()
        elif choice == "7":
            summary_report()
        elif choice == "8":
            save_data()
            print("\nThank you for using the Student Gradebook. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 8.")

# ---------- Entry point ----------
if __name__ == "__main__":
    main_menu()
