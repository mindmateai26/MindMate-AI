import re
from typing import Tuple, Dict, Any

# Emergency & Crisis signals (self-harm, suicide, immediate danger)
EMERGENCY_PATTERNS = [
    r"\bsuicid(e|al)\b",
    r"\bkill\s+myself\b",
    r"\bend\s+my\s+life\b",
    r"\bhurt\s+myself\b",
    r"\bwant\s+to\s+die\b",
    r"\bdying\b",
    r"\bbetter\s+off\s+dead\b",
    r"\bno\s+reason\s+to\s+live\b",
    r"\bcan'?t\s+take\s+this\s+anymore\b",
    r"\bcan'?t\s+go\s+on\b",
    r"தற்கொலை",
    r"செத்து\s*போக",
    r"உயிர்\s*விட",
    r"\bsaaga\s+poren\b",
    r"\bsethuruven\b",
    r"\buyira\s+vidanum\b",
    r"\btharkolai\b"
]

# Emotion Lexicons for English, Tamil, and Thanglish
EMOTION_PATTERNS = {
    "Academic pressure": [
        r"\bexam(s)?\b", r"\btest(s)?\b", r"\bstudy(ing)?\b", r"\bcollege\b",
        r"\buniversity\b", r"\bmarks\b", r"\bgrades\b", r"\bassignment(s)?\b",
        r"\bsemester\b", r"\bdeadline(s)?\b", r"\bplacement(s)?\b", r"\bgpa\b",
        r"தேர்வு", r"படிப்பு", r"பரீட்சை", r"மதிப்பெண்",
        r"\bparitchai\b", r"\bpadikka\b", r"\bpadipu\b", r"\bpadikkanum\b"
    ],
    "Stress": [
        r"\bstress(ed|ful)?\b", r"\bpressure\b", r"\bburden(ed)?\b", r"\bexhaust(ed|ing)?\b",
        r"\bburnout\b", r"\boverwhelm(ed)?\b", r"\btension\b", r"\bheavy\s+head\b",
        r"அழுத்தம்", r"மன\s*அழுத்தம்", r"டென்ஷன்",
        r"\bkashtam(a)?\b", r"\bkastam(a)?\b", r"\btension\s*(ah|aa|aga)?\b",
        r"\bstress\s*(ah|aa|aga)?\b", r"\bpressure\s*(ah|aa)?\b"
    ],
    "Anxiety": [
        r"\banxi(ous|ety)\b", r"\bpanic\b", r"\bnervous\b", r"\bworr(y|ied|ying)\b",
        r"\bfear(ful)?\b", r"\bpalpitat(ion|ing)\b", r"\bscared\b", r"\bshaking\b",
        r"பயம்", r"பதட்டம்", r"கவலை",
        r"\bbayam(a)?\b", r"\bpayam(a)?\b", r"\bpathatam(a)?\b", r"\bpadhabadha\b"
    ],
    "Sadness": [
        r"\bsad(ness)?\b", r"\bcry(ing)?\b", r"\bweep(ing)?\b", r"\bdepress(ed|ion)?\b",
        r"\bhopeless(ness)?\b", r"\bgrief\b", r"\bunhappy\b", r"\bheartbroken\b",
        r"\bmiserable\b", r"\bdown\b", r"\blow\b",
        r"சோகம்", r"வருத்தம்", r"அழுகை", r"கண்ணீர்",
        r"\bsogam(a)?\b", r"\bvarutham(a)?\b", r"\bazhugai\b", r"\bmanasu\s*valikuthu\b",
        r"\bkavala(i|ya)?\b"
    ],
    "Loneliness": [
        r"\blonel(y|iness)\b", r"\balone\b", r"\bisolat(ed|ion)\b", r"\bno\s+friends\b",
        r"\bleft\s+out\b", r"\bunloved\b", r"\bignored\b",
        r"தனிமை", r"யாரும்\s*இல்லை",
        r"\bthanimai(ya)?\b", r"\byarum\s*illa(i)?\b", r"\balone\s*(ah|aa)?\b"
    ],
    "Anger": [
        r"\bang(ry|er)\b", r"\bfurious\b", r"\birritat(ed|ing)\b", r"\bmad\b",
        r"\bhate\b", r"\bfrustrat(ed|ing)?\b", r"\baggressi(ve|on)\b",
        r"கோபம்", r"எரிச்சல்",
        r"\bkovam(a)?\b", r"\bkopam(a)?\b", r"\berichal(a)?\b"
    ],
    "Positive / Neutral": [
        r"\bhappy\b", r"\bgood\b", r"\bgreat\b", r"\bfine\b", r"\bbetter\b",
        r"\bcalm\b", r"\bpeace(ful)?\b", r"\brelax(ed)?\b", r"\bcontent\b",
        r"\bthank(s| you)?\b", r"\bok\b", r"\bokay\b",
        r"மகிழ்ச்சி", r"நலம்", r"நன்றி", r"அமைதி",
        r"\bsanthosham(a)?\b", r"\bnalla\b", r"\bnallaa\b", r"\bnandri\b"
    ]
}

def detect_emotion(text: str) -> Dict[str, Any]:
    """
    Detects primary emotion and checks emergency risk flag.
    Returns:
      {
        "emotion": str,
        "moodTag": str,
        "isEmergency": bool
      }
    """
    if not text:
        return {
            "emotion": "Neutral",
            "moodTag": "Neutral",
            "isEmergency": False
        }

    clean_text = text.lower().strip()

    # 1. Emergency self-harm check
    for pattern in EMERGENCY_PATTERNS:
        if re.search(pattern, clean_text, re.IGNORECASE):
            return {
                "emotion": "Crisis / Urgent",
                "moodTag": "Emergency",
                "isEmergency": True
            }

    # 2. Match emotion lexicons
    scores: Dict[str, int] = {}
    for emotion, patterns in EMOTION_PATTERNS.items():
        count = 0
        for pat in patterns:
            matches = len(re.findall(pat, clean_text, re.IGNORECASE))
            count += matches
        if count > 0:
            scores[emotion] = count

    if not scores:
        return {
            "emotion": "Neutral",
            "moodTag": "Neutral",
            "isEmergency": False
        }

    # If academic pressure co-occurs with stress or anxiety, highlight the root context
    if "Academic pressure" in scores and ("Stress" in scores or "Anxiety" in scores):
        primary_emotion = "Academic pressure"
    else:
        primary_emotion = max(scores.items(), key=lambda x: x[1])[0]

    return {
        "emotion": primary_emotion,
        "moodTag": primary_emotion,
        "isEmergency": False
    }
