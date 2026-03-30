from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(100))
    date = db.Column(db.String(100))

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"name": u.name, "email": u.email} for u in users])

@app.route("/symptom-check", methods=["POST"])
def symptom_check():
    data = request.json
    symptom = data["symptom"]

    if "fever" in symptom.lower():
        advice = "You may have an infection. Visit nearest clinic."
    elif "headache" in symptom.lower():
        advice = "Drink water and rest. If persistent, see doctor."
    else:
        advice = "Consult a health professional."

    return jsonify({"advice": advice})

@app.route("/appointment", methods=["POST"])
def appointment():
    data = request.json
    new_app = Appointment(patient=data["patient"], date=data["date"])
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"message": "Appointment booked!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)