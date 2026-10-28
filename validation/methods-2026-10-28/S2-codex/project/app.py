def parse_tags(text: str) -> list[str]:
    tags = (item.strip() for item in text.split(","))
    return [tag for tag in tags if tag]
