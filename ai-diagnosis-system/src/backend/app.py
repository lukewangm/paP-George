from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# """
#     Random simple way to configure DB, should be modifed later
# """
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return ""

# Mock AI Diagnosis Function
def mock_ai_diagnosis(data):
    symptoms = data.get("symptoms", "")
    diagnosis = {
        "symptoms": symptoms,
        "possible_conditions": [
            "Condition A",
            "Condition B",
            "Condition C"
        ],
        "recommendations": "Consult with a doctor for further diagnosis."
    }
    return diagnosis

# API endpoint to receive data and return diagnosis
@app.route("/api/diagnose", methods=["POST"])
def diagnose():
    try:
        data = request.json  # Receive JSON data from the frontend
        diagnosis = mock_ai_diagnosis(data)
        return jsonify({"message": "Diagnosis successful", "data": diagnosis}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route("/")
def home():
    return "Welcome to the AI Diagnosis System Backend", 200

if __name__ == "__main__":
    app.run(port=8000, debug=True)