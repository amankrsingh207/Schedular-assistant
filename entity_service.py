import spacy
import re
import unicodedata
from difflib import get_close_matches

# List of supported departments
DEPARTMENTS = ["dentist", "doctor", "cardiologist", "eye", "orthopedic"]

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# ---------------------------
# Helper: clean a word
# ---------------------------
def clean_word(word):
    # Remove punctuation and invisible characters
    word = ''.join(c for c in word if c.isalnum())
    word = unicodedata.normalize('NFKC', word)
    return word.lower()

# ---------------------------
# Main entity extraction
# ---------------------------
def extract_entities(text):
    # Clean the text: remove extra whitespace
    text_clean = re.sub(r'\s+', ' ', text).strip()
    
    # Split into words and clean each
    words = [clean_word(w) for w in text_clean.split() if clean_word(w)]

    # 1️⃣ Exact match department detection
    department = None
    for w in words:
        if w in DEPARTMENTS:
            department = w
            break

    # 2️⃣ Fuzzy match for OCR typos
    if not department:
        for w in words:
            matches = get_close_matches(w, DEPARTMENTS, n=1, cutoff=0.5)
            if matches:
                department = matches[0]
                break

    # 3️⃣ Extract date and time using spacy
    doc = nlp(text_clean.lower())
    date_phrase = None
    time_phrase = None
    for ent in doc.ents:
        if ent.label_ == "DATE" and not date_phrase:
            date_phrase = ent.text
        elif ent.label_ == "TIME" and not time_phrase:
            time_phrase = ent.text

    # 4️⃣ Regex fallback for time
    if not time_phrase:
        time_match = re.search(r'\b(\d{1,2}(:\d{2})?\s?(am|pm)?)\b', text_clean, re.IGNORECASE)
        if time_match:
            time_phrase = time_match.group(0).upper()

    # 5️⃣ Guardrails
    if not department:
        return {"status": "needs_clarification", "message": "Ambiguous department"}
    if not date_phrase:
        return {"status": "needs_clarification", "message": "Ambiguous date"}
    if not time_phrase:
        time_phrase = "09:00 AM"

    return {
        "entities": {
            "department": department,
            "date_phrase": date_phrase,
            "time_phrase": time_phrase
        },
        "entities_confidence": 0.85
    }
