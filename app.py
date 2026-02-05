from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

# Add student
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json

    roll = data.get("roll")
    name = data.get("name")
    marks = data.get("marks")

    if not roll or not name or not marks:
        return jsonify({"error": "Missing data"}), 400

    student = Student(roll=roll, name=name, marks=int(marks))
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student added successfully"})

# Get result
@app.route("/get_result")
def get_result():
    roll = request.args.get("roll")
    student = Student.query.filter_by(roll=roll).first()

    if student:
        return jsonify({"name": student.name, "marks": student.marks})
    else:
        return jsonify({"error": "Student not found"}), 404

# Health check
@app.route("/")
def home():
    return "Student Result System API is running"
