import re

def detect_language(text: str) -> str:
    kazakh_chars = re.findall(r"[әіңғүұқөһ]", text.lower())
    russian_chars = re.findall(r"[а-яё]", text.lower())
    english_chars = re.findall(r"[a-z]", text.lower())

    if (kazakh_chars and russian_chars) or (kazakh_chars and english_chars) or (russian_chars and english_chars):
        return "Mixed"
    elif kazakh_chars:
        return "Kazakh"
    elif russian_chars:
        return "Russian"
    elif english_chars:
        return "English"
    else:
        return "Unknown"
