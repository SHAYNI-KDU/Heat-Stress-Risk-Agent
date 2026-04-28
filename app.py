import os
import base64
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

# Internal module imports (Ensure these files are in your project folder)
from agent import build_agent
from tools.weather import get_weather, SRI_LANKA_LOCATIONS
from tools.heat_index import calculate_heat_index
from tools.risk_classifier import classify_risk

# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Heat Stress Risk Agent",
    page_icon="🌡️",
    layout="wide",
)

# --- Helper Functions ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        return ""
    except Exception:
        return ""

# --- Modern Interactive Styling (Glassmorphism) ---
bg_image = get_base64_image("background.png")
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* The "Glass" Overlay */
    .stApp > div:first-child {{
        background-color: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
    }}
    
    /* Typography & Glow */
    h1, h2, h3, p, label, .stCaption {{
        color: white !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }}

    /* Centered Modern Metric Cards */
    [data-testid="stMetric"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center !important; /* Forces alignment */
    }}

    /* Centers the label and value specifically */
   [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }}

    /* Safe Hour Time Styling */
    .safe-label {{ color: #bdc3c7 !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 1px; }}
    .safe-time {{ color: #ffffff !important; font-size: 2.2rem !important; font-weight: bold !important; }}
    
    /* Custom Scrollbar for Chat */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 10px; }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: rgba(20, 20, 20, 0.8) !important;
        backdrop-filter: blur(10px);
    }}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center; font-size: 3rem; font-weight: 800; margin-bottom: 0;'>HeatGuard <span style='color: #ff4b4b;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8; margin-top: 0;'>Protecting Sri Lanka from dangerous heat conditions </p>", unsafe_allow_html=True)
st.write("---")

# --- Sidebar: User Profile (Preserved Features) ---
with st.sidebar:
    st.header("Your Profile")
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

    # Metrics Row (Using modern metric cards)
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Temperature", f"{current['temperature_c']}°C")
    m_col2.metric("Humidity", f"{current['humidity']}%")
    m_col3.metric("Heat Index", f"{hi_data['heat_index_c']}°C")
    m_col4.metric("Feels Like", f"{current['apparent_temp_c']}°C")

    # Risk Alert Badge with Gradient
    # Risk Alert Badge (Centered)
    st.markdown(f"""
        <div style='padding:20px; background: linear-gradient(90deg, {risk['color']}aa, #2c3e50); 
        color:white; border-radius:15px; border-left: 8px solid {risk['color']}; 
        text-align:center; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
        display: flex; flex-direction: column; align-items: center; justify-content: center;'>
            <span style='font-size: 2.5rem;'>{risk['emoji']}</span> 
            <strong style='font-size: 1.5rem;'>{risk['risk_level']} Risk</strong> 
            <p style='margin: 5px 0 0 0; opacity: 0.9; max-width: 600px;'>{risk['description']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Actionable Advice Cards
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
    fig.add_trace(go.Scatter(x=times, y=hi_values, mode="lines+markers", 
                            line=dict(color="#ff4b4b", width=3), 
                            fill="tozeroy", fillcolor="rgba(255,75,75,0.1)"))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, color="white"), yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", color="white"),
        height=300, margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Safe Hours Section
    st.subheader("Best Hours Outdoors")
    threshold = 28 if activity in ["elderly", "construction"] else 30 if activity in ["farming", "sports"] else 33
    safe_hours = [t for t, val in zip(times, hi_values) if val < threshold]

    if safe_hours:
        st.success(f"✅ **Safest hours today:** {safe_hours[0]} – {safe_hours[-1]}")
        
        # Create 3 columns for the cards
        h_cols = st.columns(3)
        
        # Select the start, middle, and end of the safe window
        picks = [safe_hours[0], safe_hours[len(safe_hours)//2], safe_hours[-1]]
        labels = ["EARLY MORNING", "MID WINDOW", "EVENING"]
        
        for col, hour, lbl in zip(h_cols, picks, labels):
            col.markdown(f"""
                <div class="safe-hour-card" style="
                    background: rgba(0, 0, 0, 0.4); 
                    backdrop-filter: blur(10px); 
                    border: 1px solid rgba(255, 255, 255, 0.1); 
                    padding: 25px; 
                    border-radius: 15px; 
                    text-align: center;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
                ">
                    <div style="color: #bdc3c7; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 15px;">
                        {lbl}
                    </div>
                    <div style="color: white; font-size: 2.8rem; font-weight: 800; line-height: 1;">
                        {hour}
                    </div>
                    <div style="
                        height: 4px; 
                        width: 40px; 
                        background-color: #27ae60; 
                        margin: 20px auto 0 auto; 
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(39, 174, 96, 0.5);
                    "></div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("⚠️ No safe hours found today. Avoid outdoor activity.")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")

# --- First Aid Guide (Preserved exactly as requested) ---
st.divider()
with st.expander("Heat Stroke First Aid Guide"):
    st.markdown("""
    **Heat Stroke (Emergency — Call 1990)**: Hot/Red/Dry skin, no sweating, high temp (39°C+), confusion.
    1. **Call 1990** immediately.
    2. Move to shade and cool rapidly with wet cloths/ice on neck & armpits.
    3. Do **NOT** give water if unconscious.
    """)

# --- Chat Interface (Fixed height for attractiveness) ---
st.subheader("🤖 Ask the Agent")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Container with height prevents the page from growing infinitely
chat_container = st.container(height=400)

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("Ask about safety plans or symptoms..."):
    if not api_key:
        st.error("Please provide an API key.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing context..."):
                    try:
                        agent = build_agent(api_key)
                        full_context = f"User: {name}, Loc: {location}, Act: {activity}, Age: {age}. Q: {prompt}"
                        result = agent.invoke({"messages": st.session_state.chat_history + [{"role": "user", "content": full_context}]})
                        response = result["messages"][-1].content
                        st.write(response)
                        
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.session_state.chat_history.extend([{"role": "user", "content": prompt}, {"role": "assistant", "content": response}])
                    except Exception as e:
                        st.error(f"Agent error: {e}")