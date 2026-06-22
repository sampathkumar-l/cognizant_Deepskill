from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from datetime import date
from models import *

engine=create_engine(DATABASE_URL, echo=True)
Session=sessionmaker(bind=engine)
session=Session()

# INSERT departments
if session.query(Department).count()==0:
    d1=Department(dept_name="Computer Science",head_of_dept="Dr. Ramesh",budget=850000)
    d2=Department(dept_name="Electronics",head_of_dept="Dr. Priya",budget=620000)
    d3=Department(dept_name="Mechanical",head_of_dept="Dr. Suresh",budget=540000)
    session.add_all([d1,d2,d3]); session.commit()

# INSERT students
if session.query(Student).count()==0:
    deps=session.query(Department).all()
    session.add_all([
        Student(first_name="Arjun",last_name="Mehta",email="arjun@college.edu",date_of_birth=date(2003,4,12),enrollment_year=2022,department=deps[0]),
        Student(first_name="Priya",last_name="Suresh",email="priya@college.edu",date_of_birth=date(2003,7,25),enrollment_year=2022,department=deps[0]),
        Student(first_name="Rohan",last_name="Verma",email="rohan@college.edu",date_of_birth=date(2002,11,8),enrollment_year=2021,department=deps[1]),
        Student(first_name="Sneha",last_name="Patel",email="sneha@college.edu",date_of_birth=date(2004,1,30),enrollment_year=2023,department=deps[2]),
        Student(first_name="Vikram",last_name="Das",email="vikram@college.edu",date_of_birth=date(2003,9,14),enrollment_year=2022,department=deps[0])
    ]); session.commit()

print("Computer Science Students:")
for s in session.query(Student).join(Department).filter(Department.dept_name=="Computer Science"):
    print(s.first_name,s.last_name)

print("\nEager Loading Example")
for e in session.query(Enrollment).options(joinedload(Enrollment.student),joinedload(Enrollment.course)).all():
    print(e.student.first_name if e.student else "", e.course.course_name if e.course else "")

st=session.query(Student).filter_by(email="arjun@college.edu").first()
if st:
    st.enrollment_year=2024
    session.commit()

session.close()
