import re

SORE = [
    r"\bsore\b", r"\btight\b", r"\bstiff\b", r"\bache\b", r"\bpain\b",
    r"\bcalf\b", r"\bhamstring\b", r"\bquad\b", r"\bshin\b",
    r"\bhip\b", r"\bfoot\b", r"\bankle\b", r"\bknee\b"
]
FATIGUE = [
    r"\bheavy legs\b", r"\bfatigued\b", r"\bwiped\b", r"\bexhausted\b",
    r"\bflat\b", r"\bdrained\b", r"\bno pop\b"
]
ILL = [
    r"\bsick\b", r"\bfever\b", r"\bcough\b", r"\bstuffy\b",
    r"\bflu\b", r"\bcold\b", r"\bsore throat\b"
]

def analyze_notes(text: str) -> dict:
    t = (text or "").lower()

    soreness_flag = any(re.search(p, t) for p in SORE)
    fatigue_flag = any(re.search(p, t) for p in FATIGUE)
    illness_flag = any(re.search(p, t) for p in ILL)

    readiness = 0.0
    if illness_flag:
        readiness -= 0.02
    elif soreness_flag:
        readiness -= 0.01
    elif fatigue_flag:
        readiness -= 0.008

    guidance = []
    if illness_flag:
        guidance += [
            "Today: rest or very easy only. Skip intensity.",
            "Resume harder work only after symptoms improve."
        ]
    if soreness_flag and not illness_flag:
        guidance += [
            "Reduce intensity for 24–72 hours; keep easy runs EASY.",
            "Avoid adding new speed/VO2 sessions while sore.",
            "If pain is sharp/localized or worsening, stop hard running and consider medical evaluation."
        ]
    if fatigue_flag and not illness_flag:
        guidance += [
            "Prioritize sleep and fueling; keep the next easy run truly easy.",
            "If fatigue persists 3+ days, reduce hard volume (not just pace)."
        ]

    return {
        "soreness_flag": soreness_flag,
        "fatigue_flag": fatigue_flag,
        "illness_flag": illness_flag,
        "readiness_modifier": float(max(-0.03, min(0.01, readiness))),
        "guidance": guidance
    }
