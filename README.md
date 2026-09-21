# MindMate AI – AI-Powered Mental Wellness Screening, Prediction & Companion

A full-stack, student-friendly mental health application engineered from scratch. **MindMate AI** offers preliminary self-report screening, Machine Learning risk category predictions, an empathetic multilingual conversational companion (powered by Google Gemini and a local fallback engine), emotion/stress detection, assessment history tracking, and crisis intervention safeguards.

[![Live Demo](https://img.shields.io/badge/Live_Website-Available_24%2F7-brightgreen?style=for-the-badge&logo=render)](https://mindmate-ai-li9m.onrender.com)
🔗 **Permanent Live Website:** [https://mindmate-ai-li9m.onrender.com](https://mindmate-ai-li9m.onrender.com)

> **Academic Project Disclaimer:**  
> MindMate AI is strictly an educational/preliminary wellness screening tool and **NOT a certified medical diagnostic device**. It does not substitute for clinical mental healthcare or psychiatric diagnosis.

---

## 🌟 Key Features

1. **Mental Wellness Screening Form (`/assessment.html`)**:
   - 9 structured self-assessment dimensions: *Mood, Stress, Sleep Quality, Concentration, Academic/Work Pressure, Social Withdrawal, Vitality/Energy, Anxiety Apprehension, and Daily Functioning*.
   - Validated step-by-step interface with dynamic progress tracking.
2. **Explainable ML Prediction Pipeline (`/result.html`)**:
   - Scikit-Learn `RandomForestClassifier` trained on 800+ realistic screening samples (94.38% test accuracy).
   - Categorizes risk into **Low**, **Mild**, **Moderate**, and **High** tiers.
   - Highlights specific top contributing distress factors and tailored wellness recommendations.
3. **Conversational AI Companion (`/companion.html`)**:
   - Built using the official `google-genai` Python SDK (`gemini-2.5-flash`).
   - Session context memory: accurately remembers names, exam stressors, and earlier concerns across conversation turns.
   - Resilient architecture: seamlessly engages in active conversation via a local fallback engine if no API key is provided.
4. **Trilingual & Mixed-Language Understanding**:
   - Supports **English**, native **Tamil (தமிழ்)** script, and colloquial **Thanglish** (e.g., *"enaku romba stress ah iruku"*).
5. **Emotion & Crisis Detection**:
   - Detects emotions: *Sadness, Stress, Anxiety, Anger, Loneliness, Academic pressure, and Positive/Neutral*.
   - Real-time crisis detection for self-harm signals, immediately presenting verified 24/7 helplines (**Tele-MANAS 14416**, **KIRAN 1800-599-0019**, **Sneha India +91 44 2464 0050**, Emergency **112**).
6. **Wellness Dashboard (`/dashboard.html`)**:
   - Displays latest screening scores, risk category badges, dominant distress drivers, and historical assessment logs.

---

## 🏗️ Project Structure

```text
mindmate_ai_v2/
├── frontend/
│   ├── index.html              # Home page with hero, features, workflow, crisis modal
│   ├── assessment.html         # 9-question interactive validated screening form
│   ├── result.html             # Dedicated prediction result page with factors & suggestions
│   ├── companion.html          # Conversational chat UI with language selector & quick prompts
│   ├── dashboard.html          # Historical assessments, latest score, risk badge
│   ├── about.html              # Tech stack, ML explainability, limitations, disclaimer
│   ├── css/
│   │   └── style.css           # Calming, modern, card-based responsive design
│   └── js/
│       ├── app.js              # Common utilities, API client, crisis modal
│       ├── assessment.js       # Screening step navigation, validation, submission
│       ├── companion.js        # Multi-turn chat handling, quick pills, emotion tags
│       └── dashboard.js        # Score cards, history table, dynamic badges
│
├── backend/
│   ├── main.py                 # FastAPI application, CORS, static file serving
│   ├── requirements.txt        # Backend dependencies
│   ├── .env.example            # Environment template
│   ├── .env                    # Runtime configuration (API keys, ports)
│   ├── routes/
│   │   ├── assessment.py       # POST /api/assessment/predict, GET /api/assessment/history
│   │   ├── chat.py             # POST /api/chat
│   │   └── emotion.py          # POST /api/emotion
│   ├── services/
│   │   ├── gemini_service.py     # Official google-genai SDK wrapper + contextual memory
│   │   ├── prediction_service.py # Scikit-learn model loading & inference
│   │   ├── emotion_detector.py   # Multi-lingual emotion & crisis detection
│   │   └── language_detector.py  # Language classifier (en, ta, thanglish)
│   ├── models/
│   │   └── prediction_model.joblib # Trained ML model & feature weights
│   └── data/
│       ├── sample_data.csv       # Training dataset for risk assessment
│       └── assessments.json      # Student-friendly persistent storage
│
├── ml/
│   ├── generate_data.py        # Generates realistic synthetic screening dataset
│   └── train_model.py          # Reproducible ML training pipeline
│
├── tests/
│   ├── test_api.py             # API route tests (health, predict, history, emotion, chat)
│   ├── test_prediction.py      # ML inference and boundary tests
│   └── test_conversation.py    # Multi-turn context, Tamil, Thanglish, and emergency tests
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3 (Custom Variables, Flexbox, CSS Grid), Vanilla JavaScript (ES6+) |
| **Backend API** | Python 3.11+, FastAPI, Uvicorn, Pydantic V2, python-dotenv |
| **Machine Learning** | Scikit-Learn (Random Forest), Pandas, NumPy, Joblib |
| **Generative AI** | Google Gemini API via official `google-genai` Python SDK (`gemini-2.5-flash`) |
| **Testing** | Pytest / Unittest, FastAPI TestClient, urllib automated verification |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Installation
Open a terminal in the project directory:
```bash
cd mindmate_ai_v2
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the `.env.example` file to `.env`:
```bash
copy backend\.env.example backend\.env
```
Open `backend/.env` and insert your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=8000
HOST=127.0.0.1
```
*(Note: If `GEMINI_API_KEY` is left blank, MindMate AI will automatically engage its intelligent local companion engine so all features, session memories, and tests remain fully functional.)*

---

## 🧠 Training the ML Model

To re-train the Random Forest risk classification model:
```bash
python ml/train_model.py
```
**Output Highlights:**
- Evaluated on 640 training / 160 testing samples.
- Test accuracy: **94.38%**.
- Serialized to `backend/models/prediction_model.joblib`.

---

## 🏃 Running the Application

Start the FastAPI unified web server:
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your web browser and navigate to:
👉 **`http://127.0.0.1:8000`**

### Available Pages:
- **Home**: `http://127.0.0.1:8000/index.html`
- **Assessment Form**: `http://127.0.0.1:8000/assessment.html`
- **Prediction Result**: `http://127.0.0.1:8000/result.html`
- **AI Companion Chat**: `http://127.0.0.1:8000/companion.html`
- **Dashboard**: `http://127.0.0.1:8000/dashboard.html`
- **About Project**: `http://127.0.0.1:8000/about.html`
- **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status and Gemini configuration check |
| `POST` | `/api/assessment/predict` | Predicts risk tier, composite score, and factor breakdown |
| `GET` | `/api/assessment/history` | Fetches historical screening sessions |
| `POST` | `/api/chat` | Context-aware chat with emotion and language detection |
| `POST` | `/api/emotion` | Detects emotion, language, and crisis/self-harm triggers |

### Chat Request Payload Example:
```json
{
  "message": "My name is Priya",
  "history": [],
  "language": "auto",
  "assessmentContext": {
    "riskCategory": "Mild",
    "score": 38.5
  }
}
```

### Chat Response Payload Example:
```json
{
  "text": "Hello Priya! It's very nice to meet you. How are you feeling today, and what is on your mind?",
  "moodTag": "Positive / Neutral",
  "language": "en",
  "source": "gemini",
  "isEmergency": false,
  "followUps": [
    "I'm feeling a bit stressed",
    "Just wanted to chat",
    "I took the screening test"
  ]
}
```

---

## 🧪 Running the Test Suite

Execute the automated test suites:
```bash
# 1. Test ML Predictions & Scoring
python tests/test_prediction.py

# 2. Test Multi-Turn Context Memory & Trilingual Support
python tests/test_conversation.py

# 3. Test All FastAPI Endpoints
python tests/test_api.py
```

### Verified Test Cases:
1. **Multi-Turn Context Flow**:
   - Turn 1: *"My name is Priya"* $\rightarrow$ AI greets Priya warmly.
   - Turn 2: *"I am feeling stressed about my exams"* $\rightarrow$ AI discusses exam pressure without repeating welcome greetings.
   - Turn 3: *"What is my name and why am I stressed?"* $\rightarrow$ AI recalls: *"Your name is Priya, and you mentioned that you are feeling stressed about your exams..."*
2. **Thanglish Parsing**:
   - User: *"enaku romba stress ah iruku"* $\rightarrow$ AI detects `thanglish`, tags `Stress`, responds supportively in colloquial Thanglish.
3. **Tamil Script Parsing**:
   - User: *"எனக்கு ரொம்ப கவலையாக இருக்கு"* $\rightarrow$ AI detects `ta`, tags `Sadness`/`Anxiety`, responds in natural Tamil.
4. **Crisis Detection Safeguard**:
   - User: *"I feel like ending my life, I want to kill myself"* $\rightarrow$ Flagged `isEmergency: True`, immediately issues Tele-MANAS (14416) & Sneha (+91 44 2464 0050) crisis protocol.

---

## 🔒 Security & Privacy Practices

- **Never Expose Secrets**: The Gemini API key is stored exclusively in backend `.env` and loaded via Python environment variables. No client-side JavaScript ever sees or transmits the key.
- **Git Ignore**: `.env`, compiled files, and virtual environments are tracked in `.gitignore`.
- **Safe Error Handling**: Server errors return standard HTTP error models without exposing Python stack traces.
