def normalize_title(title):
    normalized = title.strip()
    if not normalized:
        raise ValueError("title must not be empty")
    return normalized
