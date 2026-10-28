def parse_tags(text):
    return [t.strip() for t in text.split(",") if t.strip()]
