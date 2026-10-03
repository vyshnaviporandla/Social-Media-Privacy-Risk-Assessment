import csv, random
from pathlib import Path
from datetime import datetime, timedelta
random.seed(42)
categories=["Profile Visibility","Personal Information","Location Privacy","Posts & Content","Connections","Tagging & Mentions","Account Security","Third-Party Apps","Social Engineering","Digital Footprint"]
weights=[.10,.15,.15,.10,.10,.05,.15,.05,.10,.05]
levels=lambda s:"LOW" if s<=20 else "MODERATE" if s<=40 else "HIGH" if s<=70 else "CRITICAL"
out=Path(__file__).parent/"social_media_privacy_assessments.csv"
rows=[]
for i in range(1,1001):
    scores=[random.randint(0,100) for _ in categories]
    overall=round(sum(a*b for a,b in zip(scores,weights)),2)
    rows.append([f"ASM-{i:04d}",*scores,overall,levels(overall),(datetime(2026,1,1)+timedelta(days=random.randint(0,270))).date().isoformat()])
with out.open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["assessment_id",*categories,"overall_score","risk_level","created_at"]);w.writerows(rows)
print(f"Generated {len(rows)} synthetic records: {out}")
