import re


PII_PATTERNS = (
    r"\b\d{4}(?:[ -]?\d{4}){2,3}\b",
    r"\b\d{10,}\b",
    r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
    r"\b\d{10}\b",
    r"\b[A-Z]{5}\d{4}[A-Z]\b",
)


def mask_pii(text):
    masked = str(text)
    for pattern in PII_PATTERNS:
        masked = re.sub(pattern, "[REDACTED]", masked)
    return masked