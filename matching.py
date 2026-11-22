"""Simple lexical matching for the HumanAPI prototype (FR-23 to FR-41, FR-30)."""
import re

from database import get_connection

# Common words that should not count as a match
STOPWORDS = {
    "a", "an", "and", "or", "the", "to", "of", "in", "on", "at", "by", "for",
    "with", "from", "into", "as", "is", "are", "be", "it", "this", "that",
    "we", "our", "who", "can", "should", "will", "has", "have", "need", "needs",
    "experience", "experienced", "build", "built", "building", "use", "using",
    "make", "create", "created", "new", "task", "work", "project", "developer",
    "someone", "person", "good", "strong", "knowledge", "skill", "skills",
    "required",
}

SKILL_POINTS = 3
EVIDENCE_POINTS = 2
MAX_LISTED = 3


def tokenize(text):
    """Split text into a set of meaningful lowercase words."""
    words = re.findall(r"[a-z0-9+#]+", (text or "").lower())
    return {w for w in words if len(w) > 1 and w not in STOPWORDS}


def skill_in_text(skill_name, text_lower):
    """True if the skill name appears as a whole word or phrase in the text."""
    pattern = r"(?<![a-z0-9])" + re.escape(skill_name.lower()) + r"(?![a-z0-9])"
    return re.search(pattern, text_lower) is not None


def load_profiles(cur):
    """FR-23 to FR-26: read profiles, skills, projects and completed work."""
    cur.execute("SELECT id, name, job_title FROM developer_profiles ORDER BY id")
    profiles = {
        pid: {"id": pid, "name": name, "skills": [], "projects": [], "work": []}
        for pid, name, _job_title in cur.fetchall()
    }

    cur.execute(
        "SELECT ps.profile_id, s.name FROM profile_skills ps "
        "JOIN skills s ON s.id = ps.skill_id"
    )
    for pid, skill in cur.fetchall():
        profiles[pid]["skills"].append(skill)

    cur.execute(
        "SELECT pp.profile_id, p.name, p.description, pp.role "
        "FROM project_participation pp JOIN projects p ON p.id = pp.project_id"
    )
    for pid, name, description, role in cur.fetchall():
        profiles[pid]["projects"].append(
            (name, f"{name} {description or ''} {role or ''}")
        )

    cur.execute("SELECT profile_id, title, description FROM completed_work")
    for pid, title, description in cur.fetchall():
        profiles[pid]["work"].append((title, f"{title} {description or ''}"))

    return list(profiles.values())


def score_profile(profile, task_text):
    """FR-27 to FR-29: compare the task with skills, projects and work."""
    text_lower = task_text.lower()
    task_words = tokenize(task_text)

    skills = [s for s in profile["skills"] if skill_in_text(s, text_lower)]
    projects = [n for n, text in profile["projects"] if task_words & tokenize(text)]
    work = [t for t, text in profile["work"] if task_words & tokenize(text)]

    score = SKILL_POINTS * len(skills) + EVIDENCE_POINTS * (len(projects) + len(work))
    evidence_count = len(skills) + len(projects) + len(work)
    return score, skills, projects, work, evidence_count


def explain(skills, projects, work, limited):
    """FR-34 to FR-38: short explanation of why someone was suggested."""
    parts = []
    if skills:
        parts.append("Matching skills: " + ", ".join(skills[:MAX_LISTED]) + ".")
    if projects:
        parts.append("Related projects: " + ", ".join(projects[:MAX_LISTED]) + ".")
    if work:
        parts.append("Related completed work: " + ", ".join(work[:MAX_LISTED]) + ".")
    if limited:
        parts.append(
            "Limited evidence: based on only one item, so check the profile before deciding."
        )
    return " ".join(parts)


def match_task(task_id):
    """Run matching for one task and save the ranked results (FR-31, FR-49)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT title, description FROM tasks WHERE id = %s", (task_id,))
        title, description = cur.fetchone()
        task_text = f"{title} {description}"

        candidates = []
        for profile in load_profiles(cur):
            score, skills, projects, work, evidence_count = score_profile(
                profile, task_text
            )
            if score > 0:
                limited = evidence_count <= 1
                candidates.append(
                    (score, profile["name"], profile["id"],
                     explain(skills, projects, work, limited), limited)
                )

        # FR-32: strongest match first
        candidates.sort(key=lambda c: (-c[0], c[1]))

        outcome = "results" if candidates else "no_match"
        cur.execute(
            "INSERT INTO match_results (task_id, outcome) VALUES (%s, %s) RETURNING id",
            (task_id, outcome),
        )
        result_id = cur.fetchone()[0]

        for rank, (score, _name, profile_id, explanation, limited) in enumerate(
            candidates, start=1
        ):
            cur.execute(
                "INSERT INTO recommendations "
                "(match_result_id, profile_id, rank, score, explanation, limited_evidence) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (result_id, profile_id, rank, score, explanation, limited),
            )

        cur.execute("UPDATE tasks SET status = 'completed' WHERE id = %s", (task_id,))
        conn.commit()
    except Exception:
        # FR-45 / FR-46: record the error instead of showing wrong results
        conn.rollback()
        cur.execute(
            "INSERT INTO match_results (task_id, outcome) VALUES (%s, 'error')",
            (task_id,),
        )
        cur.execute("UPDATE tasks SET status = 'failed' WHERE id = %s", (task_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()