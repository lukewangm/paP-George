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

# Mock diagnosis function

# Mock AI Diagnosis Function
def mock_ai_diagnosis(payload):
    # Extract the relevant fields from the payload
    symptoms = payload.get("symptoms")
    lab = payload.get("lab")
    physical = payload.get("physical")
    age = payload.get("age")
    sex = payload.get("sex")
    
    # Generate mock response based on the input
    response_urls = [
        "https://medical-report.example.com/report1",
        "https://medical-report.example.com/report2",
        "https://medical-report.example.com/report3"
    ]
    
    return response_urls

# API route to handle the diagnosis request
@app.route("/submission", methods=["POST"])
def diagnose():
    payload = request.json  # Get the JSON payload from the request

    if not payload:
        return jsonify({"error": "Invalid input"}), 400

    # Generate the mock URLs response
    response_data = mock_ai_diagnosis(payload)

    # Return the response as a JSON array (matching [string, string, string] structure)
    return jsonify(response_data)

@app.route("/")
def home():
    return "Welcome to the AI Diagnosis System Backend", 200

if __name__ == "__main__":
    app.run(port=8000, debug=True)