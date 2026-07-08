"""
Course Service - owns Department + Course data exclusively.
No other service is allowed to touch courses.db directly - if another
service needs course data it must call this service's HTTP API (see
Hands-On 10 / Task 2 for that inter-service call).
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------------------------------------------------------- Models

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    head_of_dept = db.Column(db.String(120))
    budget = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "head_of_dept": self.head_of_dept, "budget": self.budget}


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits,
            "department_id": self.department_id,
        }


with app.app_context():
    db.create_all()


def error(status_code, message):
    return jsonify({"error": {"code": status_code, "message": message}}), status_code


# ---------------------------------------------------------------- Health

@app.get("/health")
def health():
    return jsonify({"service": "course-service", "status": "ok"})


# ---------------------------------------------------------------- Departments

@app.post("/api/departments/")
def create_department():
    data = request.get_json(silent=True) or {}
    if "name" not in data:
        return error(400, "name is required")

    department = Department(name=data["name"], head_of_dept=data.get("head_of_dept"), budget=data.get("budget", 0.0))
    db.session.add(department)
    db.session.commit()
    return jsonify(department.to_dict()), 201


@app.get("/api/departments/")
def list_departments():
    return jsonify([d.to_dict() for d in Department.query.all()])


# ---------------------------------------------------------------- Courses

@app.get("/api/courses/")
def list_courses():
    return jsonify([c.to_dict() for c in Course.query.all()])


@app.post("/api/courses/")
def create_course():
    data = request.get_json(silent=True) or {}
    required = {"name", "code", "credits", "department_id"}
    if not required.issubset(data):
        return error(400, f"Missing required fields: {required - set(data)}")

    if not Department.query.get(data["department_id"]):
        return error(400, "department_id does not exist")

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data["department_id"],
    )
    db.session.add(course)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return error(400, "Course code must be unique")

    return jsonify(course.to_dict()), 201


@app.get("/api/courses/<int:course_id>/")
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return error(404, f"Course with id {course_id} does not exist")
    return jsonify(course.to_dict())


@app.delete("/api/courses/<int:course_id>/")
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return error(404, f"Course with id {course_id} does not exist")
    db.session.delete(course)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    # Runs on its own port, with its own database - independent of Student Service.
    app.run(port=5001, debug=True)
