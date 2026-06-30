from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

import storage

# --------------------------------------------------------------------------
# App configuration
# --------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this-in-production"  # needed for flash messages

VALID_PRIORITIES = ["Low", "Medium", "High"]
VALID_STATUSES = ["Pending", "In Progress", "Completed"]


# --------------------------------------------------------------------------
# Template filter: format the ISO timestamp we store, nicely
# --------------------------------------------------------------------------
@app.template_filter("nice_datetime")
def nice_datetime(value):
    """Convert an ISO timestamp string (e.g. '2026-06-29T18:30:00') into
    something readable, e.g. '29 Jun 2026, 06:30 PM'."""
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        return value


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.route("/")
def index():
    """READ: show all tasks. Supports simple filtering via query string."""
    status_filter = request.args.get("status", "All")
    tasks = storage.get_all_tasks(status_filter=status_filter)

    return render_template(
        "index.html",
        tasks=tasks,
        statuses=VALID_STATUSES,
        current_filter=status_filter,
    )


@app.route("/task/<int:task_id>")
def view_task(task_id):
    """READ: view a single task's full detail."""
    task = storage.get_task(task_id)
    if task is None:
        flash("That task doesn't exist (maybe it was already deleted).", "warning")
        return redirect(url_for("index"))
    return render_template("view_task.html", task=task)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    """CREATE: GET shows the empty form, POST processes submission."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        due_date = request.form.get("due_date", "").strip()

        # Basic server-side validation
        errors = []
        if not title:
            errors.append("Title is required.")
        if priority not in VALID_PRIORITIES:
            errors.append("Invalid priority selected.")

        if errors:
            for err in errors:
                flash(err, "danger")
            # Re-render form, keeping whatever the user already typed
            return render_template(
                "add_task.html",
                priorities=VALID_PRIORITIES,
                form_data=request.form,
            )

        storage.add_task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )

        flash(f'Task "{title}" was added successfully!', "success")
        return redirect(url_for("index"))

    # GET request -> show blank form
    return render_template("add_task.html", priorities=VALID_PRIORITIES, form_data={})


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """UPDATE: GET shows form pre-filled with existing data, POST saves changes."""
    task = storage.get_task(task_id)
    if task is None:
        flash("That task doesn't exist (maybe it was already deleted).", "warning")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        status = request.form.get("status", "Pending")
        due_date = request.form.get("due_date", "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if priority not in VALID_PRIORITIES:
            errors.append("Invalid priority selected.")
        if status not in VALID_STATUSES:
            errors.append("Invalid status selected.")

        if errors:
            for err in errors:
                flash(err, "danger")
            # Re-render with what the user just typed, not the stale stored task
            task_with_attempted_edits = {
                **task,
                "title": title,
                "description": description,
                "priority": priority,
                "status": status,
                "due_date": due_date,
            }
            return render_template(
                "edit_task.html",
                task=task_with_attempted_edits,
                priorities=VALID_PRIORITIES,
                statuses=VALID_STATUSES,
            )

        storage.update_task(
            task_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date,
        )

        flash(f'Task "{title}" was updated successfully!', "success")
        return redirect(url_for("index"))

    # GET request -> show form pre-filled with current task data
    return render_template(
        "edit_task.html",
        task=task,
        priorities=VALID_PRIORITIES,
        statuses=VALID_STATUSES,
    )


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """DELETE: remove a task. Triggered by a confirm form, not a bare link."""
    task = storage.get_task(task_id)
    deleted = storage.delete_task(task_id)

    if deleted:
        flash(f'Task "{task["title"]}" was deleted.', "info")
    else:
        flash("That task doesn't exist (maybe it was already deleted).", "warning")

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    """Quick action: toggle a task between Completed and Pending from the list view."""
    updated = storage.toggle_complete(task_id)
    if updated is None:
        flash("That task doesn't exist (maybe it was already deleted).", "warning")
    return redirect(url_for("index"))


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
