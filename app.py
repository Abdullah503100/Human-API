import os
from datetime import timedelta
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database import get_connection

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


if __name__ == "__main__":
    app.run(debug=True)