import math
import pandas as pd

def compute_metrics(intervals: pd.DataFrame, effort: int, notes_analysis: dict) -> dict:
    if intervals is None or intervals.empty:
        return {
            "duration_min": 0.0,
            "hard_meters": 0.0,
            "density_score": 0.0,
            "sRPE_load": 0.0,
            **{k: notes_analysis[k] for k in ["soreness_flag","fatigue_flag","illness_flag","readiness_modifier"]}
        }

    hard_m = 0.0
    work_sec = 0.0
    rest_sec = 0.0
    density_acc = 0.0

    for _, r in intervals.iterrows():
        sets = float(r["sets"])
        reps = float(r["reps_per_set"])
        d = float(r["rep_distance_m"])
        t = float(r["rep_time_sec"])
        rr = float(r["rest_rep_sec"])
        rs = float(r["rest_set_sec"])

        total_reps = sets * reps
        meters = d * total_reps
        hard_m += meters

        work = t * total_reps
        rest = rr * (total_reps - sets) + rs * max(sets - 1, 0)
        work_sec += work
        rest_sec += rest

        density = work / (rest + 1.0)
        density_acc += meters * math.tanh(density / 1.25)

    duration_min = (work_sec + rest_sec) / 60.0
    density_score = density_acc / max(hard_m, 1.0)
    sRPE_load = float(effort) * float(duration_min)

    return {
        "duration_min": float(duration_min),
        "hard_meters": float(hard_m),
        "density_score": float(density_score),
        "sRPE_load": float(sRPE_load),
        **{k: notes_analysis[k] for k in ["soreness_flag","fatigue_flag","illness_flag","readiness_modifier"]}
    }
