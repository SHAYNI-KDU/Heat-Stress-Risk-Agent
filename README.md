# Heat Stress Risk Agent

An autonomous AI agent that protects people in Sri Lanka from dangerous heat conditions.

Built for the KDU BSc Applied Data Science Communication assignment (LB3114, Intake 41).

## YT Link :  https://youtube.com/shorts/q2SCJA6JYfk?feature=share

---

## Features

- **Real-time weather data** via Open-Meteo API (free, no API key required)
- **Scientifically accurate heat index** using the Steadman formula
- **Risk classification** based on WHO heat stress thresholds
- **All 25 Sri Lanka districts** supported
- **Personalised advice** for farmers, construction workers, athletes, and elderly people
- **Best hours highlighter** — shows safest outdoor working hours based on forecast
- **Heat Stroke First Aid Guide** with Sri Lanka emergency numbers
- **Conversation memory** — agent remembers previous messages in session
- **Interactive Streamlit dashboard** with live metrics and hourly forecast chart
- **AI-powered chat agent** built with LangChain + Groq Llama3 (free)
- **Custom activity input** — type any activity not listed in the dropdown

---

##  Project Structure

```
heat-stress-agent/
│
├── app.py                    # Streamlit UI — main entry point
├── agent.py                  # LangChain agent with tools
├── background.png            # Background image (optional)
├── tools/
│   ├── __init__.py
│   ├── weather.py            # Open-Meteo API integration
│   ├── heat_index.py         # Steadman heat index formula
│   └── risk_classifier.py    # WHO risk classification
├── memory/
│   ├── __init__.py
│   └── profile_store.py      # User profile persistence (JSON)
├── requirements.txt
├── .env                      
└── README.md
```

---

##  Setup & Installation

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Groq API key
Edit the `.env` file:
```
GROQ_API_KEY=your_api_key_here
```
Get a **free** API key at [console.groq.com](https://console.groq.com)

### 3. Run the app
```bash
streamlit run app.py
```



---

##  How It Works

1. **User sets profile** — name, location, activity type, age in the sidebar
2. **Live dashboard** fetches real weather data from Open-Meteo API
3. **Heat index** is calculated using the Steadman formula (same as used by meteorological agencies worldwide)
4. **Risk level** is classified using WHO / OSHA thresholds:
   - Low (< 27°C)
   - Moderate (27–33°C)
   - High (33–40°C)
   - Very High (40–51°C)
   - Extreme Danger (51°C+)
5. **Personalised recommendations** — water intake, rest schedule, activity-specific advice
6. **Best hours** — automatically identifies safest outdoor working hours from hourly forecast
7. **AI chat agent** answers natural language questions using LangChain + Groq Llama3
8. **Memory** — agent remembers conversation history within each session
9. **First Aid Guide** — heat stroke signs, treatment steps, and Sri Lanka emergency numbers

---

## Supported Districts (All 25)

Ampara, Anuradhapura, Badulla, Batticaloa, Colombo, Galle, Gampaha, Hambantota, Jaffna, Kalutara, Kandy, Kegalle, Kilinochchi, Kurunegala, Mannar, Matale, Matara, Monaragala, Mullaitivu, Nuwara Eliya, Polonnaruwa, Puttalam, Ratnapura, Trincomalee, Vavuniya

---

##  Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| LangChain | Agent framework |
| Groq Llama3 | LLM reasoning (free) |
| Open-Meteo API | Free real-time weather data |
| Plotly | Interactive charts |
| python-dotenv | Environment variable management |

---


## Disclaimer

This tool provides general heat safety guidance based on standard meteorological formulas. It is not a substitute for professional medical advice. In a heat emergency, seek immediate medical attention and call **1990**.

