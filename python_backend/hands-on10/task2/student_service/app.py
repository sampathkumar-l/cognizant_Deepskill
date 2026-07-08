"""
Student Service - owns Student + Enrollment data in its own database
(students.db), completely separate from Course Service's courses.db.

NEW in Task 2: POST /api/students/<id>/enroll  [step 100]
  This endpoint needs to know whether a course exists, but Course Service
  owns that data - Student Service is NOT allowed to query courses.db
  directly. So it makes a synchronous HTTP call to Course Service's own
  API: GET /api/courses/{id}/.

  If Course Service is unreachable, the requests call raises
  ConnectionError, which is caught and turned into a 503 Service
  Unavailable response  [step 101] - callers get a clear signal that the
  *dependency* is down, distinct from a 404 (course simply doesn't exist)
  or a 400 (bad input).
"""

import os

import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# In a real deployment this would come from service discovery / an env var
# per-environment; a plain env var with a sane local default is enough here.
COURSE_SERVICE_URL = os.getenv("COURSE_SERVICE_URL", "http://127.0.0.1:5001")


# ---------------------------------------------------------------- Models

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_year": self.enrollment_year,
        }


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (db.UniqueConstraint("student_id", "course_id", name="uq_student_course"),)

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    # course_id is just an int here on purpose - Student Service does NOT
    # have a foreign key into Course Service's database (that would defeat
    # the whole point of separate databases). Referential integrity across
    # services is instead enforced at request time via the HTTP call below.
    course_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "student_id": self.student_id, "course_id": self.course_id}


with app.app_context():
    db.create_all()


def error(status_code, message):
    return jsonify({"error": {"code": status_code, "message": message}}), status_code


# ---------------------------------------------------------------- Health

@app.get("/health")
def health():
    return jsonify({"service": "student-service", "status": "ok"})


# ---------------------------------------------------------------- Students

@app.get("/api/students/")
def list_students():
    return jsonify([s.to_dict() for s in Student.query.all()])


@app.post("/api/students/")
def create_student():
    data = request.get_json(silent=True) or {}
    required = {"first_name", "last_name", "email"}
    if not required.issubset(data):
        return error(400, f"Missing required fields: {required - set(data)}")

    student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        enrollment_year=data.get("enrollment_year"),
    )
    db.session.add(student)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return error(400, "Email must be unique")

    return jsonify(student.to_dict()), 201


@app.get("/api/students/<int:student_id>/")
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error(404, f"Student with id {student_id} does not exist")
    return jsonify(student.to_dict())


@app.delete("/api/students/<int:student_id>/")
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error(404, f"Student with id {student_id} does not exist")
    db.session.delete(student)
    db.session.commit()
    return "", 204


# ---------------------------------------------------------------- Enrollment  [step 100/101]

@app.post("/api/students/<int:student_id>/enroll")
def enroll_student(student_id):
    """
    Enroll a student in a course. Verifies the course exists by calling
    Course Service's own API - this is the inter-service call.
    """
    student = Student.query.get(student_id)
    if not student:
        return error(404, f"Student with id {student_id} does not exist")

    data = request.get_json(silent=True) or {}
    course_id = data.get("course_id")
    if course_id is None:
        return error(400, "course_id is required")

    try:
        response = requests.get(f"{COURSE_SERVICE_URL}/api/courses/{course_id}/", timeout=3)
    except requests.exceptions.ConnectionError:
        # Course Service is down/unreachable - tell the caller this is a
        # dependency outage, not a bad request or a missing course.
        return error(503, "Course Service is unavailable - could not verify the course")
    except requests.exceptions.Timeout:
        return error(503, "Course Service timed out - could not verify the course")

    if response.status_code == 404:
        return error(400, f"course_id {course_id} does not exist in Course Service")
    if response.status_code != 200:
        return error(503, "Course Service returned an unexpected response")

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return error(400, "Student is already enrolled in this course")

    return jsonify(enrollment.to_dict()), 201


@app.get("/api/students/<int:student_id>/enrollments/")
def list_enrollments_for_student(student_id):
    if not Student.query.get(student_id):
        return error(404, f"Student with id {student_id} does not exist")
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    return jsonify([e.to_dict() for e in enrollments])


if __name__ == "__main__":
    app.run(port=5002, debug=True)
