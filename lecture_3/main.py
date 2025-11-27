def main():
    students = []
    print("Student Grade Analyzer - Starting!")

    while True:
        try:
            print("STUDENT GRADE ANALYZER")
            print("-" * 50)
            print("1. Add new student")
            print("2. Add grades for student")
            print("3. Show report (all students)")
            print("4. Find top performer")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                name = input("Enter student name: ").strip()

                student_exists = False
                for student in students:
                    if student["name"].lower() == name.lower():
                        student_exists = True
                        break

                if student_exists:
                    print(f"Student '{name}' already exists!")
                else:
                    new_student = {"name": name, "grades": []}
                    students.append(new_student)
                    print(f"Student '{name}' added successfully!")

            elif choice == '2':
                if not students:
                    print("No students available! Add students first.")
                    continue

                name = input("Enter student name: ").strip()
                student_found = None

                for student in students:
                    if student["name"].lower() == name.lower():
                        student_found = student
                        break

                if not student_found:
                    print(f"Student '{name}' not found!")
                else:
                    print(f"Adding grades for {student_found['name']}:")
                    while True:
                        grade_input = input("Enter grade (0-100) or 'done': ").strip().lower()

                        if grade_input == 'done':
                            break

                        try:
                            grade = int(grade_input)
                            if 0 <= grade <= 100:
                                student_found["grades"].append(grade)
                                print(f"Grade {grade} added.")
                            else:
                                print("Grade must be between 0 and 100!")
                        except ValueError:
                            print("Invalid input! Please enter a number.")

            elif choice == '3':
                if not students:
                    print("No students available for report!")
                    continue

                print("\n--- STUDENT REPORT ---")
                averages = []

                for student in students:
                    if student["grades"]:
                        try:
                            avg = sum(student["grades"]) / len(student["grades"])
                            print(f"🎓 {student['name']}: average grade {avg:.1f}")
                            averages.append(avg)
                        except ZeroDivisionError:
                            print(f"🎓 {student['name']}: N/A (no grades)")
                    else:
                        print(f"🎓 {student['name']}: N/A (no grades)")

                if averages:
                    print("\n--- STATISTICS ---")
                    print(f"Max Average: {max(averages):.1f}")
                    print(f"Min Average: {min(averages):.1f}")
                    print(f"Overall Average: {sum(averages) / len(averages):.1f}")
                else:
                    print("\nℹNo grades available for statistics.")

            elif choice == '4':
                if not students:
                    print("No students available!")
                    continue

                students_with_grades = [s for s in students if s["grades"]]

                if not students_with_grades:
                    print("No students with grades available!")
                    continue

                try:
                    top_student = max(students_with_grades,
                                      key=lambda s: sum(s["grades"]) / len(s["grades"]))

                    top_avg = sum(top_student["grades"]) / len(top_student["grades"])
                    print(f"TOP PERFORMER: {top_student['name']}")
                    print(f"Average Grade: {top_avg:.1f}")
                    print(f"Total Grades: {len(top_student['grades'])}")

                except Exception as e:
                    print(f"Error finding top performer: {e}")

            elif choice == '5':
                print("\nThank you for using Student Grade Analyzer! Goodbye!")
                break

            else:
                print("Invalid choice! Please enter number 1-5.")

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()