from sqlalchemy import Column,Integer,String,Float,ForeignKey,Date,UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__='departments'
    id=Column(Integer,primary_key=True)
    name=Column(String(100),nullable=False)
    head_of_dept=Column(String(100))
    budget=Column(Float)
    courses=relationship('Course',back_populates='department')
    students=relationship('Student',back_populates='department')

class Course(Base):
    __tablename__='courses'
    id=Column(Integer,primary_key=True)
    name=Column(String(100),nullable=False)
    code=Column(String(20),unique=True)
    credits=Column(Integer)
    department_id=Column(Integer,ForeignKey('departments.id'))
    department=relationship('Department',back_populates='courses')
    enrollments=relationship('Enrollment',back_populates='course')

class Student(Base):
    __tablename__='students'
    id=Column(Integer,primary_key=True)
    first_name=Column(String(100))
    last_name=Column(String(100))
    email=Column(String(100),unique=True)
    enrollment_year=Column(Integer)
    department_id=Column(Integer,ForeignKey('departments.id'))
    department=relationship('Department',back_populates='students')
    enrollments=relationship('Enrollment',back_populates='student')

class Enrollment(Base):
    __tablename__='enrollments'
    id=Column(Integer,primary_key=True)
    enrollment_date=Column(Date)
    grade=Column(String(10))
    student_id=Column(Integer,ForeignKey('students.id'))
    course_id=Column(Integer,ForeignKey('courses.id'))
    student=relationship('Student',back_populates='enrollments')
    course=relationship('Course',back_populates='enrollments')
    __table_args__=(UniqueConstraint('student_id','course_id',name='uq_enroll'),)
