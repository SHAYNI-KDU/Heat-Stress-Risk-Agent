def classify_risk(heat_index_c: float, activity: str = "general", age: int = 30) -> dict:
    """
    Classify heat stress risk level and generate personalised recommendations.
    Based on WHO / OSHA heat stress thresholds.
    """

    # Risk level thresholds (Celsius heat index)
    if heat_index_c < 27:
        level = "Low"
        color = "#2d9e4f"
        emoji = "✅"
        description = "Conditions are safe for most people and activities."
    elif heat_index_c < 33:
        level = "Moderate"
        color = "#e8a020"
        emoji = "⚠️"
        description = "Caution advised. Fatigue possible with prolonged exposure."
    elif heat_index_c < 40:
        level = "High"
        color = "#e06020"
        emoji = "🔶"
        description = "Heat cramps and heat exhaustion possible. Limit outdoor activity."
    elif heat_index_c < 51:
        level = "Very High"
        color = "#cc2020"
        emoji = "🔴"
        description = "Heat stroke possible. Avoid outdoor exertion."
    else:
        level = "Extreme Danger"
        color = "#7b0080"
        emoji = "🚨"
        description = "Life-threatening heat conditions. Stay indoors immediately."

    # Hydration schedule
    if level == "Low":
        water_ml_per_hour = 250
    elif level == "Moderate":
        water_ml_per_hour = 500
    elif level == "High":
        water_ml_per_hour = 750
    else:
        water_ml_per_hour = 1000

    # Rest schedule
    if level in ["Low", "Moderate"]:
        rest_ratio = "5 min rest per 30 min activity"
    elif level == "High":
        rest_ratio = "10 min rest per 20 min activity"
    else:
        rest_ratio = "Avoid outdoor activity entirely"

    # Age adjustment note
    age_note = ""
    if age > 60:
        age_note = " Note: Older adults are at significantly higher risk — add extra caution."
    elif age < 18:
        age_note = " Note: Children are more vulnerable — reduce activity further."

    # Activity-specific advice
    activity_advice = {
        "farming": "Wear a wide-brimmed hat and light clothing. Work during early morning (before 9am) and evening (after 5pm).",
        "construction": "Use shaded rest areas. Rotate workers frequently. Never skip water breaks.",
        "sports": "Reduce training intensity by 30–50%. Move sessions to dawn or dusk.",
        "general": "Seek shade or air-conditioned spaces. Avoid peak sun hours (11am–3pm).",
        "elderly": "Stay indoors. Use fans or air conditioning. Check on neighbours regularly.",
    }

    advice = activity_advice.get(activity, activity_advice["general"])

    return {
        "risk_level": level,
        "color": color,
        "emoji": emoji,
        "description": description,
        "water_per_hour_ml": water_ml_per_hour,
        "rest_schedule": rest_ratio,
        "activity_advice": advice + age_note,
    }
