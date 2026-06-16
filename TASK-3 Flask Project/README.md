# My Notes App - Flask Mini Project

A simple CRUD notes application built with Flask and Bootstrap.

## Features
- Create, Read, Update, Delete notes
- Flash messages for feedback
- Notes stored in a JSON file (no database needed)
- Clean Bootstrap UI

## How to Run

1. **Clone the repo**
   ```
   git clone <your-repo-url>
   cd flask_notes_app
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000`

## Project Structure
```
flask_notes_app/
├── app.py              # Main Flask application
├── notes.json          # Data storage (auto-created)
├── requirements.txt
├── static/
│   └── style.css       # Custom styles
└── templates/
    ├── base.html       # Base layout with navbar
    ├── index.html      # Home - list all notes
    ├── add_note.html   # Add note form
    ├── edit_note.html  # Edit note form
    └── view_note.html  # View single note
```

## Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | List all notes |
| `/add` | GET, POST | Add new note |
| `/edit/<id>` | GET, POST | Edit a note |
| `/view/<id>` | GET | View a note |
| `/delete/<id>` | POST | Delete a note |