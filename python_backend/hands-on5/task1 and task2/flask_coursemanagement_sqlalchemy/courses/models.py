from app import db


class Department(db.Model):

    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    head_of_dept = db.Column(db.String(100))

    budget = db.Column(db.Float)

    courses = db.relationship(
        "Course",
        back_populates="department",
        cascade="all, delete"
    )

    students = db.relationship(
        "Student",
        back_populates="department",
        cascade="all, delete"
    )

    def __repr__(self):
        return self.name

    #task 2 changes
    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "head_of_dept": self.head_of_dept,
        "budget": self.budget
    }


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    code = db.Column(db.String(20), unique=True)

    credits = db.Column(db.Integer)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )

    department = db.relationship(
        "Department",
        back_populates="courses"
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete"
    )

    def __repr__(self):
        return self.name
    
    #task 2 changes
    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "code": self.code,
        "credits": self.credits,
        "department_id": self.department_id
    }


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100))

    last_name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    enrollment_year = db.Column(db.Integer)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )

    department = db.relationship(
        "Department",
        back_populates="students"
    )

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete"
    )

    def __repr__(self):
        return self.first_name
    
    #task 2 changes
    def to_dict(self):
        return {
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "enrollment_year": self.enrollment_year,
        "department_id": self.department_id
    }


class Enrollment(db.Model):

    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    enrollment_date = db.Column(db.Date)

    grade = db.Column(db.String(5))

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id")
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id")
    )

    student = db.relationship(
        "Student",
        back_populates="enrollments"
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "course_id",
            name="unique_enrollment"
        ),
    )

    def __repr__(self):
        return f"{self.student_id}-{self.course_id}"
    
    #task 2 changes
    def to_dict(self):
        return {
        "id": self.id,
        "student_id": self.student_id,
        "course_id": self.course_id,
        "enrollment_date": str(self.enrollment_date),
        "grade": self.grade
    }