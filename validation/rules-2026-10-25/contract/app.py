def normalize_title(title):
    title=title.strip()
    if not title or len(title)>40:
        raise ValueError("invalid title")
    return title
