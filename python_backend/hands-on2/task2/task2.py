from courses.models import Department, Course, Student
from django.db.models import Count, F
from django.db import connection

# -------------------------------
# Create Departments
# -------------------------------
cs = Department.objects.create(
    name="Computer Science",
    head_of_dept="Dr. John",
    budget=500000
)

ece = Department.objects.create(
    name="Electronics",
    head_of_dept="Dr. Smith",
    budget=400000
)

# -------------------------------
# Create Courses
# -------------------------------
Course.objects.create(
    name="Python Programming",
    code="CS101",
    credits=4,
    department=cs
)

Course.objects.create(
    name="Data Structures",
    code="CS102",
    credits=4,
    department=cs
)

Course.objects.create(
    name="Digital Electronics",
    code="EC101",
    credits=3,
    department=ece
)

Course.objects.create(
    name="Microprocessors",
    code="EC102",
    credits=4,
    department=ece
)

# -------------------------------
# Create Students
# -------------------------------
Student.objects.create(
    first_name="Alice",
    last_name="Johnson",
    email="alice@example.com",
    department=cs,
    enrollment_year=2024
)

Student.objects.create(
    first_name="Bob",
    last_name="Smith",
    email="bob@example.com",
    department=cs,
    enrollment_year=2023
)

Student.objects.create(
    first_name="Charlie",
    last_name="Brown",
    email="charlie@example.com",
    department=ece,
    enrollment_year=2024
)

Student.objects.create(
    first_name="David",
    last_name="Lee",
    email="david@example.com",
    department=ece,
    enrollment_year=2022
)

Student.objects.create(
    first_name="Eva",
    last_name="Wilson",
    email="eva@example.com",
    department=cs,
    enrollment_year=2025
)

print("=" * 50)
print("Departments, Courses, and Students Created")
print("=" * 50)

# -------------------------------------------------
# Query all courses in Computer Science Department
# -------------------------------------------------
print("\nCourses in Computer Science Department:")

courses = Course.objects.filter(
    department__name="Computer Science"
)

for course in courses:
    print(f"{course.name} ({course.code})")

# -------------------------------------------------
# Count courses per department
# -------------------------------------------------
print("\nCourse Count per Department:")

departments = Department.objects.annotate(
    course_count=Count("course")
)

for dept in departments:
    print(f"{dept.name}: {dept.course_count}")

# -------------------------------------------------
# select_related Example
# -------------------------------------------------
print("\nStudents with Department (select_related):")

connection.queries.clear()

students = Student.objects.select_related("department")

for student in students:
    print(
        f"{student.first_name} {student.last_name} "
        f"-> {student.department.name}"
    )

print("\nTotal SQL Queries Executed:")
print(len(connection.queries))

# -------------------------------------------------
# Update Department Budget by 10%
# -------------------------------------------------
Department.objects.update(
    budget=F("budget") * 1.10
)

print("\nUpdated Department Budgets:")

for dept in Department.objects.all():
    print(f"{dept.name}: {dept.budget}")

print("\nTask 2 Completed Successfully.")