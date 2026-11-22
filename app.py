import os
from datetime import timedelta
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database import get_connection
from matching import match_task

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
# NFR-10: session expires after 30 minutes of inactivity
app.permanent_session_lifetime = timedelta(minutes=30)


def login_required(view):
    """FR-02: block pages for users who are not logged in."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    """FR-01: log in with email and password."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, password_hash, role FROM users WHERE email = %s",
            (email,),
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            session.clear()
            session.permanent = True
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["role"] = user[3]
            return redirect(url_for("home"))

        # Same message for wrong email or wrong password (SD-1)
        flash("Wrong email or password. Please try again.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """FR-03: log out and end the session."""
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, job_title FROM developer_profiles ORDER BY id")
    developers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template(
        "home.html",
        user_name=session["user_name"],
        role=session["role"],
        developers=developers,
    )


@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def new_task():
    """FR-04 to FR-09: enter, check and submit a task."""
    errors = {}
    title = ""
    description = ""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        # FR-06 / FR-07: check required fields and explain the problem
        if not title:
            errors["title"] = "Please enter a short title for the task."
        elif len(title) > 150:
            errors["title"] = "The title must be 150 characters or fewer."
        if not description:
            errors["description"] = "Please describe the task and the skills it needs."

        if not errors:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tasks (title, description, created_by) "
                "VALUES (%s, %s, %s) RETURNING id",
                (title, description, session["user_id"]),
            )
            task_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()

            # FR-09 / FR-23: start matching for the new task
            try:
                match_task(task_id)
                flash("Your task was submitted and matched.")
            except Exception:
                flash("Your task was saved, but matching could not run. Please try again.")
            return redirect(url_for("view_task", task_id=task_id))

    return render_template(
        "new_task.html", errors=errors, title=title, description=description
    )


@app.route("/tasks/<int:task_id>")
@login_required
def view_task(task_id):
    """FR-10, FR-42, FR-43: show the task, its status and ranked candidates."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT title, description, status FROM tasks WHERE id = %s", (task_id,)
    )
    task = cur.fetchone()

    if task is None:
        cur.close()
        conn.close()
        flash("That task was not found.")
        return redirect(url_for("home"))

    cur.execute(
        "SELECT id, outcome FROM match_results WHERE task_id = %s "
        "ORDER BY id DESC LIMIT 1",
        (task_id,),
    )
    result = cur.fetchone()

    recommendations = []
    if result and result[1] == "results":
        cur.execute(
            "SELECT r.rank, d.name, d.job_title, r.score, r.explanation, "
            "r.limited_evidence FROM recommendations r "
            "JOIN developer_profiles d ON d.id = r.profile_id "
            "WHERE r.match_result_id = %s ORDER BY r.rank",
            (result[0],),
        )
        recommendations = cur.fetchall()

    cur.close()
    conn.close()
    return render_template(
        "task.html",
        task=task,
        outcome=result[1] if result else None,
        recommendations=recommendations,
    )


if __name__ == "__main__":
    app.run(debug=True)