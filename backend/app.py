from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime, timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backend.services.questions import QUESTIONS
from backend.services.risk_engine import assess, simulate_improvement
from backend.database import init_db, save_assessment, get_assessment, stats

BASE = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_folder=str(BASE/"frontend"), static_url_path="")
CORS(app)
init_db()

@app.get("/")
def home():
    return send_from_directory(BASE/"frontend","index.html")

@app.get("/api/questions")
def questions():
    safe = [{"id":q["id"],"category":q["category"],"text":q["text"],"options":list(q["weights"].keys())} for q in QUESTIONS]
    return jsonify(safe)

@app.post("/api/assessment")
def create_assessment():
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", {})
    missing = [q["id"] for q in QUESTIONS if answers.get(q["id"]) not in q["weights"]]
    if missing:
        return jsonify({"error":"Please answer every question.","missing":missing}),400
    result = assess(answers)
    aid = save_assessment(result, answers, datetime.now(timezone.utc).isoformat())
    return jsonify({"id":aid,**result})

@app.get("/api/assessment/<int:aid>")
def assessment(aid):
    item = get_assessment(aid)
    if not item: return jsonify({"error":"Assessment not found"}),404
    return jsonify(item)

@app.get("/api/assessment/<int:aid>/recommendations")
def assessment_recommendations(aid):
    item = get_assessment(aid)
    if not item: return jsonify({"error":"Assessment not found"}),404
    return jsonify(item["recommendations"])

@app.post("/api/assessment/simulate-improvement")
def simulate():
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", {})
    missing = [q["id"] for q in QUESTIONS if answers.get(q["id"]) not in q["weights"]]
    if missing: return jsonify({"error":"Complete the questionnaire first.","missing":missing}),400
    return jsonify(simulate_improvement(answers))

@app.get("/api/dashboard/stats")
def dashboard_stats():
    return jsonify(stats())

@app.get("/api/privacy-checklist")
def checklist():
    return jsonify([
      "Keep the smallest practical audience for personal posts.",
      "Do not publish phone numbers, email addresses, birth dates, or home-area details unnecessarily.",
      "Avoid real-time location, geotagging, check-ins, and predictable routine information.",
      "Review old posts, tags, mentions, followers, and connected apps.",
      "Enable MFA and login/security alerts.",
      "Use unique passwords and a password manager for important accounts.",
      "Verify unexpected requests and links independently.",
      "Review privacy settings after major platform changes."
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
