import psycopg2
import time

conn = psycopg2.connect(
    host="localhost",
    database="college_db",
    user="postgres",
    password="password"
)

cur = conn.cursor()

start = time.time()

cur.execute("""
SELECT
    e.enrollment_id,
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id
""")

rows = cur.fetchall()

end = time.time()

print("1 query executed")
print("Execution Time:", end - start)

for row in rows:
    print(row)

cur.close()
conn.close()