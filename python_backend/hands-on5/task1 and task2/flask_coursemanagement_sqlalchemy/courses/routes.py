from flask import Blueprint, request, jsonify
from app import db
from courses.models import Course, Student, Enrollment

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)


# GET ALL COURSES
@courses_bp.route("/", methods=["GET"])
def get_courses():

    courses = Course.query.all()

    return jsonify([course.to_dict() for course in courses])


# CREATE COURSE
@courses_bp.route("/", methods=["POST"])
def add_course():

    data = request.get_json()

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data["department_id"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_dict()), 201


# GET COURSE BY ID
@courses_bp.route("/<int:id>", methods=["GET"])
def get_course(id):

    course = Course.query.get_or_404(id)

    return jsonify(course.to_dict())


# UPDATE COURSE
@courses_bp.route("/<int:id>", methods=["PUT"])
def update_course(id):

    course = Course.query.get_or_404(id)

    data = request.get_json()

    course.name = data.get("name", course.name)
    course.code = data.get("code", course.code)
    course.credits = data.get("credits", course.credits)
    course.department_id = data.get(
        "department_id",
        course.department_id
    )

    db.session.commit()

    return jsonify(course.to_dict())


# DELETE COURSE
@courses_bp.route("/<int:id>", methods=["DELETE"])
def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)

    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    })


# STUDENTS ENROLLED IN A COURSE
@courses_bp.route("/<int:id>/students/", methods=["GET"])
def course_students(id):

    course = Course.query.get_or_404(id)

    students = (
        db.session.query(Student)
        .join(Enrollment)
        .filter(Enrollment.course_id == course.id)
        .all()
    )

    return jsonify(
        [student.to_dict() for student in students]
    )