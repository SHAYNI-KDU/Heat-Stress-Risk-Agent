# Heat Stress Risk Agent

An autonomous AI agent that protects people in Sri Lanka from dangerous heat conditions.

Built for the KDU BSc Applied Data Science Communication assignment (LB3114, Intake 41).

---

## YT Link :
https://youtube.com/shorts/7qQ9nerpK_I?feature=share

##  Features:
- Real-time weather data for all 25 Sri Lanka districts
- Scientific heat index calculation (Steadman formula)
- Risk classification based on WHO thresholds
- Personalised advice by activity type and age
- Best safe working hours from hourly forecast
- AI-powered chat agent for heat safety questions
- Heat stroke first aid guide with emergency numbers
- Conversation memory across sessions

## Built With:
- Python & Streamlit
- LangChain + Groq Llama3 (AI agent)
- Open-Meteo API (free real-time weather)
- Plotly (interactive charts)
---

## Project Structure

```
heat-stress-agent/
│
├── app.py                    # Streamlit UI — main entry point
├── agent.py                  # LangChain agent with tools
├── tools/
│   ├── weather.py            # Open-Meteo API integration
│   ├── heat_index.py         # Steadman heat index formula
│   └── risk_classifier.py    # WHO risk classification
├── memory/
│   └── profile_store.py      # User profile persistence (JSON)
├── requirements.txt
├── .env                      # API key (Groq)
└── README.md
```

---

##  Setup & Installation


### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Anthropic API key
Edit the `.env` file:
```
GROQ_API_KEY=your_api_key_here
```


### 3. Run the app
```bash
streamlit run app.py
```

##  How It Works

1. **User sets profile** — name, location, activity type, age in the sidebar
2. **Live dashboard** fetches real weather data from Open-Meteo API
3. **Heat index** is calculated using the Steadman formula (same as used by meteorological agencies)
4. **Risk level** is classified using WHO  thresholds (Low / Moderate / High / Very High / Extreme Danger)
5. **Personalised recommendations** — water intake, rest schedule, activity-specific advice
6. **AI chat agent** answers natural language questions using LangChain + Claude
7. **Memory** — user profiles are saved to disk and reloaded in future sessions

---

## Supported Locations

The agent supports real-time monitoring for all 25 districts of Sri Lanka:
Ampara, Anuradhapura, Badulla, Batticaloa, Colombo, Galle, Gampaha, Hambantota, Jaffna, Kalutara, Kandy, Kegalle, Kilinochchi, Kurunegala, Mannar, Matale, Matara, Monaragala, Mullaitivu, Nuwara Eliya, Polonnaruwa, Puttalam, Ratnapura, Trincomalee, and Vavuniya.

---


## ⚠️ Disclaimer

This tool provides general heat safety guidance based on standard meteorological formulas. It is not a substitute for professional medical advice. In a heat emergency, seek immediate medical attention.
