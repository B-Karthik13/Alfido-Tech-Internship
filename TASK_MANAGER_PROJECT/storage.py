"""
storage.py
----------
Tiny JSON-file "database" layer for the Task Manager.

All tasks live as a list of dicts inside data/tasks.json, e.g.:

[
  {
    "id": 1,
    "title": "Write report",
    "description": "Internship summary",
    "priority": "High",
    "status": "Pending",
    "due_date": "2026-07-01",
    "created_at": "2026-06-29T18:30:00"
  },
  ...
]

This module is the ONLY place that touches the JSON file directly.
app.py calls these functions instead of reading/writing JSON itself,
which keeps the route logic clean and makes it easy to swap storage
later (e.g. for a real database) without touching app.py much.
"""

import json
import os
from datetime import datetime
from threading import Lock

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")

# A simple lock to avoid two requests corrupting the file if they write
# at the exact same moment (Flask's dev server can be threaded).
_file_lock = Lock()


def _ensure_data_file():
    """Create the data folder/file with an empty list if they don't exist yet."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _read_all():
    """Read and return the full list of task dicts from tasks.json."""
    _ensure_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # File exists but is empty/corrupted -> treat as empty list
            return []


def _write_all(tasks):
    """Overwrite tasks.json with the given list of task dicts."""
    _ensure_data_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def _next_id(tasks):
    """Generate the next numeric id (max existing id + 1, or 1 if empty)."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# --------------------------------------------------------------------------
# Public CRUD API used by app.py
# --------------------------------------------------------------------------

def get_all_tasks(status_filter=None):
    """Return all tasks, newest first. Optionally filter by status."""
    with _file_lock:
        tasks = _read_all()

    if status_filter and status_filter != "All":
        tasks = [t for t in tasks if t.get("status") == status_filter]

    # Newest first (by created_at)
    tasks.sort(key=lambda t: t.get("created_at", ""), reverse=True)
    return tasks


def get_task(task_id):
    """Return a single task dict by id, or None if not found."""
    with _file_lock:
        tasks = _read_all()
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def add_task(title, description, priority, due_date):
    """Create a new task and persist it. Returns the new task dict."""
    with _file_lock:
        tasks = _read_all()
        new_task = {
            "id": _next_id(tasks),
            "title": title,
            "description": description,
            "priority": priority,
            "status": "Pending",
            "due_date": due_date or None,
            "created_at": datetime.utcnow().isoformat(timespec="seconds"),
        }
        tasks.append(new_task)
        _write_all(tasks)
    return new_task


def update_task(task_id, title, description, priority, status, due_date):
    """Update an existing task in place. Returns the updated dict, or None if not found."""
    with _file_lock:
        tasks = _read_all()
        updated = None
        for task in tasks:
            if task["id"] == task_id:
                task["title"] = title
                task["description"] = description
                task["priority"] = priority
                task["status"] = status
                task["due_date"] = due_date or None
                updated = task
                break
        if updated:
            _write_all(tasks)
    return updated


def delete_task(task_id):
    """Delete a task by id. Returns True if a task was removed, False otherwise."""
    with _file_lock:
        tasks = _read_all()
        remaining = [t for t in tasks if t["id"] != task_id]
        deleted = len(remaining) != len(tasks)
        if deleted:
            _write_all(remaining)
    return deleted


def toggle_complete(task_id):
    """Flip a task between 'Completed' and 'Pending'. Returns the updated dict, or None."""
    with _file_lock:
        tasks = _read_all()
        updated = None
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "Pending" if task.get("status") == "Completed" else "Completed"
                updated = task
                break
        if updated:
            _write_all(tasks)
    return updated
