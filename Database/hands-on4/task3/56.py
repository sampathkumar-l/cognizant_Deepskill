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

query_count = 0

cur.execute("SELECT * FROM enrollments")
enrollments = cur.fetchall()
query_count += 1

for enrollment in enrollments:
    student_id = enrollment[1]

    cur.execute(
        "SELECT first_name, last_name FROM students WHERE student_id = %s",
        (student_id,)
    )

    cur.fetchone()
    query_count += 1

end = time.time()

print("Queries Executed:", query_count)
print("Execution Time:", end - start)

cur.close()
conn.close()