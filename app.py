import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
from tools.weather import get_weather, SRI_LANKA_LOCATIONS
from tools.heat_index import calculate_heat_index
from tools.risk_classifier import classify_risk
import base64
from agent import build_agent

load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="Heat Stress", layout="centered")

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

bg_image = get_base64_image("background.png")

# --- MOBILE WRAPPER CSS ---
st.markdown(f"""
    <style>
    .block-container {{
        max-width: 450px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    
    }}
    [data-testid="stMetric"] {{
    background-color: rgba(255, 255, 255, 0.2); /* 20% transparent white */
    backdrop-filter: blur(10px); /* Adds a modern blur effect */
    padding: 15px !important;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
}}
    [data-testid="stChatMessage"] {{
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    [data-testid="stSidebar"] {{ display: none; }}

    [data-testid="stChatInput"] {{
        max-width: 450px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        left: 0 !important;
        right: 0 !important;
    }}
    .safe-hour-card {{
        background: rgba(46, 204, 113, 0.2);
        border: 1px solid #2ecc71;
        border-radius: 10px;
        padding: 8px;
        text-align: center;
        margin-bottom: 5px;
    }}
    .safe-label {{
        font-size: 0.7rem;
        color: #dfdfdf;
        text-transform: uppercase;
    }}
    .safe-time {{
        font-size: 1.1rem;
        font-weight: bold;
        color: #2ecc71;
    }}
    .custom-tip {{
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #f1c40f;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-size: 0.9rem;
    }}
            .stApp h1 {{
        background: linear-gradient(90deg, #FF4B2B 0%, #FF8008 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(255, 75, 43, 0.3);
    }}

    .stApp h2 {{
        color: #E0E0E0;
    }}
    </style>

""", unsafe_allow_html=True)

# ── Title Area ──
st.markdown("<h1 style='text-align: center;'>Heat Stress Risk Agent</h1>", unsafe_allow_html=True)
st.caption("Protecting Sri Lanka from dangerous heat conditions — powered by AI")

# ── 1. Profile Expander ──
with st.expander("Open Your Profile ", expanded=False):
    st.markdown("### User Settings")
    api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
    name = st.text_input("Your name", value="shanu")
    
    col_a, col_b = st.columns(2)
    with col_a:
        location = st.selectbox("District", sorted(SRI_LANKA_LOCATIONS.keys()), index=0)
    with col_b:
        activity_options = ["farming", "construction", "sports", "elderly", "general", "Other"]
        activity_select = st.selectbox("Activity", activity_options)
        if activity_select == "Other":
            activity = st.text_input("Describe activity", placeholder="e.g. cycling, fishing...")
            if not activity:
                activity = "general"
        else:
            activity = activity_select
    
    age = st.slider("Age", 10, 90, 24)
    
    if st.button("Save & Update Conditions", use_container_width=True):
        st.success("Profile Updated!")

st.divider()


# ── 2. Live Dashboard ──
try:
    coords = SRI_LANKA_LOCATIONS[location]
    weather = get_weather(*coords)
    current = weather["current"]
    hi = calculate_heat_index(current["temperature_c"], current["humidity"])
    risk = classify_risk(hi["heat_index_c"], activity=activity, age=age)

    if weather.get("is_mock"): 
        st.info("📡 Live weather unavailable — showing realistic Sri Lanka sample data.")

    st.subheader("Live Conditions")
    
    # 2x2 Grid for metrics
    col1, col2 = st.columns(2)
    col1.metric("🌡️ Temp", f"{current['temperature_c']}°C")
    col2.metric("💧 Hum", f"{current['humidity']}%")
    
    col3, col4 = st.columns(2)
    col3.metric("🔥 Heat Index", f"{hi['heat_index_c']}°C")
    col4.metric("🌡️ Feels Like", f"{current['apparent_temp_c']}°C")

    # Risk Warning Badge
    st.markdown(
        f"<div style='padding:15px; background:{risk['color']}; color:white; "
        f"border-radius:12px; text-align:center; font-weight:bold; margin-bottom:15px;'>"
        f"{risk['emoji']} {risk['risk_level']} Risk<br>"
        f"<small>{risk['description']}</small>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ── 3. Advice Cards ──
    st.info(f"💧 **Water intake**: {risk['water_per_hour_ml']} ml/hr")
    st.info(f"😴 **Rest schedule**: {risk['rest_schedule']}")
    st.info(f"📋 **Activity advice**: {risk['activity_advice']}")

    # ── 4. Forecast Chart ──
    st.subheader("Hourly Forecast")
    hourly = weather["hourly"]
    hi_values = [calculate_heat_index(t, h)["heat_index_c"] for t, h in zip(hourly["temperatures"], hourly["humidities"])]
    times = [t[11:16] for t in hourly["times"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times, y=hi_values, mode='lines+markers',
        line=dict(color='tomato', width=2),
        fill='tozeroy', fillcolor='rgba(255, 99, 71, 0.2)'
    ))
    fig.update_layout(
        height=280, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    
    # ── 5. Best Hours to Work Outdoors ──
    st.divider()
    st.subheader("Best Hours to Work Outdoors")

    if activity in ["elderly", "construction"]:
        threshold = 28
        threshold_label = "28°C (strict — high risk group)"
    elif activity in ["farming", "sports"]:
        threshold = 30
        threshold_label = "30°C (moderate activity)"
    else:
        threshold = 33
        threshold_label = "33°C (general public)"

    safe_hours = [t for t, hi_val in zip(times, hi_values) if hi_val < threshold]
    st.caption(f"Based on heat index threshold: {threshold_label}")

    if safe_hours:
        st.success(f"✅ **Safest hours today:** {safe_hours[0]} – {safe_hours[-1]}")
        col_h1, col_h2, col_h3 = st.columns(3)
        picks = [safe_hours[0], safe_hours[len(safe_hours)//2], safe_hours[-1]]
        labels = ["🌅 Morning", "☀️ Midday", "🌆 Evening"]
        for col, hour, label in zip([col_h1, col_h2, col_h3], picks, labels):
            with col:
                st.markdown(f"""
                    <div class="safe-hour-card">
                        <div class="safe-label">{label}</div>
                        <div class="safe-time">{hour}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="custom-tip">
                💡 <b>Expert Advice:</b> Avoid outdoor exposure between <b>{safe_hours[-1]}</b> and <b>{safe_hours[0]}</b> tomorrow morning.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ No safe hours found today. Avoid all outdoor activity.")

    # ── 6. Heat Stroke First Aid Guide ──
    st.divider()
    
    # Conditional Warning based on risk level
    risk_level_now = risk["risk_level"]
    if risk_level_now in ["High", "Very High", "Extreme Danger"]:
        st.warning("⚠️ Current conditions are dangerous. Read the first aid guide below.")

    with st.expander(" Heat Stroke First Aid Guide — Click to expand"):
        st.markdown("""
    ### Know the Signs

    **Heat Exhaustion** (Warning stage):
    - Heavy sweating, cool/pale/clammy skin
    - Fast/weak pulse, nausea or vomiting
    - Muscle cramps, tiredness, weakness
    - Dizziness, headache, fainting

    **Heat Stroke** (Emergency — call 1990 immediately):
    - High body temperature (103°F / 39.4°C+)
    - Hot, red, dry skin — **no sweating**
    - Rapid/strong pulse
    - Confusion, slurred speech, unconsciousness

    ---

    ### What To Do — Heat Exhaustion
    1. **Move** to a cool shaded area immediately
    2. **Loosen** tight clothing
    3. **Cool them down** — wet cloths on neck, armpits, groin
    4. **Give water** — small sips if conscious (not cold water)
    5. **Fan** the person
    6. If no improvement in 15 minutes → **call 1990**

    ---

    ### What To Do — Heat Stroke
    1. **Call 1990 (Suwa Seriya)** immediately
    2. **Move** to coolest area available
    3. **Cool rapidly** — wet cloths, ice packs on neck/armpits/groin
    4. **Do NOT** give water if unconscious
    5. Stay until ambulance arrives

    ---

    ### Emergency Numbers
    | Service | Number |
    |---|---|
    | Suwa Seriya Ambulance | **1990** |
    | Fire & Rescue | **110** |
    | Police | **119** |
    | Disaster Hotline | **117** |
        """)

    # ── 7. The AI Agent Interface ──
    st.divider()
    st.subheader("🤖 Ask the Agent")
    
    if "messages" not in st.session_state:
       st.session_state.messages = []
    if "chat_history" not in st.session_state:
       st.session_state.chat_history = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about safety..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    agent = build_agent(api_key)
                    full_context = f"User: {name}, Age: {age}, Activity: {activity}, Location: {location}. Heat Index: {hi['heat_index_c']}°C. Question: {prompt}"
                    messages = st.session_state.chat_history + [{"role": "user", "content": full_context}]
                    result = agent.invoke({"messages": messages})
                    response = result["messages"][-1].content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.chat_history.extend([
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": response},
                    ])
                except Exception as e:
                    st.error(f"Error: {e}")

except Exception as e:
    st.info("👋 Welcome! Please open the profile above and click 'Save' to start.")
