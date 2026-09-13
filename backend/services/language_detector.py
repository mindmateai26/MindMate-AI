import re

# Tamil Unicode Block: \u0B80 - \u0BFF
TAMIL_UNICODE_PATTERN = re.compile(r'[\u0B80-\u0BFF]')

# Common Thanglish vocabulary and phonetics
THANGLISH_KEYWORDS = {
    "enaku", "enakku", "enakku", "unaku", "unakku",
    "romba", "rombaaa", "rompa",
    "iruku", "irukku", "irukken", "iruken", "irunthathu",
    "kavala", "kavalai", "kavalaiya", "kavalaiyaa",
    "kashtam", "kashtama", "kastam", "kastama",
    "bayama", "bayam", "payama", "payam",
    "theriyala", "puriyala", "mudiyala", "mudiyathu",
    "manasu", "manasula", "valikuthu", "valikudhu",
    "solla", "solrathu", "solunga", "sollunga",
    "vanakkam", "nanba", "nanbi", "thambi", "thangachi",
    "anna", "akka", "amma", "appa",
    "epdi", "yeppadi", "eppadi", "yen", "enna",
    "aachu", "aachu", "aayiduchu", "illai", "illa",
    "padikka", "padipu", "paritchai", "velai", "neram",
    "thookam", "thookame", "vara", "varala",
    "sari", "seri", "kooda", "mattum", "panna", "pannunga"
}

def detect_language(text: str, user_override: str = "auto") -> str:
    """
    Detects language among 'en' (English), 'ta' (Tamil Script), 'thanglish' (Tamil in Latin script).
    Allows user override if not 'auto'.
    """
    if user_override and user_override.lower() not in ["auto", ""]:
        override = user_override.lower()
        if override in ["ta", "tamil"]:
            return "ta"
        if override in ["thanglish", "tanglish"]:
            return "thanglish"
        if override in ["en", "english"]:
            return "en"

    if not text or not text.strip():
        return "en"

    # Check for Tamil native script characters
    if TAMIL_UNICODE_PATTERN.search(text):
        return "ta"

    # Check for Thanglish words
    words = re.findall(r'[a-zA-Z]+', text.lower())
    thanglish_match_count = sum(1 for w in words if w in THANGLISH_KEYWORDS)

    # If significant Thanglish words detected
    if thanglish_match_count >= 1:
        return "thanglish"

    return "en"
