from flask import Flask
from database import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, job_title FROM developer_profiles ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    lines = [f"{name} - {job_title}" for name, job_title in rows]
    return "<h1>Human API</h1>" + "<br>".join(lines)


if __name__ == "__main__":
    app.run(debug=True)