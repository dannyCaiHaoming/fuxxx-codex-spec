"""Small persistent task list backed by a caller-selected UTF-8 JSON file."""

import json
from pathlib import Path


def add_task(path, title):
    title = title.strip()
    if not title:
        raise ValueError("Task title must not be blank")
    tasks = list_tasks(path)
    task = {"id": max((item["id"] for item in tasks), default=0) + 1,
            "title": title}
    tasks.append(task)
    Path(path).write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return task


def list_tasks(path):
    try:
        contents = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    return json.loads(contents)
