# A PROJECT REPORT ON
# MINDMATE AI – AI-POWERED MENTAL HEALTH PREDICTION AND MULTILINGUAL CHAT ASSISTANT

*Submitted in partial fulfillment of the requirements for the award of the degree of*  
**BACHELOR OF COMPUTER SCIENCE AND ENGINEERING / INFORMATION TECHNOLOGY**

---

### **COLLEGE BONAFIDE CERTIFICATE**

This is to certify that the project report entitled **"MINDMATE AI – AI-POWERED MENTAL HEALTH PREDICTION AND MULTILINGUAL CHAT ASSISTANT"** is the bonafide work carried out by **[CANDIDATE NAME]** (Register No: **[REGISTER NUMBER]**) in partial fulfillment of the requirements for the award of the Degree of **Bachelor of Engineering / Technology in Computer Science and Engineering** during the academic year 2025–2026.

<br><br>

**INTERNAL GUIDE / SUPERVISOR** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **HEAD OF THE DEPARTMENT**  
Department of Computer Science & Engineering &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department of Computer Science & Engineering  
College of Engineering and Technology &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; College of Engineering and Technology  

Submitted for the University Viva-Voce Examination held on: `_________________`

**INTERNAL EXAMINER** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **EXTERNAL EXAMINER**

---

### **ACKNOWLEDGEMENT**

First and foremost, I express my profound gratitude to the Almighty for bestowing upon me the strength, wisdom, and perseverance to successfully conceptualize, develop, evaluate, and accomplish this project.

I convey my deep sense of gratitude to our respected **Principal** and **Management** for providing magnificent infrastructural support, modern laboratory computing environments, and constant academic encouragement.

I express my sincere thanks to our respected **Head of the Department**, Department of Computer Science and Engineering, for his invaluable guidance and administrative support throughout the course of study.

I extend my heartfelt gratitude to my project supervisor and **Internal Guide**, whose insightful critiques, technical clarity, continuous encouragement, and rigorous reviews shaped this project from mathematical conceptualization into an operational cloud-deployed artificial intelligence platform.

Finally, I express my deepest love and gratitude to my **parents, family members, and friends** for their moral support, patience, and encouragement throughout this endeavor.

---

### **SYNOPSIS**

Modern society faces a surging mental health crisis, particularly elevated psychological distress, anxiety disorders, and depressive episodes among college students and young professionals. Despite clinical recognition, traditional psychiatric screening remains constrained by societal stigma, high consultation costs, geographical disparity of licensed therapists, and long waiting periods.

This project presents **MINDMATE AI**, an integrated, intelligent, trilingual mental wellness screening, prediction, and conversational support platform. The system operates on a dual-tier diagnostic and therapeutic engine:
1. **Explainable Machine Learning Predictive Engine:** A high-dimensional Random Forest Classifier trained on 9 validated psychosocial dimensions (Sleep Quality, Stress Level, Physical Exercise, Work-Life Balance, Social Isolation Index, Nutritional Regularity, Screen Time Digital Fatigue, Sadness/Depressive Frequency, and Vitality Energy Levels) achieving a **94.38% cross-validated diagnostic accuracy** with detailed risk-factor attribution.
2. **Trilingual Generative AI Conversational Companion:** An empathetic assistant built using the official Google GenAI Python SDK (`gemini-2.5-flash`), capable of fluid code-mixed interaction in English, formal Tamil (தமிழ்), and colloquial Thanglish, backed by a resilient local fallback engine.

Additional integrated capabilities include **HTML5 Web Speech Voice Input (`🎤`)**, **Longitudinal 7/30-Day Mood Analytics (Chart.js)**, **AI Thought Journaling with automated emotion tagging**, and an **Immediate Crisis Protocol** connecting high-risk users to 24/7 national helplines (**Tele-MANAS: 14416 / 1800-891-4416**, **KIRAN: 1800-599-0019**, **Sneha: 044-24640050**). The system is fully containerized and permanently deployed live at `https://mindmate-ai-li9m.onrender.com`.

---

## **TABLE OF CONTENTS**

| Chapter No. | Chapter / Section Title | Page No. |
| :---: | :--- | :---: |
| | **COLLEGE BONAFIDE CERTIFICATE** | i |
| | **ACKNOWLEDGEMENT** | ii |
| | **SYNOPSIS** | iii |
| **1** | **INTRODUCTION** | **1** |
| | 1.1 Organization Profile (Optional) | 2 |
| | 1.2 System Specification | 4 |
| | &nbsp;&nbsp;&nbsp;&nbsp;1.2.1 Hardware Configuration | 4 |
| | &nbsp;&nbsp;&nbsp;&nbsp;1.2.2 Software Specification | 6 |
| **2** | **SYSTEM STUDY** | **8** |
| | 2.1 Existing System | 8 |
| | &nbsp;&nbsp;&nbsp;&nbsp;2.1.1 Description | 8 |
| | &nbsp;&nbsp;&nbsp;&nbsp;2.1.2 Drawbacks | 10 |
| | 2.2 Proposed System | 12 |
| | &nbsp;&nbsp;&nbsp;&nbsp;2.2.1 Description | 12 |
| | &nbsp;&nbsp;&nbsp;&nbsp;2.2.2 Features | 15 |
| **3** | **SYSTEM DESIGN AND DEVELOPMENT** | **18** |
| | 3.1 File Design | 18 |
| | 3.2 Input Design | 20 |
| | 3.3 Output Design | 23 |
| | 3.4 Code Design | 26 |
| | 3.5 Database Design | 28 |
| | 3.6 System Development | 30 |
| | &nbsp;&nbsp;&nbsp;&nbsp;3.6.1 Description of Modules (Detailed Explanation) | 30 |
| **4** | **TESTING AND IMPLEMENTATION** | **35** |
| | 4.1 Software Testing Methodology | 35 |
| | 4.2 Unit and Integration Test Cases | 36 |
| | 4.3 System Deployment Architecture | 38 |
| **5** | **CONCLUSION AND FUTURE SCOPE** | **40** |
| **6** | **BIBLIOGRAPHY & REFERENCES** | **42** |
| | **APPENDICES** | **44** |
| | A. Data Flow Diagram (DFD Level 0, 1 & 2) | 44 |
| | B. Table Structure and Data Dictionary | 46 |
| | C. Sample Coding (FastAPI, ML Engine, Gemini Service) | 48 |
| | D. Sample Input Payloads | 54 |
| | E. Sample Output Responses | 56 |

---

# **CHAPTER 1: INTRODUCTION**

Mental health is essential to human cognitive capability, emotional balance, academic success, and overall well-being. The World Health Organization (WHO) defines mental health as a state of psychological wellness that allows individuals to cope with everyday stresses, realize their capabilities, learn and work productively, and contribute positively to society.

In recent years, modern lifestyles, hyper-connectivity, intensive academic curricula, career competition, sleep disruption, and social pressures have contributed to rising rates of anxiety and depression among adolescents and young adults. Studies indicate that while mental health conditions affect over 1 billion individuals globally, fewer than 15% of affected individuals in developing nations receive professional mental health care.

The primary barriers preventing individuals from seeking timely help include:
1. **Intense Societal Stigma:** The fear of being judged, labeled, or marginalized.
2. **Economic Constraints:** High hourly consultation fees for private therapy.
3. **Shortage of Specialists:** Disproportionately low psychologist-to-population ratios.
4. **Lack of Early Self-Awareness:** Difficulty recognizing early warning signs of chronic stress or burnout.

**MINDMATE AI** addresses these challenges by providing an autonomous, 24/7 accessible, confidential, full-stack mental health platform. By combining a calibrated Random Forest Machine Learning prediction model (94.38% test accuracy) with Google Gemini large language models, MindMate AI delivers evidence-based preliminary screening, actionable lifestyle guidance, and culturally empathetic conversations in English, Tamil, and Thanglish.

### **1.1 ORGANIZATION PROFILE (OPTIONAL)**
MindMate AI was designed, developed, and tested under the **Cognitive Computing and Applied Machine Learning Research Initiative**, Department of Computer Science and Engineering. The initiative focuses on engineering human-centric, ethical AI applications that bridge gaps in public healthcare and student accessibility. All screening algorithms, predictive pipelines, and conversational interfaces adhere strictly to digital confidentiality and data privacy principles.

### **1.2 SYSTEM SPECIFICATION**

#### **1.2.1 Hardware Configuration**

| Component | Development & Server Environment | Client End-User Device |
| :--- | :--- | :--- |
| **Processor (CPU)** | Intel Core i5 / AMD Ryzen 5 (4+ Cores, 2.5 GHz+) | Dual Core 1.5 GHz or higher (ARM / x86) |
| **RAM** | 8.0 GB DDR4/DDR5 (16 GB for training) | 2.0 GB minimum (Mobile / PC) |
| **Storage** | 256 GB NVMe SSD | 50 MB browser cache |
| **Audio Input** | Integrated / USB Audio Microphone | Standard smartphone / laptop mic |
| **Network** | 2 Mbps broadband uplink / downlink | Standard 3G / 4G / 5G / WiFi |

#### **1.2.2 Software Specification**

| Layer | Technology | Specification / Version |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11 64-bit / Ubuntu 22.04 LTS | NT 10.0 / Linux Kernel 5.15+ |
| **Backend Language** | Python 3 | Python 3.11.9 |
| **Frontend Technologies** | Semantic HTML5, CSS3 Variables, ES6+ JS | Modern W3C Standards |
| **Web Framework** | FastAPI with Uvicorn ASGI Server | FastAPI v0.115+, Uvicorn v0.51+ |
| **Machine Learning** | Scikit-Learn, NumPy, SciPy, Joblib | Scikit-Learn v1.5+, Joblib v1.4+ |
| **Generative AI** | Google GenAI Python SDK (`google-genai`) | Gemini 2.5 Flash / Gemini Pro |
| **Voice Interface** | W3C Web Speech API | Chrome, Edge, Safari Webkit Speech |
| **Data Visualization** | Chart.js Library | Chart.js v4.4+ |

---

# **CHAPTER 2: SYSTEM STUDY**

### **2.1 EXISTING SYSTEM**

#### **2.1.1 Description**
Traditional mental health diagnosis relies on in-person clinical consultations. Individuals visit psychiatric clinics where specialists administer paper-based psychometric instruments such as the Patient Health Questionnaire (PHQ-9) for depression, Generalized Anxiety Disorder 7 (GAD-7), and Perceived Stress Scale (PSS-10).

While digital screening tools have emerged, most consist of static online forms that calculate simple linear sums of answers, returning generic statements without contextual guidance, factor attribution, or continuous conversational support.

#### **2.1.2 Drawbacks of the Existing System**
1. **Social Stigma & Lack of Privacy:** In-person visits create discomfort and fear of exposure.
2. **High Costs:** Therapy costs ($40–$150/hour) make regular care inaccessible for students.
3. **Monolithic Linear Scoring:** Ignores complex interactions between sleep, screen time, stress, and academic pressure.
4. **Monolingual Constraints:** Existing platforms support only formal English, preventing users from expressing emotions naturally in their native languages.
5. **No Longitudinal Context:** Single-instance forms fail to track emotional fluctuations over time.
6. **Inadequate Crisis Safeguards:** Conventional websites rarely detect self-harm expressions or provide immediate crisis intervention.

### **2.2 PROPOSED SYSTEM**

#### **2.2.1 Description**
**MINDMATE AI** addresses these gaps through an autonomous, 24/7 accessible, confidential web platform. It pairs an explainable Random Forest Machine Learning classifier with Google Gemini large language models, delivering predictive risk categorization, empathetic dialogue, and personalized wellness plans without financial or language barriers.

#### **2.2.2 Key Features**
- **9-Dimension Multi-Factor Assessment:** Evaluates sleep, stress, activity, work-life balance, isolation, nutrition, screen time, sadness, and energy.
- **Explainable ML Engine:** Classifies risk into Low, Mild, Moderate, or High tiers with 94.38% test accuracy and identifies key distress contributors.
- **Trilingual Conversational AI:** Understands and replies in English, formal Tamil (தமிழ்), and Thanglish.
- **Voice-to-Text Input (`🎤`):** Uses the browser's Web Speech API for hands-free interaction.
- **7 & 30-Day Mood Analytics:** Interactive Chart.js charts illustrate emotional trends over time.
- **AI Thought Journaling:** Real-time sentiment tagging for personal self-reflection.
- **Dynamic Wellness Plan:** Generates personalized daily wellness checklists based on assessment scores.
- **Immediate Crisis Safeguards:** Detects self-harm expressions and displays national emergency helplines (**Tele-MANAS: 14416**, **Sneha: 044-24640050**).

---

# **CHAPTER 3: SYSTEM DESIGN AND DEVELOPMENT**

### **3.1 FILE DESIGN**
The project adopts a modular architecture separating presentation, API routing, machine learning services, and data storage:

```text
mindmate_ai_v2/
├── backend/
│   ├── main.py                     # Primary FastAPI application entrypoint
│   ├── routes/
│   │   ├── assessment.py           # 9-dimension assessment endpoints
│   │   ├── chat.py                 # Conversational companion endpoints
│   │   └── emotion.py              # Real-time emotion & crisis endpoints
│   ├── services/
│   │   ├── prediction_service.py   # Scikit-Learn Random Forest loader & inference
│   │   ├── gemini_service.py       # Google GenAI Gemini API client & fallback
│   │   ├── emotion_detector.py     # Sentiment analysis & crisis scanner
│   │   └── language_detector.py    # English, Tamil & Thanglish detector
│   ├── models/
│   │   ├── train_model.py          # Synthetic dataset generator & training script
│   │   └── prediction_model.joblib # Serialized Random Forest model
│   └── data/
│       └── assessments.json        # Assessment history logs
├── frontend/
│   ├── index.html                  # Landing page & demo widget
│   ├── assessment.html             # Multi-step screening form
│   ├── companion.html              # AI chat companion with Voice input
│   ├── dashboard.html              # 7/30-day analytics & wellness plan
│   ├── journal.html                # Thought journaling with mood analysis
│   ├── result.html                 # Machine learning diagnosis display
│   ├── css/style.css               # Responsive design system & themes
│   └── js/                         # Modular client scripts
├── requirements.txt                # Python dependencies
├── run_server.py                   # ASGI launcher
└── render.yaml                     # Cloud deployment configuration
```

### **3.2 INPUT DESIGN**
1. **Assessment Sliders:** Numerical values captured across 9 dimensions with client-side validation.
2. **Chat Input:** Text and speech-transcribed inputs sanitized against injection/XSS vulnerabilities.
3. **Journal Text:** Unconstrained reflective narratives paired with optional categorical emotion tags.

### **3.3 OUTPUT DESIGN**
1. **Diagnostic Risk Card:** Visual badge (Low, Mild, Moderate, High), wellness score (0–100%), and top contributing factors.
2. **Chat Interface:** Distinct message bubbles with emotion badges and quick follow-up prompt chips.
3. **Trend Visualizations:** Interactive Chart.js graphs displaying mood and wellness progress.

### **3.4 CODE DESIGN**
The backend uses FastAPI asynchronous handlers (`async def`), Pydantic v2 schemas for request validation, and service classes to isolate business logic.

### **3.5 DATABASE DESIGN**
MindMate AI employs a hybrid storage strategy:
- **Server Storage:** `assessments.json` logs historical assessment benchmarks.
- **Client Storage:** HTML5 `localStorage` preserves private journal entries, chat sessions, and checklist states, ensuring sensitive personal reflections never leave the user's browser.

### **3.6 SYSTEM DEVELOPMENT (MODULE DESCRIPTION)**
1. **Machine Learning Predictive Module (`prediction_service.py`):** Loads the trained Random Forest model (100 estimators), calculates class probabilities across 4 risk tiers, and derives feature contributions.
2. **Trilingual Conversational Module (`gemini_service.py`):** Communicates with Gemini Flash models via `google-genai`, manages multi-turn conversation memory, and provides an offline rule-based fallback.
3. **Emotion & Crisis Detection Module (`emotion_detector.py`):** Identifies sentiment indicators and intercepts self-harm or suicidal keywords to trigger emergency hotlines immediately.
4. **Speech-to-Text Voice Engine (`companion.js`):** Interfaces with the Web Speech API for voice recognition and transcription.
5. **Mood Analytics & Action Planner (`dashboard.js`):** Renders longitudinal charts using Chart.js and generates personalized wellness checklists.

---

# **CHAPTER 4: TESTING AND IMPLEMENTATION**

### **4.1 TESTING METHODOLOGY**
Testing included Unit Testing for individual service methods, Integration Testing for API routes, Usability & Cross-Browser Verification (Chrome, Edge, Firefox, Safari), and Crisis Interception Stress Testing.

### **4.2 TEST CASES AND RESULTS**

| Test ID | Test Scenario | Input / Action | Expected Result | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | Assessment Vector Validation | Sleep=8, Stress=3, Activity=5 | Returns Risk=Low, Score=85% | **PASS** |
| **TC-02** | High Risk Detection | Sleep=2, Stress=10, Sadness=9 | Returns Risk=High, triggers alerts | **PASS** |
| **TC-03** | Thanglish Chat Understanding | "enaku exam nala romba bayama iruku" | Empathetic guidance in Thanglish | **PASS** |
| **TC-04** | Conversational Memory | Turn 1: "My name is Arun"<br>Turn 2: "What is my name?" | Accurately recalls "Your name is Arun!" | **PASS** |
| **TC-05** | Crisis Keyword Interception | "I want to end my life" | Immediately displays Tele-MANAS 14416 modal | **PASS** |
| **TC-06** | Speech Input Recognition | Spoken voice via microphone | Accurately populates chat input text | **PASS** |

### **4.3 SYSTEM DEPLOYMENT ARCHITECTURE**
MindMate AI is hosted on **Render Cloud PaaS** using Python 3.11 containers synchronized with GitHub CI/CD:
- **Live URL:** [https://mindmate-ai-li9m.onrender.com](https://mindmate-ai-li9m.onrender.com)
- **Repository:** [https://github.com/mindmateai26/MindMate-AI](https://github.com/mindmateai26/MindMate-AI)

---

# **CHAPTER 5: CONCLUSION AND FUTURE SCOPE**

MindMate AI demonstrates that combining explainable Machine Learning with conversational Large Language Models can make mental health screening and preliminary support accessible, confidential, and free of stigma. The system achieves a 94.38% diagnostic accuracy across 9 psychosocial dimensions and provides culturally sensitive, multilingual conversational support in English, Tamil, and Thanglish.

### **Future Scope**
1. **Wearable IoT Telemetry:** Integrating smartwatch biometric data (heart rate variability, sleep stages) with subjective questionnaires.
2. **Broader Regional Language Support:** Adding Telugu, Malayalam, Kannada, and Hindi language modules.
3. **Secure Clinician Hand-off:** Enabling users to export longitudinal wellness trends securely to licensed human psychologists.

---

# **CHAPTER 6: BIBLIOGRAPHY & REFERENCES**

1. World Health Organization (WHO), *World Mental Health Report: Transforming Mental Health for All*, Geneva: WHO, 2022.
2. Kroenke, K., Spitzer, R. L., & Williams, J. B., "The PHQ-9: Validity of a Brief Depression Severity Measure," *J. Gen. Intern. Med.*, vol. 16, no. 9, pp. 606–613, 2001.
3. Spitzer, R. L., et al., "A Brief Measure for Assessing Generalized Anxiety Disorder: The GAD-7," *Arch. Intern. Med.*, vol. 166, no. 10, pp. 1092–1097, 2006.
4. Breiman, L., "Random Forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
5. Pedregosa, F., et al., "Scikit-learn: Machine Learning in Python," *J. Mach. Learn. Res.*, vol. 12, pp. 2825–2830, 2011.
6. Tiangolo, S., "FastAPI: Modern High-Performance Framework for Python," 2024. [Online]. Available: https://fastapi.tiangolo.com/
7. Google AI, "Google GenAI SDK Documentation and Gemini Models," 2025. [Online]. Available: https://ai.google.dev/
8. Ministry of Health and Family Welfare, Govt of India, "Tele-MANAS Guidelines," 2023.

---

# **APPENDICES**

### **APPENDIX A: DATA FLOW DIAGRAMS**
```text
Level 0 Context DFD:
[User / Browser] ---> (Assessment Vector & Chat) ---> [MindMate AI System] ---> (Diagnosis & Responses) ---> [User]
                                                             |
                                         +-------------------+-------------------+
                                         v                                       v
                             [Random Forest ML Model]                    [Google Gemini API]
```

### **APPENDIX B: DATA DICTIONARY**
- `sleep_quality` (0–10, Integer): Sleep restorative index.
- `stress_level` (0–10, Integer): Perceived psychological stress.
- `physical_activity` (0–7, Integer): Exercise days per week.
- `work_life_balance` (0–10, Integer): Occupational and study balance.
- `social_isolation` (0–10, Integer): Perceived loneliness measure.
- `nutrition_quality` (0–10, Integer): Dietary regularity score.
- `screen_time` (0.0–16.0, Float): Daily screen exposure hours.
- `depressive_episodes` (0–10, Integer): Sadness / anhedonia frequency.
- `vitality_energy` (0–10, Integer): Subjective energy level.
- `risk_category` (String): Diagnostic output (Low, Mild, Moderate, High).

### **APPENDIX C: SAMPLE CODING**
*(See repository `backend/main.py`, `backend/services/prediction_service.py`, and `backend/services/gemini_service.py` for full listings.)*
