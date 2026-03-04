import re

def analyze_notes(text):

    t = text.lower()

    soreness = bool(re.search("sore|tight|ache|pain", t))
    fatigue = bool(re.search("fatigue|heavy legs|tired", t))
    illness = bool(re.search("sick|cold|flu", t))

    readiness = 0

    if illness:
        readiness -= 0.02
    elif soreness:
        readiness -= 0.01
    elif fatigue:
        readiness -= 0.008

    return {
        "soreness_flag": soreness,
        "fatigue_flag": fatigue,
        "illness_flag": illness,
        "readiness_modifier": readiness,
        "guidance": []
    }
