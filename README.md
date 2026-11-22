# Human API

A developer-matching web app that helps a company find the best developer for a task based on their skills, past projects and completed work.

SWE 401 group project, Abu Dhabi University, Fall 2026.

## Team Members
- Abdullah Hisham Ibrahim
- Abdel Rahman Dabash
- Zaid Himmo


## Problem
Managers often assign tasks based on CVs or memory, which do not show a person's real skills. Human API compares a task description with each developer's recorded skills, projects and completed work, and suggests a ranked list of suitable developers with a short explanation for each. The final decision always stays with the manager.

## Key Features
- Log in and log out, with protected pages and a 30-minute session timeout
- Task form with required-field checks and clear error messages
- Lexical matching of the task against skills, projects and completed work
- Ranked list of developers with a score and an explanation for each
- "Limited evidence" warning when a suggestion is based on only one item
- Clear message when no developer matches the task
- All data stored in PostgreSQL

## Technologies
- Python 3.14
- Flask (web framework)
- PostgreSQL 17 (database)
- psycopg2 (PostgreSQL driver for Python)
- HTML templates (Jinja2)
- Git and GitHub
- VS Code and pgAdmin 4

## Prerequisites
- Python 3.10 or newer
- PostgreSQL 17 (with pgAdmin 4)
- Git

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Abdullah503100/Human-API.git
   cd Human-API
   ```
2. Install the Python libraries:
   ```
   pip install -r requirements.txt
   ```
3. In pgAdmin, create a database named `humanapi`.
4. Open the Query Tool on `humanapi` and run `schema.sql`, then `sample_data.sql`.

## Configuration
The app reads the database settings from environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `DB_HOST` | `localhost` | Database server |
| `DB_PORT` | `5432` | Database port |
| `DB_NAME` | `humanapi` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | (none) | Your PostgreSQL password |
| `SECRET_KEY` | development key | Key used to sign sessions |

In PowerShell, set your password before running the app:
```
$env:DB_PASSWORD="your_password"
```

## How to Run
1. Create the sample login users (only once):
   ```
   python create_users.py
   ```
2. Start the app:
   ```
   python app.py
   ```
3. Open `http://127.0.0.1:5000` in your browser.
4. Log in with a sample account:

| Email | Password | Role |
|---|---|---|
| admin@humanapi.test | admin123 | admin |
| manager@humanapi.test | manager123 | manager |
| hr@humanapi.test | hr123 | hr |

## How to Test
The test cases are listed in `tests/test_plan.md`. To try the main ones:
1. Open the home page without logging in. You are sent to the login page.
2. Log in with a wrong password. You see "Wrong email or password."
3. Log in correctly, click "Submit a new task" and submit with empty fields. Both error messages appear.
4. Submit the task "Payroll API" with the description "Need Python, Flask and PostgreSQL experience". A ranked list appears with Sara Ali first.
5. Submit "Java bug fix" / "Fix a small Java issue". Hamad Rashid appears with a "Limited evidence" note.
6. Submit "Garden design" / "Plan an underwater basket weaving garden". The app shows that no developer matches.