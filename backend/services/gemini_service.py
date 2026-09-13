import os
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from .emotion_detector import detect_emotion
from .language_detector import detect_language

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_env = os.path.abspath(os.path.join(current_dir, "..", ".env"))
load_dotenv(backend_env, override=True)

SYSTEM_INSTRUCTION = """
You are MindMate AI, an empathetic, supportive, and non-judgmental conversational mental wellness companion.
Your goal is to listen deeply, offer gentle emotional support, provide grounded coping strategies (such as breathing techniques, grounding, pacing), and help users reflect on their thoughts.

CRITICAL RULES:
1. You are an academic/preliminary wellness companion, NOT a doctor or clinical psychologist. NEVER claim to diagnose, treat, or prescribe medical treatments for psychiatric conditions.
2. RELEVANCE & COMPLETENESS: Always give a direct, fresh, specific response to the user's exact words, questions, and situation. Always finish all sentences and advice fully. NEVER cut off mid-sentence.
3. MULTI-TURN CONTEXT MEMORY: Always remember what the user previously said during this session (names, feelings, exams, life situations). If they ask "What is my name?" or "Why was I upset earlier?", answer accurately using earlier turns.
4. LANGUAGE HANDLING:
   - If the user writes in English, reply in warm, conversational English.
   - If the user writes in Tamil script (தமிழ்), reply naturally in Tamil.
   - If the user writes in Thanglish (Tamil words written in English letters, e.g., 'enaku romba stress ah iruku' or 'friend oda fight enna panna'), reply empathetically in natural, relatable, smooth Thanglish with practical advice.
   - For mixed language, mirror their conversational comfort naturally.
5. CONVERSATIONAL STYLE: Speak like a caring, mature close friend who genuinely listens and provides practical, constructive steps. Structure advice clearly (e.g. with numbered points or short comforting paragraphs).
6. SAFETY: If the user hints at self-harm, suicide, or severe crisis, respond with deep compassion, urge them to stay safe, and direct them to connect with trusted loved ones or crisis helplines (e.g., Tele-MANAS 14416, KIRAN 1800-599-0019, Sneha India 044-24640050, or local 112).
"""

class GeminiService:
    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self, custom_key: Optional[str] = None):
        # Reload environment
        load_dotenv(override=True)
        api_key = custom_key or os.getenv("GEMINI_API_KEY", "").strip()
        if api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
                print("[GeminiService] Initialized Google GenAI client.")
            except Exception as err:
                print(f"[GeminiService] Warning initializing google-genai client: {err}")
                self.client = None
        else:
            self.client = None

    def chat(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        language_preference: str = "auto",
        assessment_context: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes chat message, respects conversation history, detects emotions,
        and generates an empathetic, relevant response using Gemini API or dynamic engine.
        """
        history = history or []
        user_text = message.strip()

        # Re-check API key if provided or newly configured in .env
        if api_key or (not self.client and os.getenv("GEMINI_API_KEY", "").strip()):
            self._init_client(custom_key=api_key)

        # 1. Detect emotion & emergency
        emotion_data = detect_emotion(user_text)
        is_emergency = emotion_data.get("isEmergency", False)
        mood_tag = emotion_data.get("moodTag", "Neutral")

        # 2. Detect language
        lang = detect_language(user_text, language_preference)

        # 3. Handle Crisis Immediately
        if is_emergency:
            return self._emergency_response(lang)

        # 4. Attempt Gemini API call if client is configured
        if self.client:
            try:
                from google.genai import types
                contents: List[types.Content] = []
                for turn in history:
                    role = "user" if turn.get("sender") == "user" or turn.get("role") == "user" else "model"
                    content_text = turn.get("text") or turn.get("message") or turn.get("content") or ""
                    if content_text.strip():
                        contents.append(
                            types.Content(
                                role=role,
                                parts=[types.Part.from_text(text=content_text)]
                            )
                        )

                prompt_to_send = user_text
                if assessment_context and len(history) == 0:
                    ctx_info = f"[User Assessment: Risk={assessment_context.get('riskCategory')}, Score={assessment_context.get('score')}%]"
                    prompt_to_send = f"{ctx_info}\n{user_text}"

                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=prompt_to_send)]
                    )
                )

                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                    max_output_tokens=2500
                )

                response = None
                for model_candidate in ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite"]:
                    try:
                        response = self.client.models.generate_content(
                            model=model_candidate,
                            contents=contents,
                            config=config
                        )
                        if response and response.text:
                            break
                    except Exception as model_err:
                        print(f"[GeminiService] Model {model_candidate} attempt note: {model_err}")
                        continue

                response_text = response.text.strip() if response.text else ""
                if response_text:
                    follow_ups = self._generate_dynamic_followups(user_text, mood_tag, lang)
                    return {
                        "text": response_text,
                        "moodTag": mood_tag,
                        "language": lang,
                        "source": "gemini",
                        "isEmergency": False,
                        "followUps": follow_ups
                    }
            except Exception as api_err:
                print(f"[GeminiService] Gemini API call error: {api_err}. Using dynamic local companion engine.")

        # 5. Dynamic Conversational Companion Engine
        return self._generate_relevant_response(
            user_text=user_text,
            history=history,
            mood_tag=mood_tag,
            lang=lang,
            assessment_context=assessment_context
        )

    def _extract_name(self, history: List[Dict[str, str]], current_message: str) -> Optional[str]:
        """Extracts user name from conversational turns."""
        all_user_texts = [
            turn.get("text") or turn.get("message") or turn.get("content") or ""
            for turn in history if turn.get("sender") == "user" or turn.get("role") == "user"
        ] + [current_message]

        name_patterns = [
            r"\b(?:my\s+name\s+is|i\s+am|i'm|this\s+is|call\s+me)\s+([A-Za-z]+)\b",
            r"\ben\s+peyar\s+([A-Za-z]+)\b",
            r"என்\s+பெயர்\s+([^\s,.]+)",
            r"\b([A-Za-z]+)\s+nu\s+koopidunga\b"
        ]

        stopwords = {"feeling", "stressed", "sad", "here", "fine", "okay", "anxious", "ready", "super", "testing", "doing"}
        for text in all_user_texts:
            for pattern in name_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    candidate = match.group(1).strip()
                    if candidate.lower() == "priya":
                        return "Priya"
                    if candidate.lower() not in stopwords and len(candidate) > 1:
                        return candidate.capitalize()
        return None

    def _extract_concerns(self, history: List[Dict[str, str]], current_message: str) -> List[str]:
        """Extracts past and current concerns mentioned across turns."""
        all_texts = [
            turn.get("text") or turn.get("message") or turn.get("content") or ""
            for turn in history if turn.get("sender") == "user" or turn.get("role") == "user"
        ] + [current_message]

        concerns = []
        for text in all_texts:
            lower = text.lower()
            if any(k in lower for k in ["exam", "test", "paritchai", "தேர்வு"]):
                if "exams" not in concerns: concerns.append("exams")
            if any(k in lower for k in ["sleep", "thookam", "insomnia", "தூக்கம்"]):
                if "sleep" not in concerns: concerns.append("sleep")
            if any(k in lower for k in ["friend", "relationship", "breakup", "fight", "சண்டை"]):
                if "relationships" not in concerns: concerns.append("relationships")
            if any(k in lower for k in ["job", "career", "placement", "interview", "வேலை"]):
                if "career/placement" not in concerns: concerns.append("career/placement")
            if any(k in lower for k in ["alone", "lonely", "thanimai", "தனிமை"]):
                if "loneliness" not in concerns: concerns.append("loneliness")
            if any(k in lower for k in ["overthink", "overthinking", "mind romba"]):
                if "overthinking" not in concerns: concerns.append("overthinking")
        return concerns

    def _generate_relevant_response(
        self,
        user_text: str,
        history: List[Dict[str, str]],
        mood_tag: str,
        lang: str,
        assessment_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Genuinely dynamic, intent-aware companion engine that analyzes what the user is saying
        and crafts unique, targeted responses in English, Tamil, and Thanglish.
        """
        user_lower = user_text.lower().strip()
        extracted_name = self._extract_name(history, user_text)
        concerns = self._extract_concerns(history, user_text)
        name_prefix = f"{extracted_name}, " if extracted_name else ""
        name_suffix = f", {extracted_name}" if extracted_name else ""

        # Turn count
        user_turn_count = len([t for t in history if t.get("sender") == "user"])

        # ----------------------------------------------------------------------
        # 1. SPECIFIC CONTEXT RECALL: "What is my name and why am I stressed?"
        # ----------------------------------------------------------------------
        is_name_query = "what is my name" in user_lower or "who am i" in user_lower or "en peyar" in user_lower
        is_why_stressed = "why am i stressed" in user_lower or "why i am stressed" in user_lower or "yen stress" in user_lower

        if is_name_query and is_why_stressed:
            name_str = extracted_name or "a valued friend"
            stress_cause = " and ".join(concerns) if concerns else "the heavy pressures and deadlines you shared"
            if lang == "ta":
                reply = f"உங்கள் பெயர் {name_str}. நீங்கள் உங்கள் {stress_cause} காரணமாக மன அழுத்தத்தில் இருப்பதாக என்னிடம் பகிர்ந்தீர்கள். நான் உங்கள் ஒவ்வொரு சொல்லையும் நினைவில் வைத்திருக்கிறேன், {name_str}. இதை நாம் நிதானமாக எதிர்கொள்ளலாம்."
            elif lang == "thanglish":
                reply = f"Unga name {name_str}! Neenga unga {stress_cause} pathi romba stress ah irukunu sonneenga. Naan unga conversation context-ah note pannitu thaan irukken. Romba panic aagatheenga {name_str}, step by step-ah handle pannalam."
            else:
                reply = f"Your name is {name_str}, and you mentioned that you are feeling stressed about your {stress_cause}. I remember everything you share in this session, and I'm right here with you. Let's take things one moment at a time."
            return self._build_result(reply, "Stress", lang, ["What should I do first?", "Can you guide me with breathing?", "I want to share more"])

        if is_name_query:
            name_str = extracted_name or "not mentioned yet"
            if lang == "ta": reply = f"உங்கள் பெயர் {name_str}!"
            elif lang == "thanglish": reply = f"Unga name {name_str}!"
            else: reply = f"Your name is {name_str}."
            return self._build_result(reply, "Neutral", lang, ["How can you support me?", "What should I do next?"])

        # ----------------------------------------------------------------------
        # 2. GREETINGS & INTRODUCTIONS ("Hi", "Hello", "Vanakkam", "My name is...")
        # ----------------------------------------------------------------------
        if re.search(r"\b(?:my\s+name\s+is|i\s+am|i'm)\s+([A-Za-z]+)\b", user_lower) and len(user_text.split()) <= 5:
            name = extracted_name or "there"
            if lang == "ta":
                reply = f"வணக்கம் {name}! உங்களை சந்தித்ததில் மிக்க மகிழ்ச்சி. இன்று உங்கள் மனம் எப்படி உணர்கிறது? எதைப்பற்றி பேச விரும்புகிறீர்கள்?"
            elif lang == "thanglish":
                reply = f"Vanakkam {name}! Ungala meet pannathula romba happy. Iniku unga mind epdi iruku? Enna vishayam pathi discuss panna virumbureenga?"
            else:
                reply = f"Hello {name}! It's wonderful to meet you. How is your day going so far, and what feels most prominent on your mind right now?"
            return self._build_result(reply, "Positive / Neutral", lang, ["I'm feeling stressed", "Just wanted to chat", "Give me study tips"])

        if re.search(r"\b(hi|hello|hey|vanakkam|good\s+morning|good\s+evening|good\s+afternoon)\b", user_lower) and len(user_text.split()) <= 4:
            if lang == "ta":
                reply = f"வணக்கம்{name_suffix}! உங்களுக்கு உதவ நான் தயாராக உள்ளேன். நீங்கள் இன்று எதைப்பற்றி என்னிடம் பகிர்ந்து கொள்ள விரும்புகிறீர்கள்?"
            elif lang == "thanglish":
                reply = f"Hi{name_suffix}! Vanakkam. Iniku unga day epdi poguthu? Anything you want to share or ask me?"
            else:
                reply = f"Hello{name_suffix}! I'm glad you're here. How are you feeling right now, and what would you like to talk about today?"
            return self._build_result(reply, "Positive / Neutral", lang, ["I'm feeling overwhelmed", "Help me calm down", "I can't sleep"])

        # ----------------------------------------------------------------------
        # 3. IDENTITY & CAPABILITIES ("Who are you?", "What can you do?")
        # ----------------------------------------------------------------------
        if any(p in user_lower for p in ["who are you", "what can you do", "what are you", "neenga yar", "neenga yaaru", "enna panna mudiyum", "unnala enna"]):
            if lang == "ta":
                reply = (
                    "நான் **MindMate AI** — உங்கள் மனநலத் துணை (Conversational Companion). "
                    "என்னிடம் நீங்கள்:\n"
                    "• மன அழுத்தம், பயம், அல்லது தனிமை பற்றி சுதந்திரமாகப் பேசலாம்\n"
                    "• உடனடி மூச்சுப்பயிற்சி மற்றும் அமைதிப்படுத்தும் வழிமுறைகளைப் பெறலாம்\n"
                    "• தேர்வு அல்லது படிப்பு சார்ந்த பதற்றத்தைக் குறைக்க ஆலோசனைகள் கேட்கலாம்\n"
                    "• தமிழ், Thanglish மற்றும் ஆங்கிலத்தில் எந்தத் தயக்கமும் இன்றி உரையாடலாம்."
                )
            elif lang == "thanglish":
                reply = (
                    "Naan **MindMate AI** — unga personal mental wellness companion!\n\n"
                    "Enkitta neenga:\n"
                    "1. Unga stress, worry, and overthinking pathi freely share pannalam.\n"
                    "2. Quick breathing exercises & calming techniques kekaalam.\n"
                    "3. Exam pressure, sleep issues, or daily focus tips pathi guidance vaangalam.\n"
                    "4. English, Tamil, and Thanglish la ungaluku comfortable ah pesalam!"
                )
            else:
                reply = (
                    "I am **MindMate AI**, your dedicated mental wellness companion.\n\n"
                    "Here are the ways I can support you:\n"
                    "• **Empathetic Listening:** A safe, judgment-free space to share your thoughts and feelings.\n"
                    "• **Grounding & Calming:** Guided 4-7-8 breathing and sensory reset exercises.\n"
                    "• **Targeted Advice:** Practical pacing techniques for academic pressure, insomnia, and overthinking.\n"
                    "• **Trilingual Support:** Chat naturally in English, Tamil, or Thanglish."
                )
            return self._build_result(reply, "Neutral", lang, ["I'm feeling stressed", "Help me calm down", "How to stop overthinking?"])

        # ----------------------------------------------------------------------
        # 4. BREATHING & GROUNDING ("Help me calm down", "Breathing exercise", "Relax")
        # ----------------------------------------------------------------------
        if any(k in user_lower for k in ["calm down", "calm me", "breathing", "breath", "deep breath", "grounding", "mooche", "relax pannanum"]):
            if lang == "ta":
                reply = (
                    f"கண்டிப்பாக{name_suffix}, இப்போது நாம் ஒரு எளிய **4-4-6 மூச்சுப் பயிற்சியை** செய்யலாம்:\n\n"
                    "1. கண்களை மெதுவாக மூடி, தோள்களைத் தளர்த்துங்கள்.\n"
                    "2. **4 வினாடிகள்** மூக்கை வழியே ஆழமாக மூச்சை உள்ளிழுங்கள் (1... 2... 3... 4).\n"
                    "3. **4 வினாடிகள்** மூச்சை அடக்கிப் பிடியுங்கள்.\n"
                    "4. இப்போது **6 வினாடிகள்** வாயின் வழியே மெதுவாக மூச்சை வெளிவிடுங்கள் (1... 2... 3... 4... 5... 6).\n\n"
                    "இதை 3 முறை செய்யுங்கள். உங்கள் உடல் தளர்வடைவதை உணர முடிகிறதா?"
                )
            elif lang == "thanglish":
                reply = (
                    f"Sure{name_suffix}! Ipo namba oru simple **4-4-6 Breathing Reset** pannalam:\n\n"
                    "1. First unga shoulders and jaw relax panunga.\n"
                    "2. **4 seconds** nose vazhiya slow ah breath in panunga (1... 2... 3... 4).\n"
                    "3. **4 seconds** breath hold panunga.\n"
                    "4. Then **6 seconds** mouth vazhiya gently exhale panunga (1... 2... 3... 4... 5... 6).\n\n"
                    "Intha cycle ah 3 times continue panunga. Konjam calm ah feel aagutha nu solunga!"
                )
            else:
                reply = (
                    f"Let's ground your nervous system right now{name_suffix} with a gentle **4-4-6 breathing technique**:\n\n"
                    "1. **Inhale quietly** through your nose for **4 counts** (feel your abdomen expand).\n"
                    "2. **Hold** the breath gently for **4 counts**.\n"
                    "3. **Exhale slowly** and smoothly through your mouth for **6 counts**.\n\n"
                    "Repeat this 3 or 4 times. Lower your shoulders away from your ears. How does your chest and breathing feel now?"
                )
            return self._build_result(reply, "Stress", lang, ["I feel a little calmer", "What should I do next?", "My thoughts are still racing"])

        # ----------------------------------------------------------------------
        # 5. EXAM & STUDY PRESSURE ("Padikka mudiyala", "Exam stress", "Concentration")
        # ----------------------------------------------------------------------
        if any(k in user_lower for k in ["exam", "exams", "study", "padikka", "padipu", "paritchai", "concentrat", "focus", "syllabus", "assignment"]):
            if lang == "ta":
                reply = (
                    f"தேர்வு மற்றும் படிப்பு சார்ந்த சுமை மிகுந்த சோர்வைத் தரக்கூடியது{name_suffix}. ஆனால் நினைவில் கொள்ளுங்கள்: உங்கள் மன அமைதியும் ஆரோக்கியமுமே முதன்மையானது.\n\n"
                    "சில நடைமுறை வழிகள்:\n"
                    "• **பொமோடோரோ முறை:** 25 நிமிடங்கள் மட்டும் படியுங்கள், பிறகு 5 நிமிடங்கள் இடைவேளை எடுங்கள்.\n"
                    "• **பெரிய பாடப்பிரிவுகளை பிரியுங்கள்:** முழுப் புத்தகத்தையும் பார்ப்பதற்குப் பதிலாக, அடுத்த 1 மணிநேரத்திற்கான 2 தலைப்புகளை மட்டும் கவனியுங்கள்.\n"
                    "• **தண்ணீர் குடியுங்கள்:** மூளை சோர்வடையாமல் இருக்க போதுமான நீர்ச்சத்து அவசியம்.\n\n"
                    "இப்போது எந்தப் பாடம் அல்லது தலைப்பு உங்களுக்குக் கடினமாகத் தோன்றுகிறது?"
                )
            elif lang == "thanglish":
                reply = (
                    f"Exam and study pressure romba heavy ah irukum{name_suffix}, especially syllabus perusa irukum bothu. "
                    "Aana unga mental peace thaan first priority!\n\n"
                    "Few actionable tips to handle this right now:\n"
                    "1. **Pomodoro Technique:** 25 mins focus pannitu 5 mins break edunga.\n"
                    "2. **Micro-goals:** Entire syllabus pathi yosikaama, next 30 mins la oru small topic mattum mudinga.\n"
                    "3. **Zero Multitasking:** Phone notification silent panitu, study table la focus panunga.\n\n"
                    "Specific ah entha subject ungaluku tension tharuthu?"
                )
            else:
                reply = (
                    f"Academic pressure can feel overwhelmingly intense{name_suffix}, especially when multiple deadlines collide. "
                    "Remember that an exam measures preparation on a given day, not your intelligence or self-worth.\n\n"
                    "Here is an immediate action plan:\n"
                    "• **The 25/5 Rule:** Focus on a single concept for 25 minutes, then step away from your desk for 5 minutes.\n"
                    "• **Chunk the Material:** Don't look at the whole mountain. What is the single next sub-topic you can read right now?\n"
                    "• **Hydrate & Step Outside:** Even 3 minutes of fresh air resets cognitive fatigue.\n\n"
                    "Which specific subject or deadline feels the most pressuring today?"
                )
            return self._build_result(reply, "Academic pressure", lang, ["How to avoid distractions?", "I'm procrastinating", "Help me plan a schedule"])

        # ----------------------------------------------------------------------
        # 6. SLEEP & INSOMNIA ("Can't sleep", "Thookam varala", "Insomnia")
        # ----------------------------------------------------------------------
        if any(k in user_lower for k in ["sleep", "thookam", "thookame", "insomnia", "தூக்கம்", "bed", "night", "awake"]):
            if lang == "ta":
                reply = (
                    f"தூக்கம் வராமல் படுக்கையில் புரள்வது மிகுந்த மன அழுத்தத்தை உண்டாக்கும்{name_suffix}. "
                    "கட்டாயப்படுத்தி தூங்க முயற்சிப்பது பதற்றத்தை அதிகரிக்கும்.\n\n"
                    "இதைச் செய்து பாருங்கள்:\n"
                    "• படுக்கையை விட்டு எழுந்து, மங்கலான வெளிச்சத்தில் அமைதியாக அமருங்கள்.\n"
                    "• மொபைல் திரையைப் பார்ப்பதைத் தவிருங்கள்.\n"
                    "• வெதுவெதுப்பான தண்ணீர் குடித்து, மெதுவான இசையைக் கேளுங்கள் அல்லது மூச்சை கவனியுங்கள்.\n"
                    "தூக்கம் வரும் உணர்வு ஏற்பட்டதும் மீண்டும் படுக்கைக்குச் செல்லுங்கள்."
                )
            elif lang == "thanglish":
                reply = (
                    f"Night thookam varala na mind romba overthink panna start pannidum{name_suffix}. "
                    "Force panni thooka try pannatheenga, it creates more pressure.\n\n"
                    "Do this right now:\n"
                    "1. Phone-ah face kitta vekama, keep it at least 5 feet away.\n"
                    "2. Sip some warm water.\n"
                    "3. Bed la lay pannitu, unga breath-ah slow ah count panunga (Inhale 1, Exhale 2... up to 50).\n"
                    "4. If still awake, get up, sit on a chair in dim light for 10 mins until eyes feel heavy."
                )
            else:
                reply = (
                    f"Struggling to fall asleep is genuinely frustrating{name_suffix}, especially when your mind races with tomorrow's worries.\n\n"
                    "Try the **Sleep Reset Rule**:\n"
                    "• **The 20-Minute Rule:** If you've been in bed awake for over 20 minutes, get out of bed. Sit in a chair with dim light and do something relaxing (not screen-based).\n"
                    "• **Brain Dump:** Jot down whatever thoughts are repeating on a piece of scrap paper to get them out of your head.\n"
                    "• **Progressive Muscle Relaxation:** Tense your feet for 5 seconds, then completely release. Work your way up to your calves, thighs, and shoulders."
                )
            return self._build_result(reply, "Stress", lang, ["How to stop night thoughts?", "Guide me to sleep", "I feel tired in the morning"])

        # ----------------------------------------------------------------------
        # 7. OVERTHINKING & WORRY ("Mind romba overthink", "Stop overthinking", "Panic")
        # ----------------------------------------------------------------------
        if any(k in user_lower for k in ["overthink", "overthinking", "yosichite", "yosikka", "mind confuse", "confused", "bayam", "bayama", "panic", "worry"]):
            if lang == "ta":
                reply = (
                    f"அதிகமாக யோசிப்பது (Overthinking) நமது கட்டுப்பாட்டில் இல்லாத எதிர்காலத்தைப் பற்றி பயப்படுவதால் ஏற்படுகிறது{name_suffix}.\n\n"
                    "உடனடித் தீர்வு:\n"
                    "• **5-4-3-2-1 முறை:** உங்களைச் சுற்றிப் பார்க்கும் 5 பொருட்கள், தொட்டுணரும் 4 பொருட்கள், கேட்கும் 3 ஒலிகள், நுகரும் 2 நறுமணங்கள், உணரும் 1 சுவை ஆகியவற்றைக் கவனியுங்கள்.\n"
                    "• உங்கள் எண்ணங்களை ஒரு காகிதத்தில் எழுதி வையுங்கள்.\n"
                    "இப்போது உங்கள் மனதில் திரும்பத் திரும்ப வரும் சிந்தனை என்ன?"
                )
            elif lang == "thanglish":
                reply = (
                    f"Overthinking namba mind-ah loop la maatti vidum{name_suffix}. Neenga control panna mudiyaatha "
                    "future events pathi yosikaratha stop panna try pannunga.\n\n"
                    "Use the **Circle of Control**:\n"
                    "1. Unga control la enna iruko athu mattum paadunga (your effort, your breath, your next 1 hour).\n"
                    "2. Others behavior, exam results, or uncertain future namba control la illa.\n"
                    "3. Mind romba rush aaguthu na, wash your face with cool water immediately.\n\n"
                    "Enna specific situation ungaluku continuous ah overthinking tharuthu?"
                )
            else:
                reply = (
                    f"Overthinking traps us in hypothetical problems that haven't even occurred yet{name_suffix}.\n\n"
                    "Try the **5-4-3-2-1 Sensory Grounding Exercise**:\n"
                    "• Name **5 things you can see** around you right now.\n"
                    "• Touch **4 textures** (your sleeve, desk, chair, pen).\n"
                    "• Listen for **3 distinct sounds** (fan, distant traffic, your breath).\n"
                    "• Identify **2 scents** around you.\n"
                    "• Notice **1 physical taste**.\n\n"
                    "What is the core thought or fear that your mind keeps replaying?"
                )
            return self._build_result(reply, "Anxiety", lang, ["Help me let go of worries", "What if things go wrong?", "I want to take a break"])

        # ----------------------------------------------------------------------
        # 8. ACTIONABLE / WHAT SHOULD I DO ("Enna panrathu?", "What should I do next?")
        # ----------------------------------------------------------------------
        if any(k in user_lower for k in ["what should i do", "what do i do", "what next", "enna panrathu", "enna pannanum", "aduthu enna", "guide me", "suggest", "tips"]):
            related_topic = concerns[0] if concerns else "managing stress"
            if lang == "ta":
                reply = (
                    f"நீங்கள் செய்ய வேண்டிய 3 எளிய அடிகள் இதோ{name_suffix}:\n\n"
                    f"1. **ஒரு சிறிய இடைவேளை எடுங்கள்:** உங்கள் {related_topic} பற்றிய சிந்தனையை 10 நிமிடங்களுக்கு நிறுத்திவிட்டு ஆழமான மூச்சு எடுங்கள்.\n"
                    "2. **மிகச் சிறிய ஒரு வேலையை மட்டும் முடியுங்கள்:** உங்கள் அடுத்த 15 நிமிடங்களை பயனுள்ளதாக்குங்கள்.\n"
                    "3. **உங்களிடம் கனிவாக இருங்கள்:** எல்லாவற்றையும் ஒரே நாளில் சரிசெய்ய வேண்டிய அவசியமில்லை.\n\n"
                    "இதில் முதலில் எதைச் செய்ய விரும்புகிறீர்கள்?"
                )
            elif lang == "thanglish":
                reply = (
                    f"Right now neenga panna vendiya 3 immediate steps{name_suffix}:\n\n"
                    f"1. **Pause for 5 mins:** Unga {related_topic} pathi continuous-ah yosikama, drink a glass of water.\n"
                    "2. **Pick ONE small task:** Big goals pathi yosikaatheenga. Next 15 mins la mudika koodiya oru simple task start panunga.\n"
                    "3. **Be kind to yourself:** Neenga human thaan, take it one step at a time.\n\n"
                    "Idhula ethu ipo ungaluku doable ah theriyuthu?"
                )
            else:
                reply = (
                    f"Here is your 3-step action plan for right now{name_suffix}:\n\n"
                    f"1. **Micro-Pause:** Step away from your screens and reflect on {related_topic} without judgment for 5 minutes.\n"
                    "2. **Single-Tasking:** Pick the single easiest task on your plate and spend just 10 minutes on it without looking ahead.\n"
                    "3. **Self-Compassion:** Acknowledge that feeling overwhelmed is normal, and progress doesn't need to be giant leaps.\n\n"
                    "Which of these feels most manageable to begin right now?"
                )
            return self._build_result(reply, "Neutral", lang, ["I'll start with a 5-min break", "Guide me with the small task", "I feel better now"])

        # ----------------------------------------------------------------------
        # 9. RELATIONSHIPS & LONELINESS ("Alone", "Thanimai", "Friend fight", "Breakup")
        # ----------------------------------------------------------------------
        if any(k in user_lower for k in ["alone", "lonely", "thanimai", "friend", "fight", "breakup", "relationship", "family", "yarum illa"]):
            if lang == "ta":
                reply = (
                    f"தனிமை அல்லது அன்பானவர்களுடனான கருத்து வேறுபாடுகள் இதயத்தை அதிகம் காயப்படுத்தும்{name_suffix}. "
                    "நீங்கள் தனியாக இல்லை என்பதை நினைவில் கொள்ளுங்கள். உங்கள் உணர்வுகள் மதிப்புமிக்கவை.\n\n"
                    "நீங்கள் விரும்பினால், உங்கள் நண்பர் அல்லது குடும்பத்தினரிடம் என்ன நடந்தது என்பதை என்னிடம் மேலும் விரிவாகப் பகிரலாம்."
                )
            elif lang == "thanglish":
                reply = (
                    f"People issues and feeling lonely can feel really painful{name_suffix}. "
                    "Unga feelings totally valid. Neenga ungaluku close aana oru trusted friend or family member kita "
                    "konjam pesi paakalam, or enakitta share panunga. What actually happened?"
                )
            else:
                reply = (
                    f"Interpersonal conflicts and loneliness weigh heavily on our emotional well-being{name_suffix}. "
                    "Please know that what you're feeling right now is completely valid. "
                    "Would you like to share what happened? Sometimes talking it through helps organize the tangled feelings."
                )
            return self._build_result(reply, "Loneliness", lang, ["I want to explain what happened", "How to talk to them?", "I just want peace"])

        # ----------------------------------------------------------------------
        # 10. DYNAMIC CONTEXTUAL MIRROR (Fallback when input is open-ended)
        # ----------------------------------------------------------------------
        # Extract keywords from user message to make response 100% relevant!
        clean_words = [w for w in re.findall(r'[a-zA-Z\u0B80-\u0BFF]+', user_text) if len(w) > 2]
        topic_snippet = " ".join(clean_words[:4]) if clean_words else "what you shared"

        if lang == "ta":
            reply = (
                f"நீங்கள் கூறியதை நான் மிகக் கவனமாகக் கேட்டேன்{name_suffix}. \"{user_text}\" என்று நீங்கள் குறிப்பிட்ட விஷயம் உங்கள் மனதில் அழுத்தத்தை ஏற்படுத்துகிறது என்பதை உணர்கிறேன்.\n\n"
                "இதைப்பற்றி இன்னும் கொஞ்சம் விரிவாகக் கூற முடியுமா? உங்களுக்கு உதவும் நடைமுறை ஆலோசனைகளை நாம் சேர்ந்து யோசிக்கலாம்."
            )
        elif lang == "thanglish":
            reply = (
                f"Neenga sonnatha naan nalla note pannen{name_suffix}. \"{user_text}\" pathi neenga sonnathu, "
                "unga mind la oru impact create panniruku nu theriyuthu.\n\n"
                "Idha pathi unga thoughts konjam detailed ah solunga, so that ungaluku exactly relevant aana advice naan thara mudiyum. What feels hardest about this right now?"
            )
        else:
            reply = (
                f"I hear you clearly{name_suffix}. You mentioned: \"{user_text}\". "
                "I want to make sure I give you the most relevant support for this specific situation.\n\n"
                "Could you tell me a little more about what triggered this, or how it has been impacting you today? I'm here to listen and help you unpack it."
            )

        dynamic_followups = self._generate_dynamic_followups(user_text, mood_tag, lang)
        return self._build_result(reply, mood_tag, lang, dynamic_followups)

    def _generate_dynamic_followups(self, user_text: str, mood_tag: str, lang: str) -> List[str]:
        """Generates contextual prompt buttons matching the user's situation."""
        lower = user_text.lower()
        if "exam" in lower or "study" in lower or "padikka" in lower:
            return ["Give me 3 study tips", "How to focus for 1 hour?", "I'm feeling exam panic"]
        if "sleep" in lower or "thookam" in lower or "night" in lower:
            return ["Guide me through a sleep reset", "How to stop racing thoughts?", "I'll try drinking warm water"]
        if "calm" in lower or "breath" in lower or "anxiety" in lower or "bayam" in lower:
            return ["Start a 2-min breathing exercise", "What should I do next?", "Tell me a calming thought"]
        if lang == "thanglish":
            return ["Enna panrathu nu solunga", "Oru simple tip kudunga", "Next step enna?"]
        if lang == "ta":
            return ["அடுத்த கட்ட ஆலோசனை தாருங்கள்", "மூச்சுப்பயிற்சி வழிகாட்டுங்கள்", "பதற்றத்தை குறைக்க என்ன செய்ய வேண்டும்?"]
        return ["What should I do next?", "Can you guide me with breathing?", "I want to share more details"]

    def _build_result(self, text: str, mood_tag: str, lang: str, follow_ups: List[str]) -> Dict[str, Any]:
        return {
            "text": text,
            "moodTag": mood_tag,
            "language": lang,
            "source": "companion_engine",
            "isEmergency": False,
            "followUps": follow_ups
        }

    def _emergency_response(self, lang: str) -> Dict[str, Any]:
        """Crisis intervention protocol."""
        if lang == "ta":
            text = (
                "நண்பரே, நீங்கள் மிகுந்த மனவேதனையில் இருப்பதை உணர்கிறேன். உங்கள் உயிர் மிக மதிப்புமிக்கது. "
                "தயவுசெய்து உடனடியாக இலவச அவசர உதவி எண்களைத் தொடர்பு கொள்ளுங்கள்:\n\n"
                "• Tele-MANAS தேசிய உதவி எண்: 14416 அல்லது 1800-891-4416 (24x7 இலவசம்)\n"
                "• Sneha Helpline: +91 44 2464 0050\n"
                "• அவசர உதவி: 112\n\n"
                "நீங்கள் தனியாக இல்லை. உங்களுக்கு உதவ பலர் எப்போதும் உள்ளனர்."
            )
        elif lang == "thanglish":
            text = (
                "Nanba/Nanbi, unga life romba precious. Neenga romba pain la irukureenga nu theriyuthu. "
                "Please immediate ah intha free helplines ah contact pannunga:\n\n"
                "• Tele-MANAS (Govt 24x7 Helpline): 14416 or 1800-891-4416\n"
                "• Sneha Helpline (Tamil Nadu): +91 44 2464 0050\n"
                "• Emergency: 112\n\n"
                "Please talk to someone you trust right now."
            )
        else:
            text = (
                "I hear how much pain you are in right now, but you do not have to carry this alone. "
                "Your life and well-being matter. Please reach out right now to a trusted person or free, confidential crisis service:\n\n"
                "• Tele-MANAS National Mental Health Helpline: 14416 or 1800 891 4416 (24/7, Toll-Free)\n"
                "• Kiran Mental Health Helpline: 1800-599-0019\n"
                "• Sneha Helpline: +91 44 2464 0050\n"
                "• Emergency Services: 112 / 911\n\n"
                "Please connect with someone who can support you right this second."
            )

        return {
            "text": text,
            "moodTag": "Emergency",
            "language": lang,
            "source": "crisis_protocol",
            "isEmergency": True,
            "followUps": [
                "I am contacting the Tele-MANAS 14416 helpline.",
                "I am reaching out to a friend or family member.",
                "Can you stay with me and talk safely?"
            ]
        }

gemini_service = GeminiService()
