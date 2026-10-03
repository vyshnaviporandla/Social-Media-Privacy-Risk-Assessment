import sqlite3, json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "privacy_assessment.db"

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = connect()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS assessments(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      overall_score REAL NOT NULL,
      risk_level TEXT NOT NULL,
      created_at TEXT NOT NULL,
      answers_json TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS category_scores(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      assessment_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      score REAL NOT NULL
    );
    CREATE TABLE IF NOT EXISTS findings(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      assessment_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      severity TEXT NOT NULL,
      finding TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS recommendations(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      assessment_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      priority TEXT NOT NULL,
      recommendation TEXT NOT NULL
    );
    """)
    con.commit()
    con.close()

def save_assessment(result, answers, created_at):
    con = connect()
    cur = con.execute("INSERT INTO assessments(overall_score,risk_level,created_at,answers_json) VALUES(?,?,?,?)",
                      (result["overall_score"],result["risk_level"],created_at,json.dumps(answers)))
    aid = cur.lastrowid
    for c,s in result["category_scores"].items():
        con.execute("INSERT INTO category_scores(assessment_id,category,score) VALUES(?,?,?)",(aid,c,s))
    for f in result["findings"]:
        con.execute("INSERT INTO findings(assessment_id,category,severity,finding) VALUES(?,?,?,?)",
                    (aid,f["category"],f["severity"],f["finding"]))
    for r in result["recommendations"]:
        con.execute("INSERT INTO recommendations(assessment_id,category,priority,recommendation) VALUES(?,?,?,?)",
                    (aid,r["category"],r["priority"],r["recommendation"]))
    con.commit()
    con.close()
    return aid

def get_assessment(aid):
    con = connect()
    a = con.execute("SELECT id,overall_score,risk_level,created_at FROM assessments WHERE id=?",(aid,)).fetchone()
    if not a: return None
    cats = con.execute("SELECT category,score FROM category_scores WHERE assessment_id=?",(aid,)).fetchall()
    fs = con.execute("SELECT category,severity,finding FROM findings WHERE assessment_id=?",(aid,)).fetchall()
    rs = con.execute("SELECT category,priority,recommendation FROM recommendations WHERE assessment_id=?",(aid,)).fetchall()
    con.close()
    return {"id":a["id"],"overall_score":a["overall_score"],"risk_level":a["risk_level"],"created_at":a["created_at"],
            "category_scores":{x["category"]:x["score"] for x in cats},
            "findings":[dict(x) for x in fs],"recommendations":[dict(x) for x in rs]}

def stats():
    con = connect()
    total = con.execute("SELECT COUNT(*) n FROM assessments").fetchone()["n"]
    avg = con.execute("SELECT COALESCE(AVG(overall_score),0) n FROM assessments").fetchone()["n"]
    levels = con.execute("SELECT risk_level,COUNT(*) n FROM assessments GROUP BY risk_level").fetchall()
    con.close()
    return {"total_assessments":total,"average_score":round(avg,2),"risk_levels":{x["risk_level"]:x["n"] for x in levels}}
