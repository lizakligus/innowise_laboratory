-- SQL queries for school database

-- All grades for Alice Johnson
SELECT s.full_name, g.subject, g.grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE s.full_name = 'Alice Johnson'
            ORDER BY g.subject;

-- Average grade per student
SELECT s.full_name, ROUND(AVG(g.grade), 2)
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id
            ORDER BY AVG(g.grade) DESC;

-- Students born after 2004
SELECT full_name, birth_year
            FROM students
            WHERE birth_year > 2004
            ORDER BY birth_year DESC;

-- Subjects and average grades
SELECT subject, ROUND(AVG(grade), 2), COUNT(*)
            FROM grades
            GROUP BY subject
            ORDER BY AVG(grade) DESC;

-- Top 3 students with highest average
SELECT s.full_name, ROUND(AVG(g.grade), 2)
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id
            ORDER BY AVG(g.grade) DESC
            LIMIT 3;

-- Students with grades below 80
SELECT DISTINCT s.full_name, g.subject, g.grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE g.grade < 80
            ORDER BY s.full_name, g.grade;
