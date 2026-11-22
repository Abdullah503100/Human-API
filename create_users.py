"""Create sample login users with hashed passwords (run once)."""
from werkzeug.security import generate_password_hash
from database import get_connection

USERS = [
    ("Admin User", "admin@humanapi.test", "admin123", "admin"),
    ("Maya Manager", "manager@humanapi.test", "manager123", "manager"),
    ("Hana HR", "hr@humanapi.test", "hr123", "hr"),
]

conn = get_connection()
cur = conn.cursor()
for name, email, password, role in USERS:
    cur.execute(
        "INSERT INTO users (name, email, password_hash, role) "
        "VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING",
        (name, email, generate_password_hash(password), role),
    )
conn.commit()
cur.close()
conn.close()
print("Users created.")