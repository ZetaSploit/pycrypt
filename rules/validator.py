REQUIRED_FIELDS = {
    "id",
    "title",
    "severity",
    "message",
    "language",
    "query",
}

VALID_SEVERITIES = {
    "low",
    "medium",
    "high",
    "critical",
}

VALID_LANGUAGES = {
    "python",
    "javascript",
    "java",
    "c",
    "c++",
}

def validate_rule(rule: dict) -> None:
    missing = REQUIRED_FIELDS - rule.keys()

    if missing:
        raise ValueError(
            f"Missing required fields: {', '.join(sorted(missing))}"
        )

    if rule["severity"] not in VALID_SEVERITIES:
        raise ValueError(
            f"Invalid severity: {rule['severity']}"
        )

    if rule["language"] not in VALID_LANGUAGES:
        raise ValueError(
            f"Unsupported language: {rule['language']}"
        )

    if not rule["query"].strip():
        raise ValueError("Query cannot be empty")
