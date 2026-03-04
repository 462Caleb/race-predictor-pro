def compute_metrics(intervals, effort, notes_analysis):

    return {
        "duration_min":0,
        "hard_meters":0,
        "density_score":0,
        "sRPE_load":effort*10,
        "soreness_flag":notes_analysis["soreness_flag"],
        "fatigue_flag":notes_analysis["fatigue_flag"],
        "illness_flag":notes_analysis["illness_flag"],
        "readiness_modifier":notes_analysis["readiness_modifier"]
    }
