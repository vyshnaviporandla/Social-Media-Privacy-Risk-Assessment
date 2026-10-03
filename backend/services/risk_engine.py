from .questions import QUESTIONS, CATEGORIES, WEIGHTS

def risk_level(score):
    score = float(score)
    if score <= 20: return "LOW"
    if score <= 40: return "MODERATE"
    if score <= 70: return "HIGH"
    return "CRITICAL"

def category_scores(answers):
    result = {}
    for category in CATEGORIES:
        qs = [q for q in QUESTIONS if q["category"] == category]
        total = 0
        maximum = 0
        for q in qs:
            maximum += max(q["weights"].values())
            value = answers.get(q["id"])
            if value in q["weights"]:
                total += q["weights"][value]
        result[category] = round((total / maximum) * 100, 2) if maximum else 0
    return result

def overall_score(categories):
    return round(sum(categories[c] * WEIGHTS[c] for c in CATEGORIES), 2)

def findings(categories):
    rules = {
        "Profile Visibility":"Your profile visibility exposes more information to a broader audience.",
        "Personal Information":"Visible personal details can support profiling and social-engineering attempts.",
        "Location Privacy":"Location and travel information can reveal routines or places you visit.",
        "Posts & Content":"Older or detailed posts can increase your long-term digital exposure.",
        "Connections":"Unknown or unmanaged connections can expand who can interact with you.",
        "Tagging & Mentions":"Uncontrolled tags and mentions can expose information you did not choose to publish.",
        "Account Security":"Account-security gaps can increase the impact of credential or takeover attempts.",
        "Third-Party Apps":"Unused or over-permissioned apps increase unnecessary access to account data.",
        "Social Engineering":"Public information can make deceptive messages appear more convincing.",
        "Digital Footprint":"Old and repeated public information can accumulate into a detailed profile."
    }
    return [{"category":c,"severity":risk_level(categories[c]),"finding":rules[c]} for c in CATEGORIES if categories[c] >= 35]

def recommendations(categories):
    recs = {
        "Profile Visibility":"Use the most restrictive audience that still fits your needs; review profile discovery settings.",
        "Personal Information":"Hide contact details, birthday, family details, and other information that does not need public visibility.",
        "Location Privacy":"Avoid real-time location sharing and review geotags, check-ins, travel posts, and routine patterns.",
        "Posts & Content":"Review older posts, remove unnecessary sensitive context, and avoid screenshots containing account details.",
        "Connections":"Review followers regularly and avoid accepting requests from people you cannot verify.",
        "Tagging & Mentions":"Enable tag/mention review where available and restrict who can tag or mention you.",
        "Account Security":"Enable MFA, use a unique password, turn on security alerts, and review active sessions.",
        "Third-Party Apps":"Remove unused integrations and grant only permissions that are necessary.",
        "Social Engineering":"Pause before responding to unexpected requests and independently verify links, identities, and urgent claims.",
        "Digital Footprint":"Search your own public profile periodically, remove outdated information, and revisit privacy settings after platform changes."
    }
    return [{"category":c,"priority":risk_level(categories[c]),"recommendation":recommendations if False else recs[c]} for c in CATEGORIES if categories[c] >= 25]

def assess(answers):
    cats = category_scores(answers)
    score = overall_score(cats)
    return {"category_scores":cats,"overall_score":score,"risk_level":risk_level(score),
            "findings":findings(cats),"recommendations":recommendations(cats)}

def simulate_improvement(answers):
    current = assess(answers)
    improved = dict(answers)
    for q in QUESTIONS:
        if q["id"] not in improved: continue
        # Safely simulate choosing the lowest-risk available option.
        lowest = min(q["weights"], key=q["weights"].get)
        improved[q["id"]] = lowest
    simulated = assess(improved)
    return {"current_score":current["overall_score"],"simulated_score":simulated["overall_score"],
            "current_level":current["risk_level"],"simulated_level":simulated["risk_level"],
            "improvement":round(current["overall_score"]-simulated["overall_score"],2),
            "note":"Simulation only; results are not a guarantee of future risk."}
