import sqlite3
import os

def create_tables(cursor):
    """Create database tables with indexes"""
    # students table
    cursor.execute('''
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_year INTEGER NOT NULL
    )''')

    # grades table
    cursor.execute('''
    CREATE TABLE grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    )''')

    # indexes
    indexes = [
        "CREATE INDEX idx_students_birth_year ON students(birth_year)",
        "CREATE INDEX idx_grades_student_id ON grades(student_id)",
        "CREATE INDEX idx_grades_subject ON grades(subject)",
        "CREATE INDEX idx_grades_grade ON grades(grade)",
        "CREATE INDEX idx_students_name ON students(full_name)"
    ]

    for index_sql in indexes:
        cursor.execute(index_sql)

    # print("Tables and indexes created successfully")


def insert_data(cursor):
    """Insert sample data into tables"""
    students = [
        ('Alice Johnson', 2005), ('Brian Smith', 2004), ('Carla Reyes', 2006),
        ('Daniel Kim', 2005), ('Eva Thompson', 2003), ('Felix Nguyen', 2007),
        ('Grace Patel', 2005), ('Henry Lopez', 2004), ('Isabella Martinez', 2006)
    ]

    grades = [
        (1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
        (2, 'Math', 75), (2, 'History', 83), (2, 'English', 79),
        (3, 'Science', 95), (3, 'Math', 91), (3, 'Art', 89),
        (4, 'Math', 84), (4, 'Science', 88), (4, 'PE', 93),
        (5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
        (6, 'Science', 72), (6, 'Math', 78), (6, 'English', 81),
        (7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
        (8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
        (9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92)
    ]

    cursor.executemany("INSERT INTO students (full_name, birth_year) VALUES (?, ?)", students)
    cursor.executemany("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", grades)
    print(f"Inserted {len(students)} students and {len(grades)} grades")


def run_query(cursor, query, description):
    """Execute a single query and display results"""
    print(f"\n{description}:")
    cursor.execute(query)

    for row in cursor.fetchall():
        print(" ", *row)


def main():
    """Main function to set up database and run queries"""
    # Remove old database if exists
    if os.path.exists('school.db'):
        os.remove('school.db')

    # Connect to database
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    # Setup database
    create_tables(cursor)
    insert_data(cursor)
    conn.commit()

    # Define all required queries
    queries = [
        # Query 3: All grades for Alice Johnson
        ('''SELECT s.full_name, g.subject, g.grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE s.full_name = 'Alice Johnson'
            ORDER BY g.subject''',
         "All grades for Alice Johnson"),

        # Query 4: Average grade per student
        ('''SELECT s.full_name, ROUND(AVG(g.grade), 2)
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id
            ORDER BY AVG(g.grade) DESC''',
         "Average grade per student"),

        # Query 5: Students born after 2004
        ('''SELECT full_name, birth_year
            FROM students
            WHERE birth_year > 2004
            ORDER BY birth_year DESC''',
         "Students born after 2004"),

        # Query 6: Subjects and average grades
        ('''SELECT subject, ROUND(AVG(grade), 2), COUNT(*)
            FROM grades
            GROUP BY subject
            ORDER BY AVG(grade) DESC''',
         "Subjects and average grades"),

        # Query 7: Top 3 students
        ('''SELECT s.full_name, ROUND(AVG(g.grade), 2)
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id
            ORDER BY AVG(g.grade) DESC
            LIMIT 3''',
         "Top 3 students with highest average"),

        # Query 8: Students with grades below 80
        ('''SELECT DISTINCT s.full_name, g.subject, g.grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE g.grade < 80
            ORDER BY s.full_name, g.grade''',
         "Students with grades below 80")
    ]

    # Execute all queries
    print("QUERY RESULTS")

    for query, description in queries:
        run_query(cursor, query, description)

    # Show database stats
    print("\nDATABASE STATISTICS")

    stats = [
        ("Total students:", "SELECT COUNT(*) FROM students"),
        ("Total grades:", "SELECT COUNT(*) FROM grades"),
        ("Unique subjects:", "SELECT COUNT(DISTINCT subject) FROM grades"),
        ("Overall average:", "SELECT ROUND(AVG(grade), 2) FROM grades")
    ]

    for label, query in stats:
        cursor.execute(query)
        value = cursor.fetchone()[0]
        print(f"{label:20} {value}")

    # Export SQL file
    with open('school_queries.sql', 'w') as f:
        f.write("-- SQL queries for school database\n")
        for query, desc in queries:
            f.write(f"\n-- {desc}\n{query};\n")
    print("\nSQL queries saved to 'school_queries.sql'")

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()