import os
import base64
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

# Internal module imports
from agent import build_agent
from tools.weather import get_weather, SRI_LANKA_LOCATIONS
from tools.heat_index import calculate_heat_index
from tools.risk_classifier import classify_risk

# Load environment variables
load_dotenv()

# --- Helper Functions ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        return ""
    except Exception:
        return ""

# --- Page Configuration ---
st.set_page_config(
    page_title="Heat Stress Risk Agent",
    page_icon="🌡️",
    layout="wide",
)

# --- Custom Styling ---
bg_image = get_base64_image("background.png")
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp > div {{ background-color: rgba(0, 0, 0, 0.45); }}
    
    h1, h2, h3, p, label, .stCaption {{
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }}

    [data-testid="stChatMessage"] {{
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .safe-hour-card {{
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-top: 10px;
    }}
    .safe-label {{ color: #bdc3c7 !important; font-size: 0.85rem !important; text-transform: uppercase; }}
    .safe-time {{ color: #ffffff !important; font-size: 2.2rem !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>Heat Stress Risk Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>Protecting Sri Lanka from dangerous heat conditions — powered by AI</p>", unsafe_allow_html=True)

# --- Sidebar: User Profile ---
with st.sidebar:
    st.header("⚙️ Your Profile")
    api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
    st.divider()
    
    name = st.text_input("Your name", value="User")
    location_list = sorted(SRI_LANKA_LOCATIONS.keys())
    location = st.selectbox("Location (District)", location_list, index=location_list.index("Kandy") if "Kandy" in location_list else 0)
    
    activity_options = ["farming", "construction", "sports", "elderly", "general", "Other (type below)"]
    activity_select = st.selectbox("Activity type", activity_options)
    
    if activity_select == "Other (type below)":
        activity = st.text_input("Describe your activity", placeholder="e.g. cycling...") or "general"
    else:
        activity = activity_select
    
    age = st.slider("Age", 10, 90, 30)
    st.divider()
    st.markdown("**Data Sources:** [Open-Meteo](https://open-meteo.com/) & [Groq Llama3](https://console.groq.com)")

# --- Live Dashboard Logic ---
try:
    coords = SRI_LANKA_LOCATIONS[location]
    weather = get_weather(*coords)
    current = weather["current"]
    hi_data = calculate_heat_index(current["temperature_c"], current["humidity"])
    risk = classify_risk(hi_data["heat_index_c"], activity=activity, age=age)

    if weather.get("is_mock"):
        st.info("Live weather unavailable — showing sample data.")

    # Metrics Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    label_style = "margin-bottom: 0; font-size: 1.1rem; font-weight: 400; color: white;"
    value_style = "margin-top: -10px; font-size: 2.8rem; font-weight: 500; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);"

    with m_col1:
        st.markdown(f'<div style="text-align: center;"><p style="{label_style}"> Temperature</p><h1 style="{value_style}">{current["temperature_c"]}°C</h1></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div style="text-align: center;"><p style="{label_style}"> Humidity</p><h1 style="{value_style}">{current["humidity"]}%</h1></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div style="text-align: center;"><p style="{label_style}"> Heat Index</p><h1 style="{value_style}">{hi_data["heat_index_c"]}°C</h1></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown(f'<div style="text-align: center;"><p style="{label_style}"> Feels Like</p><h1 style="{value_style}">{current["apparent_temp_c"]}°C</h1></div>', unsafe_allow_html=True)

    # Risk Badge
    st.markdown(f"""
        <div style='padding:14px; background:{risk['color']}; color:white; border-radius:10px; 
        font-size:17px; text-align:center; margin: 15px 0;'>
            {risk['emoji']} <strong>{risk['risk_level']} Risk</strong> — {risk['description']}
        </div>
    """, unsafe_allow_html=True)

    # Advice Cards
    c_a, c_b, c_c = st.columns(3)
    c_a.info(f"**Water Intake**\n\n{risk['water_per_hour_ml']} ml/hr")
    c_b.info(f"**Rest Schedule**\n\n{risk['rest_schedule']}")
    c_c.info(f"**Advice**\n\n{risk['activity_advice']}")

    # Hourly Forecast Chart
    st.subheader("Hourly Heat Index Forecast")
    hourly = weather["hourly"]
    hi_values = [calculate_heat_index(t, h)["heat_index_c"] for t, h in zip(hourly["temperatures"], hourly["humidities"])]
    times = [t[11:16] for t in hourly["times"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=hi_values, mode="lines+markers", line=dict(color="tomato", width=2.5), fill="tozeroy", fillcolor="rgba(255,99,71,0.1)"))
    fig.add_hline(y=33, line_dash="dash", line_color="#e8a020", annotation_text="Moderate")
    fig.add_hline(y=40, line_dash="dash", line_color="#cc2020", annotation_text="High Risk")
    fig.update_layout(xaxis_title="Time", yaxis_title="Heat Index (°C)", height=300, margin=dict(l=0, r=0, t=20, b=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Safe Hours Section
    st.subheader("Best Hours Outdoors")
    threshold = 28 if activity in ["elderly", "construction"] else 30 if activity in ["farming", "sports"] else 33
    safe_hours = [t for t, val in zip(times, hi_values) if val < threshold]

    if safe_hours:
        st.success(f"✅ **Safest hours today:** {safe_hours[0]} – {safe_hours[-1]}")
        h_cols = st.columns(3)
        picks = [safe_hours[0], safe_hours[len(safe_hours)//2], safe_hours[-1]]
        labels = ["Early Morning", "Mid Window", "Evening"]
        for col, hour, lbl in zip(h_cols, picks, labels):
            col.markdown(f'<div class="safe-hour-card"><div class="safe-label">{lbl}</div><div class="safe-time">{hour}</div></div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ No safe hours found today. Avoid outdoor activity.")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")

# --- First Aid Guide ---
st.divider()
with st.expander("Heat Stroke First Aid Guide"):
    st.markdown("""
    **Heat Stroke (Emergency — Call 1990)**: Hot/Red/Dry skin, no sweating, high temp (39°C+), confusion.
    1. **Call 1990** immediately.
    2. Move to shade and cool rapidly with wet cloths/ice on neck & armpits.
    3. Do **NOT** give water if unconscious.
    """)

# --- Chat Interface ---
st.subheader("🤖 Ask the Agent")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about safety plans or symptoms..."):
    if not api_key:
        st.error("Please provide an API key.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    agent = build_agent(api_key)
                    full_context = f"User: {name}, Loc: {location}, Act: {activity}, Age: {age}. Q: {prompt}"
                    # Use a clean version of messages for the agent logic
                    result = agent.invoke({"messages": st.session_state.chat_history + [{"role": "user", "content": full_context}]})
                    response = result["messages"][-1].content
                    st.write(response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.chat_history.extend([{"role": "user", "content": prompt}, {"role": "assistant", "content": response}])
                except Exception as e:
                    st.error(f"Agent error: {e}")