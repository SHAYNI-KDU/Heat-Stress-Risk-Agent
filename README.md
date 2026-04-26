# 🌡️ Heat Stress Risk Agent

An autonomous AI agent that protects people in Sri Lanka from dangerous heat conditions.

Built for the **KDU BSc Applied Data Science Communication** assignment (LB3114, Intake 41).

---

## 📌 Features

- **Real-time weather data** via Open-Meteo API (free, no API key required)
- **Scientifically accurate heat index** using the Steadman formula
- **Risk classification** based on WHO / OSHA heat stress thresholds
- **Personalised advice** for farmers, construction workers, athletes, and elderly people
- **Conversation memory** — saves user profiles across sessions
- **Interactive Streamlit dashboard** with live metrics and hourly forecast chart
- **AI-powered chat agent** built with LangChain + OpenAI GPT-4o

---

## 🗂️ Project Structure

```
heat-stress-agent/
│
├── app.py                    # Streamlit UI — main entry point
├── agent.py                  # LangChain agent with tools
├── tools/
│   ├── weather.py            # Open-Meteo API integration
│   ├── heat_index.py         # Steadman heat index formula
│   └── risk_classifier.py    # WHO/OSHA risk classification
├── memory/
│   └── profile_store.py      # User profile persistence (JSON)
├── requirements.txt
├── .env                      # API key (do not commit to GitHub)
└── README.md
```

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/heat-stress-agent
cd heat-stress-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Anthropic API key
Edit the `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```
Get a free API key at [platform.openai.com](https://platform.openai.com)

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🧠 How It Works

1. **User sets profile** — name, location, activity type, age in the sidebar
2. **Live dashboard** fetches real weather data from Open-Meteo API
3. **Heat index** is calculated using the Steadman formula (same as used by meteorological agencies)
4. **Risk level** is classified using WHO / OSHA thresholds (Low / Moderate / High / Very High / Extreme Danger)
5. **Personalised recommendations** — water intake, rest schedule, activity-specific advice
6. **AI chat agent** answers natural language questions using LangChain + Claude
7. **Memory** — user profiles are saved to disk and reloaded in future sessions

---

## 📍 Supported Locations

Kandy, Colombo, Galle, Jaffna, Trincomalee, Anuradhapura, Batticaloa, Negombo

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| LangChain | Agent framework |
| OpenAI GPT-4o | LLM reasoning |
| Open-Meteo API | Free weather data |
| Plotly | Charts |
| python-dotenv | Environment variable management |

---

## ⚠️ Disclaimer

This tool provides general heat safety guidance based on standard meteorological formulas. It is not a substitute for professional medical advice. In a heat emergency, seek immediate medical attention.
