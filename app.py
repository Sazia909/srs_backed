from flask import render_template
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(50))
    marks = db.Column(db.Integer)

# Create database
with app.app_context():
    db.create_all()

@app.route("/add_student", methods=["POST", "GET"])
def add_student():
    roll = request.args.get("roll")
    name = request.args.get("name")
    marks = request.args.get("marks")

    student = Student(roll=roll, name=name, marks=marks)
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student added successfully"})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_result")
def get_result():
    roll = request.args.get("roll")
    student = Student.query.filter_by(roll=roll).first()

    if student:
        return jsonify({"name": student.name, "marks": student.marks})
    else:
        return jsonify({"error": "Student not found"})