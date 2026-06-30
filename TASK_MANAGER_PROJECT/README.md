# Flask Task Manager — Mini Project (JSON file storage)

A simple, full-CRUD Task Manager built with Flask and Bootstrap 5.
Built as a backend-fundamentals demo: routing, templates, form handling (GET & POST), and CRUD — with data persisted in a plain `tasks.json` file, no database required.

## Features

- **Create** — add a new task with title, description, priority, and due date
- **Read** — view all tasks (with status filter) and view a single task's detail page
- **Update** — edit any task, including marking it Pending / In Progress / Completed
- **Delete** — remove a task (with a confirmation prompt)
- **Quick complete/reopen toggle** from the task list
- **Form validation** — empty titles and invalid values are rejected with flash messages, and the form re-renders with what you already typed
- **Clean, responsive UI** using Bootstrap 5 + Bootstrap Icons
- **No database** — all tasks live in `data/tasks.json`, a human-readable file you can open and inspect directly

## Tech Stack

- **Backend:** Flask 3
- **Storage:** A single JSON file (`data/tasks.json`), read/written via Python's built-in `json` module — no SQL, no ORM, no external DB service
- **Frontend:** Jinja2 templates + Bootstrap 5 (via CDN) + small custom CSS file

## Project Structure

```
flask_task_manager/
├── app.py                  # Flask app: routes, form handling, calls into storage.py
├── storage.py               # All JSON file read/write logic (the "data layer")
├── requirements.txt
├── README.md
├── data/
│   └── tasks.json           # Where all tasks are stored, auto-created if missing
├── templates/
│   ├── base.html            # Shared layout: navbar, flash messages, footer
│   ├── index.html           # Task list page (Read + filter)
│   ├── add_task.html        # Create form (GET shows form, POST saves)
│   ├── edit_task.html       # Update form (pre-filled)
│   └── view_task.html       # Single task detail page
└── static/
    └── style.css             # Custom styling on top of Bootstrap
```

## How `tasks.json` works

Each task is stored as a JSON object inside a list, e.g.:

```json
[
  {
    "id": 1,
    "title": "Write report",
    "description": "Internship summary",
    "priority": "High",
    "status": "Pending",
    "due_date": "2026-07-01",
    "created_at": "2026-06-30T03:39:22"
  }
]
```

All reading and writing happens inside **`storage.py`** — `app.py` never touches the file directly. This separation means:
- Route logic in `app.py` stays focused on handling requests and forms
- All file I/O (including a `threading.Lock` to avoid two simultaneous requests corrupting the file) is isolated in one place
- It would be straightforward to later swap `storage.py` for a real database without changing `app.py` much

## How to Run

1. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   (Just Flask — no database driver needed.)

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open your browser** at:
   ```
   http://127.0.0.1:5000/
   ```

`data/tasks.json` is created automatically (as an empty list) the first time the app needs it, if it doesn't already exist.

## Routes Overview

| Route | Methods | Purpose |
|---|---|---|
| `/` | GET | List all tasks, optional `?status=` filter |
| `/task/<id>` | GET | View a single task's details |
| `/add` | GET, POST | Show add-task form / handle form submission |
| `/edit/<id>` | GET, POST | Show pre-filled edit form / handle update |
| `/delete/<id>` | POST | Delete a task |
| `/complete/<id>` | POST | Toggle a task between Completed and Pending |

## Things to Highlight in a Walkthrough / Interview

- **GET vs POST on the same route** (`/add`, `/edit/<id>`): the same view function renders the form on `GET` and processes/validates it on `POST` — the classic Flask pattern.
- **Server-side validation**: required fields and allowed values (priority/status) are checked in `app.py` before saving; on failure, the form re-renders with the user's input preserved and an error flash message.
- **File-based persistence**: `storage.py` reads the entire JSON file, modifies the in-memory list, then writes it back — a simple, transparent way to persist data without a database engine.
- **`url_for()`** is used everywhere instead of hardcoded URLs, so routes can be renamed without breaking links.
- **Flash messages** give user feedback after every create/update/delete action.
- **Template inheritance** (`{% extends "base.html" %}`) keeps the navbar/footer/flash-message logic in one place.
- **Graceful missing-data handling**: visiting a task id that no longer exists redirects back to the list with a warning, instead of crashing.

## Limitations of JSON file storage (good talking points)

- Not safe for high concurrency — every write rewrites the whole file. A `Lock` is used here to avoid corruption from simultaneous requests, but this won't scale to many concurrent users.
- No querying/indexing — every read loads the entire file into memory and filters in Python.
- No relationships, transactions, or migrations — fine for a small mini-project, but a real database (SQLite/Postgres) would be the next step for anything production-bound.

## Possible Extensions (if asked "what would you add next?")

- Swap `storage.py` for a real database (SQLite via SQLAlchemy) — `app.py` wouldn't need to change much
- User authentication (Flask-Login) so each user has their own task file
- A REST API (JSON endpoints) alongside the HTML views
- Categories/tags, search, or sorting
- Pagination for large task lists
