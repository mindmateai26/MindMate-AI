# MindMate AI – Comprehensive Project Report & Technical Documentation

**Project Title:** MindMate AI – AI-Powered Mental Wellness Screening, ML Risk Prediction & Multilingual Conversational Companion  
**Domain:** Artificial Intelligence / Healthcare Informatics / Applied Machine Learning / Generative AI  
**Academic Year:** 2025–2026  
**Repository:** [https://github.com/mindmateai26/MindMate-AI](https://github.com/mindmateai26/MindMate-AI)  
**Deployment Platform:** FastAPI, Uvicorn, Scikit-Learn, Google GenAI (Gemini 2.5/3.6 Flash), Vanilla HTML5/CSS3/JavaScript  

---

## 1. Executive Summary

Mental health distress among undergraduate students, early-career researchers, and working professionals has reached critical levels globally. Due to acute social stigma, limited clinical availability, and financial hurdles, individuals frequently refrain from seeking timely clinical help until conditions manifest into debilitating burnout or severe psychological distress.

**MindMate AI** addresses this gap by engineering an empathetic, culturally-competent, privacy-first wellness screening and conversational companion web application. The platform provides:
1. **Explainable Machine Learning Screening**: A 9-dimensional multi-tier classification pipeline powered by a Scikit-Learn `RandomForestClassifier` trained on curated clinical behavioral factors (94.38% test accuracy).
2. **Context-Aware Multilingual Conversational AI**: A generative dialogue companion powered by the official `google-genai` SDK (Google Gemini Flash) with persistent session context and native multi-lingual support across English, Native Tamil (தமிழ்), and colloquial Thanglish.
3. **Voice Input Speech Recognition**: Native hands-free speech-to-text dictation utilizing the Web Speech API.
4. **AI-Assisted Journaling & Emotion Detection**: Private reflective journaling featuring automatic sentiment/mood classification and supportive psychological grounding feedback.
5. **Interactive 7/30-Day Mood Analytics & Personalized Plans**: Actionable daily wellness checklists customized dynamically to the individual’s risk tier, accompanied by interactive historical trend charts.
6. **Strict Crisis Intervention Safeguards**: Zero-latency emergency heuristics routing acute distress signals to verified national 24/7 helplines (**Tele-MANAS 14416**, **KIRAN 1800-599-0019**, **Sneha +91 44 2464 0050**).

---

## 2. Problem Statement & Objectives

### 2.1 Problem Statement
Traditional mental health applications often suffer from:
- **Linguistic and Cultural Inaccessibility**: Failure to understand colloquial regional phrasing (e.g., Indian English, Tamil transliteration / Thanglish).
- **Black-Box Algorithmic Predictions**: Returning opaque numbers without explaining *why* a user is categorized under a specific distress tier.
- **Fragmented User Experiences**: Disconnected tools requiring separate apps for tracking, journaling, and conversation.
- **Neglect of Acute Safety Protocols**: Lack of instant fail-safes during expressions of active self-harm or suicidal ideation.

### 2.2 Core Objectives
- **Objective 1**: Develop a lightweight, explainable machine learning model to categorize preliminary mental health risk into **Low**, **Mild**, **Moderate**, and **High** tiers.
- **Objective 2**: Build an empathetic AI companion capable of multi-turn conversational memory, handling non-English and code-mixed inputs natively.
- **Objective 3**: Implement hands-free accessibility through native browser Speech-to-Text integration.
- **Objective 4**: Create a unified single-page/multi-page web application featuring responsive dark/light theme switching, 7/30-day analytics, personalized wellness roadmaps, and private emotion-analyzed journaling.
- **Objective 5**: Guarantee 100% adherence to crisis intervention ethics with immediate emergency helpline presentation.

---

## 3. System Architecture & Component Design

The platform adopts a decoupled, modular micro-architecture:

```
[ Client Layer (Browser) ]
  ├── index.html (Unified Hub & Landing Showcase)
  ├── assessment.html (9-Step Validated Questionnaire)
  ├── companion.html (Real-time Chat with Voice Input 🎤)
  ├── journal.html (Reflective Journal with Emotion Analysis)
  ├── dashboard.html (7/30-Day Analytics & Personalized Plan)
  ├── result.html (Outcome, Probabilities & Contributing Factors)
  └── about.html (Architecture, Disclaimers & Ethics)
         │
         ▼ HTTP / REST (Fetch API / JSON)
[ FastAPI Server Layer (Python 3.11) ]
  ├── CORS Middleware & Static Route Handlers
  ├── /api/health (System status check)
  ├── /api/assessment/predict (ML prediction & feature weights)
  ├── /api/assessment/history (Record retrieval & local persistence)
  ├── /api/chat (Multi-turn conversational routing)
  └── /api/emotion (Sentiment, language & emergency checks)
         │
         ├──► [ Scikit-Learn Model ] (RandomForestClassifier in joblib)
         ├──► [ Language & Emotion Detector ] (Keyword & Pattern Matchers)
         └──► [ Google Gemini Flash SDK ] (Generative AI via google-genai)
```

---

## 4. Machine Learning & Predictive Modeling

### 4.1 Feature Engineering (The 9 Dimensions)
Each assessment evaluates 9 distinct clinical dimensions on a Likert scale (1 to 5):
1. `mood_rating`: Overall mood and emotional balance (1=Balanced to 5=Severely Depressed).
2. `stress_level`: Physical and psychological tension (1=Low to 5=Extreme Stress).
3. `sleep_quality`: Sleep consistency and restfulness (1=Restorative to 5=Severe Insomnia).
4. `concentration_difficulty`: Cognitive focus in lectures or tasks (1=None to 5=Inability to Focus).
5. `academic_work_pressure`: Workload and examination burden (1=Minimal to 5=Overwhelming).
6. `social_withdrawal`: Social connectedness versus isolation (1=Connected to 5=Completely Isolated).
7. `energy_level`: Somatic vitality and fatigue (1=High Energy to 5=Severe Fatigue).
8. `anxiety_frequency`: Frequency of panic or nervous apprehension (1=Rarely to 5=Constant Panic).
9. `daily_functioning_impact`: Ability to execute basic hygiene, meals, and tasks (1=Normal to 5=Impaired).

### 4.2 Model Training & Performance
- **Algorithm**: `RandomForestClassifier(n_estimators=120, max_depth=12, random_state=42)`
- **Dataset**: 800 synthetic clinical records reflecting realistic distribution patterns of academic stressors.
- **Performance**:
  - Training Accuracy: **98.25%**
  - Validation Accuracy: **94.38%**
  - High recall on acute "High Risk" instances to minimize false negatives in critical cases.
- **Explainability**: Using feature importance weights, the system outputs an array of `contributingFactors` ranked by impact, providing actionable explanations for every user.

---

## 5. Conversational AI & Linguistic Empathy

### 5.1 Google Gemini Generative Integration
MindMate AI utilizes the official `google-genai` Python library. It dynamically connects to `gemini-3.6-flash` / `gemini-2.5-flash`:
- **Context Retention**: Maintains active session history (up to recent 10 conversational turns), enabling it to remember user names, specific test worries, and previously discussed coping techniques.
- **Token Calibration**: Output limits set to 2,500 tokens to prevent abrupt mid-sentence cutoffs during transliterated or Tamil script generation.

### 5.2 Trilingual & Code-Mixed Intelligence
- **English**: Structured psycho-educational guidance, CBT-inspired thought reframing, and progressive relaxation instructions.
- **Native Tamil (தமிழ்)**: Native script empathetic dialogue and culturally respectful phrases.
- **Thanglish**: Code-mixed transliteration (e.g., *"Ayyoo tension aagathinga bro... mudhala oru glass thanni kudinga"*), delivering warm peer-level empathy.

### 5.3 Resilient Fallback Engine
If an external API quota spike or network outage occurs, the local rule-based companion immediately handles dialogue, ensuring zero application downtime.

---

## 6. Frontend Innovation & Accessibility

- **Responsive SaaS/Card UI**: Designed with calming medical-grade aesthetics (`Inter` font, soft teals `#0d9488`, indigo `#6366f1`, and clean slate surfaces).
- **Light & Dark Theme Engine**: Complete CSS variable mapping (`--bg-main`, `--bg-card`, `--border`, `--text-main`) with persistent client state in `localStorage`.
- **Hands-Free Speech-to-Text (`🎤`)**: Integrated Web Speech API enables users under physical fatigue or motor strain to speak directly in English and Tamil.
- **AI Journaling Studio**: Instant emotion categorization of daily notes with constructive AI reflections.
- **7/30-Day Dynamic Trend Visuals**: Interactive bar charts tracking distress trajectories across days and weeks.
- **Personalized Action Checklist**: Tailored daily wellness goals that users can check off as completed.

---

## 7. Safety, Ethics & Crisis Safeguards

MindMate AI adheres strictly to digital mental health ethical standards:
- **Mandatory Medical Disclaimers**: Displayed prominently across the header, assessment submission, and results pages, clarifying that MindMate is an educational tool and **not** a clinical diagnostic device.
- **Real-Time Crisis Interception**: Any phrase containing keywords like *"end my life"*, *"kill myself"*, or *"harm myself"* bypasses standard chat generation to trigger an emergency response displaying 24/7 verified crisis numbers:
  - **Tele-MANAS**: `14416` / `1800-891-4416` (Toll-Free, 24/7)
  - **Kiran Mental Health**: `1800-599-0019`
  - **Sneha Suicide Prevention**: `+91 44 2464 0050`
  - **National Emergency Response**: `112`

---

## 8. Installation, Setup & Verification

### 8.1 Prerequisites
- Python 3.11+
- Git

### 8.2 Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/mindmateai26/MindMate-AI.git
cd MindMate-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (optional for live Gemini)
copy backend\.env.example backend\.env
# Open backend/.env and insert your GEMINI_API_KEY

# 4. Start the server
python run_server.py
```
Access the application at `http://127.0.0.1:8000`.

### 8.3 Automated Test Verification
```bash
# Run API endpoint tests
python tests/test_api.py

# Run frontend assets & HTML route tests
python tests/test_frontend_assets.py

# Run conversation & multi-turn memory tests
python tests/test_conversation.py

# Run ML model inference tests
python tests/test_prediction.py
```

---

## 9. Conclusion & Future Roadmap

**MindMate AI** successfully demonstrates the integration of modern web technologies, explainable machine learning, and generative language models into an accessible mental health support platform.

### Future Roadmap:
1. **Wearable IoT Sync**: Integrating real-time heart rate variability (HRV) and sleep trackers from smartwatches.
2. **Clinical Appointment Booking**: Secure, encrypted referral channels connecting high-risk students directly to campus counselors.
3. **Voice Tone Analysis**: Acoustic prosody and pitch fluctuation analysis to detect emotional strain beyond text semantics.
