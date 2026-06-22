from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Time,
    Numeric,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import declarative_base, relationship

# ==========================================================
# Database Connection
# ==========================================================

DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/college_db_orm"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()

# ==========================================================
# Department Model
# ==========================================================

class Department(Base):

    __tablename__ = "departments"

    department_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    dept_name = Column(
        String(100),
        nullable=False
    )

    head_of_dept = Column(
        String(100)
    )

    budget = Column(
        Numeric(12,2)
    )

    students = relationship(
        "Student",
        back_populates="department"
    )

    courses = relationship(
        "Course",
        back_populates="department"
    )

    professors = relationship(
        "Professor",
        back_populates="department"
    )


# ==========================================================
# Student Model
# ==========================================================

class Student(Base):

    __tablename__ = "students"

    student_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = Column(
        String(50),
        nullable=False
    )

    last_name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    date_of_birth = Column(Date)

    enrollment_year = Column(Integer)

    # Hands-On 7 Migration
    is_active = Column(
        Boolean,
        default=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="students"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )


# ==========================================================
# Course Model
# ==========================================================

class Course(Base):

    __tablename__ = "courses"

    course_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    course_name = Column(
        String(150),
        nullable=False
    )

    course_code = Column(
        String(20),
        unique=True
    )

    credits = Column(Integer)

    max_seats = Column(
        Integer,
        default=60
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="courses"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )

    schedules = relationship(
        "CourseSchedule",
        back_populates="course"
    )


# ==========================================================
# Enrollment Model
# ==========================================================

class Enrollment(Base):

    __tablename__ = "enrollments"

    enrollment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.student_id")
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.course_id")
    )

    enrollment_date = Column(Date)

    grade = Column(String(2))

    student = relationship(
        "Student",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )


# ==========================================================
# Professor Model
# ==========================================================

class Professor(Base):

    __tablename__ = "professors"

    professor_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    prof_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True
    )

    salary = Column(
        Numeric(10,2)
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="professors"
    )


# ==========================================================
# Hands-On 7
# Course Schedule Model
# ==========================================================

class CourseSchedule(Base):

    __tablename__ = "course_schedules"

    schedule_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.course_id")
    )

    day_of_week = Column(
        String(20),
        nullable=False
    )

    start_time = Column(Time)

    end_time = Column(Time)

    course = relationship(
        "Course",
        back_populates="schedules"
    )


# ==========================================================
# Create Tables
# ==========================================================

if __name__ == "__main__":

    Base.metadata.create_all(engine)

    print("=" * 50)
    print("All tables created successfully.")
    print("=" * 50)

# ==========================================
# UPDATE TASK
# ==========================================

print("\nUpdating Student Enrollment Year...\n")

student = (
    session.query(Student)
    .filter(
        Student.email == "arjun@college.edu"
    )
    .first()
)

if student:

    print("Before Update")

    print(
        student.first_name,
        student.enrollment_year
    )

    student.enrollment_year = 2024

    session.commit()

    print("After Update")

    print(
        student.first_name,
        student.enrollment_year
    )

# ==========================================
# DELETE TASK
# ==========================================

print("\nDeleting One Enrollment...\n")

enrollment = (
    session.query(Enrollment)
    .first()
)

if enrollment:

    session.delete(enrollment)

    session.commit()

    print("One enrollment deleted successfully.")

# ==========================================
# VERIFY DELETE
# ==========================================

print("\nRemaining Enrollments\n")

for enrollment in session.query(Enrollment).all():

    print(
        enrollment.enrollment_id,
        enrollment.student.first_name,
        enrollment.course.course_name
    )

# ==========================================
# N+1 QUERY DEMONSTRATION
# ==========================================

print("\nN + 1 Query Demonstration\n")

enrollments = session.query(Enrollment).all()

for enrollment in enrollments:

    print(
        enrollment.student.first_name,
        enrollment.course.course_name,
        enrollment.grade
    )

print("\nNotice:")
print("With echo=True, SQLAlchemy executes")
print("multiple SELECT statements (N+1 Problem).")

# ==========================================
# JOINEDLOAD SOLUTION
# ==========================================

print("\nOptimized Query Using joinedload()\n")

optimized = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    )
    .all()
)

for enrollment in optimized:

    print(
        enrollment.student.first_name,
        enrollment.course.course_name,
        enrollment.grade
    )

print("\nOnly one SQL query is executed using joinedload().")

# ==========================================
# BONUS
# ==========================================

print("\nAll Departments\n")

for department in session.query(Department).all():

    print(
        department.department_id,
        department.dept_name,
        department.head_of_dept
    )

print("\nAll Courses\n")

for course in session.query(Course).all():

    print(
        course.course_code,
        course.course_name,
        course.credits
    )

print("\nAll Professors\n")

for professor in session.query(Professor).all():

    print(
        professor.prof_name,
        professor.salary
    )

# ==========================================
# CLOSE SESSION
# ==========================================

session.close()

print("\nSession Closed Successfully.")