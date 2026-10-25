"""调用者指定文件的本地任务清单。"""
import json
from pathlib import Path
from uuid import uuid4


def add_task(path, title):
    title = title.strip()
    if not title:
        raise ValueError("title must not be blank")
    tasks = list_tasks(path)
    existing_ids = {task["id"] for task in tasks}
    task_id = uuid4().hex
    while task_id in existing_ids:
        task_id = uuid4().hex
    task = {"id": task_id, "title": title}
    tasks.append(task)
    Path(path).write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return task


def list_tasks(path):
    try:
        content = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    return json.loads(content)
