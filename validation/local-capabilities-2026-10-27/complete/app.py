def normalize_title(title: str) -> str:
    title = title.strip()
    if not title:
        raise ValueError("empty title")
    return title
