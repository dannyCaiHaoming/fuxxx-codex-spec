def parse_tags(text: str) -> list[str]:
    return [tag.strip() for tag in text.split(",") if tag.strip()]
