from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4
import re

app = FastAPI(title="Human API Learning Prototype", version="0.1.0")

# Fictional sample records only. Never load private employee data into this demo.
EMPLOYEES = [
    {
        "id": "E-001", "name": "Maya Hassan", "department": "Engineering",
        "skills": ["python", "fastapi", "postgresql", "api design"],
        "projects": ["built an internal REST API and optimized database queries"],
        "completed_tasks": ["fixed slow SQL queries and added API validation"]
    },
    {
        "id": "E-002", "name": "Omar Khalil", "department": "Data",
        "skills": ["python", "data analysis", "pandas", "machine learning"],
        "projects": ["created a data quality dashboard and forecasting pipeline"],
        "completed_tasks": ["cleaned customer datasets and evaluated classification models"]
    },
    {
        "id": "E-003", "name": "Lina Nasser", "department": "Platform",
        "skills": ["javascript", "react", "testing", "ui design"],
        "projects": ["developed a React dashboard for internal users"],
        "completed_tasks": ["implemented reusable UI components and frontend tests"]
    }
]
REQUESTS = {}

class MatchRequest(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    description: str = Field(min_length=10, max_length=4000)

def tokens(text: str):
    return set(re.findall(r"[a-zA-Z0-9+#.]+", text.lower()))

def rank_employee(query_tokens, employee):
    evidence = {
        "skills": employee["skills"],
        "projects": employee["projects"],
        "completed_tasks": employee["completed_tasks"]
    }
    matched = []
    sources = []
    for source, values in evidence.items():
        source_tokens = set()
        for value in values:
            source_tokens |= tokens(value)
        overlap = sorted(query_tokens & source_tokens)
        if overlap:
            matched.extend(overlap)
            sources.append(source)
    unique = sorted(set(matched))
    # Transparent lexical baseline: percentage of task terms found in employee evidence.
    score = round((len(unique) / max(len(query_tokens), 1)) * 100, 2)
    if len(unique) == 0:
        level = "insufficient"
    elif len(unique) < 3:
        level = "limited"
    else:
        level = "reasonable"
    explanation = (
        f"Matched terms: {', '.join(unique)}. Evidence found in: {', '.join(sources) or 'no stored evidence'}. "
        "This is a keyword-overlap indicator, not proof of ability."
    )
    return {
        "employee_id": employee["id"], "name": employee["name"],
        "department": employee["department"], "score": score,
        "matched_terms": unique, "evidence_sources": sources,
        "evidence_level": level, "explanation": explanation
    }

@app.get("/health")
def health():
    return {"status": "ok", "prototype": "learning-only"}

@app.get("/employees")
def list_employees():
    return EMPLOYEES

@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    for employee in EMPLOYEES:
        if employee["id"] == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee profile not found")

@app.post("/matches")
def create_match(request: MatchRequest):
    query = tokens(request.title + " " + request.description)
    results = [rank_employee(query, employee) for employee in EMPLOYEES]
    results.sort(key=lambda item: item["score"], reverse=True)
    request_id = str(uuid4())
    response = {
        "request_id": request_id,
        "title": request.title,
        "status": "completed",
        "decision_notice": "Recommendations support a human decision; the system does not assign or hire anyone.",
        "results": results
    }
    REQUESTS[request_id] = response
    return response

@app.get("/matches/{request_id}")
def get_match(request_id: str):
    if request_id not in REQUESTS:
        raise HTTPException(status_code=404, detail="Matching request not found")
    return REQUESTS[request_id]
