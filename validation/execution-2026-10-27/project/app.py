def parse_tags(text: str) -> list[str]:
    tags = (part.strip() for part in text.split(","))
    return [tag for tag in tags if tag]
