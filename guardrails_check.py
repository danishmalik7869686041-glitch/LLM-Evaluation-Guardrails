"python"
import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"reveal\s+(the\s+)?system prompt",
    r"show\s+(me\s+)?your\s+hidden instructions",
    r"bypass\s+(the\s+)?safety rules",
]

UNSAFE_PATTERNS = [
    r"\bsteal\s+(passwords|credentials)\b",
    r"\bmake\s+(a\s+)?bomb\b",
    r"\bbuild\s+(a\s+)?weapon\b",
    r"\bdeploy\s+ransomware\b",
]


def check_input(text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        return {
            "status": "REVIEW REQUIRED",
            "injection_detected": False,
            "unsafe_input_detected": False,
            "reasons": ["Input is empty or invalid."],
        }

    injection = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in INJECTION_PATTERNS
    )
    unsafe = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in UNSAFE_PATTERNS
    )

    reasons = []
    if injection:
        reasons.append("Possible prompt injection detected.")
    if unsafe:
        reasons.append("Potentially unsafe request detected.")

    return {
        "status": "REVIEW REQUIRED" if reasons else "PASS",
        "injection_detected": injection,
        "unsafe_input_detected": unsafe,
        "reasons": reasons or ["No configured patterns matched."],
    }
