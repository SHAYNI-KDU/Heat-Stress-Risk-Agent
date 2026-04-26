from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from tools.weather import get_weather, SRI_LANKA_LOCATIONS
from tools.heat_index import calculate_heat_index
from tools.risk_classifier import classify_risk
from memory.profile_store import save_profile, load_profile


@tool
def fetch_heat_risk(location: str, activity: str, age: int) -> str:
    """
    Fetch current weather for a Sri Lanka location, calculate the heat index,
    and return a full personalised risk assessment with safety advice.
    """
    coords = SRI_LANKA_LOCATIONS.get(location)
    if not coords:
        return (
            f"Location '{location}' not found. "
            f"Available locations: {list(SRI_LANKA_LOCATIONS.keys())}"
        )
    weather = get_weather(*coords)
    current = weather["current"]
    hi = calculate_heat_index(current["temperature_c"], current["humidity"])
    risk = classify_risk(hi["heat_index_c"], activity=activity, age=age)
    return (
        f"Location: {location}\n"
        f"Temperature: {current['temperature_c']}°C | Humidity: {current['humidity']}%\n"
        f"Heat Index: {hi['heat_index_c']}°C\n"
        f"Risk Level: {risk['emoji']} {risk['risk_level']}\n"
        f"Description: {risk['description']}\n"
        f"Water intake: {risk['water_per_hour_ml']} ml/hour\n"
        f"Rest schedule: {risk['rest_schedule']}\n"
        f"Advice: {risk['activity_advice']}"
    )


@tool
def save_user_profile(name: str, location: str, activity: str, age: int) -> str:
    """Save the user's profile (location, activity type, age) for future sessions."""
    profile = {"location": location, "activity": activity, "age": age}
    save_profile(name, profile)
    return f"Profile saved for {name}. I'll remember your details next time."


@tool
def load_user_profile(name: str) -> str:
    """Load a previously saved user profile by name."""
    profile = load_profile(name)
    if profile:
        return f"Welcome back, {name}! Your profile: {profile}"
    return f"No saved profile found for '{name}'. Let's set one up."


def build_agent(api_key: str):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0,
    )

    tools = [fetch_heat_risk, save_user_profile, load_user_profile]

    system_message = SystemMessage(content="""You are a Heat Stress Risk Agent designed to protect people in Sri Lanka 
from dangerous heat conditions. You assist farmers, construction workers, athletes, 
elderly people, and anyone exposed to outdoor heat.

When a user asks about heat risk:
1. Use the fetch_heat_risk tool to get real-time data.
2. Explain the risk level clearly and compassionately.
3. Give specific, actionable advice tailored to their activity and age.
4. Offer to save their profile so you remember them next time.

Always be clear, caring, and practical. Lives may depend on your advice.
Available Sri Lanka districts: Ampara, Anuradhapura, Badulla, Batticaloa, Colombo, Galle, Gampaha, Hambantota, Jaffna, Kalutara, Kandy, Kegalle, Kilinochchi, Kurunegala, Mannar, Matale, Matara, Monaragala, Mullaitivu, Nuwara Eliya, Polonnaruwa, Puttalam, Ratnapura, Trincomalee, Vavuniya.""")

    agent = create_react_agent(llm, tools, prompt=system_message)
    return agent
