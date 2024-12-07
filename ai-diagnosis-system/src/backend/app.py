from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from main import get_openai_response

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

# Mock diagnosis function

def format_payload(payload):
    """Formats the payload into a query string for AI function"""
    symptoms = payload.get("symptoms", "No symptoms provided")
    lab = payload.get("lab", "No lab results provided")
    physical = payload.get("physical", "No physical exam findings provided")
    age = payload.get("age", "Unknown age")
    sex = payload.get("sex", "Unknown sex")
    
    # Create a doctor's note style string for query
    doctor_note = f"Symptoms: {symptoms}\nLab Findings: {lab}\nPhysical Exam: {physical}\nAge: {age}\nSex: {sex}"
    return doctor_note

# API route to handle the diagnosis request
@app.route("/submission", methods=["POST"])
def diagnose():
    payload = request.json

    if not payload:
        return jsonify({"error": "Invalid input"}), 400

    # Format the payload as a doctor note for the query
    query = format_payload(payload)

    # Call the AI function
    ai_response = get_openai_response(query, num_articles=3)  # Fetch 3 articles

    # Ensure the response is a JSON array of dictionaries
    relevant_cases = json.loads(ai_response)

    # Return the response as JSON
    return jsonify(relevant_cases)

@app.route("/")
def home():
    return "Welcome to the AI Diagnosis System Backend", 200

if __name__ == "__main__":
    app.run(port=8000, debug=True)