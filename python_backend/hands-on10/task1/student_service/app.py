"""
Student Service - owns Student data exclusively, in its own database
(students.db), completely separate from Course Service's courses.db.

Note: this service does NOT yet talk to Course Service - that inter-service
call (verifying a course exists before enrolling a student) is added in
Hands-On 10 / Task 2, along with the API Gateway that sits in front of both
services.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


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


if __name__ == "__main__":
    # Runs on its own port, with its own database - independent of Course Service.
    app.run(port=5002, debug=True)
