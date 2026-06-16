from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mysecretkey123"

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

@app.route("/")
def index():
    notes = load_notes()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content are required!", "danger")
            return render_template("add_note.html")

        notes = load_notes()
        new_note = {
            "id": len(notes) + 1 if notes else 1,
            "title": title,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        # Make sure IDs are unique even after deletions
        existing_ids = [n["id"] for n in notes]
        new_id = 1
        while new_id in existing_ids:
            new_id += 1
        new_note["id"] = new_id

        notes.append(new_note)
        save_notes(notes)
        flash("Note added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add_note.html")

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    notes = load_notes()
    note = next((n for n in notes if n["id"] == note_id), None)

    if note is None:
        flash("Note not found!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content are required!", "danger")
            return render_template("edit_note.html", note=note)

        note["title"] = title
        note["content"] = content
        note["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_notes(notes)
        flash("Note updated!", "success")
        return redirect(url_for("index"))

    return render_template("edit_note.html", note=note)

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    notes = load_notes()
    notes = [n for n in notes if n["id"] != note_id]
    save_notes(notes)
    flash("Note deleted.", "info")
    return redirect(url_for("index"))

@app.route("/view/<int:note_id>")
def view_note(note_id):
    notes = load_notes()
    note = next((n for n in notes if n["id"] == note_id), None)
    if note is None:
        flash("Note not found!", "danger")
        return redirect(url_for("index"))
    return render_template("view_note.html", note=note)

if __name__ == "__main__":
    app.run(debug=True)