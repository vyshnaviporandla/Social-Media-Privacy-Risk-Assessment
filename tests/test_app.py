import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.services.risk_engine import risk_level, assess
from backend.services.questions import QUESTIONS

def test_boundaries():
    assert risk_level(20)=="LOW"
    assert risk_level(21)=="MODERATE"
    assert risk_level(40)=="MODERATE"
    assert risk_level(41)=="HIGH"
    assert risk_level(70)=="HIGH"
    assert risk_level(71)=="CRITICAL"

def test_question_count():
    assert len(QUESTIONS) >= 40

def test_assessment_structure():
    answers={q["id"]:min(q["weights"],key=q["weights"].get) for q in QUESTIONS}
    result=assess(answers)
    assert 0 <= result["overall_score"] <= 100
    assert result["risk_level"]=="LOW"
    assert len(result["category_scores"])==10
