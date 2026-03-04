def band(time_sec: float, weeks_of_data: int, load_volatility: float, readiness_modifier: float) -> tuple[float, float]:
    if time_sec <= 0:
        return (0.0, 0.0)

    width = 0.015
    if weeks_of_data < 2:
        width += 0.02
    elif weeks_of_data < 4:
        width += 0.01

    width += min(0.03, load_volatility * 0.01)
    if readiness_modifier < 0:
        width += min(0.02, abs(readiness_modifier) * 1.5)

    return (time_sec * (1 - width), time_sec * (1 + width))
