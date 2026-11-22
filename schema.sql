CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE developer_profiles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100)
);

CREATE TABLE profile_skills (
    profile_id INTEGER REFERENCES developer_profiles(id),
    skill_id INTEGER REFERENCES skills(id),
    PRIMARY KEY (profile_id, skill_id)
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT
);

CREATE TABLE project_participation (
    profile_id INTEGER REFERENCES developer_profiles(id),
    project_id INTEGER REFERENCES projects(id),
    role VARCHAR(100),
    PRIMARY KEY (profile_id, project_id)
);

CREATE TABLE completed_work (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER NOT NULL REFERENCES developer_profiles(id),
    project_id INTEGER REFERENCES projects(id),
    title VARCHAR(150) NOT NULL,
    description TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
        CHECK (role IN ('hr', 'manager', 'team_leader', 'developer', 'admin'))
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'submitted'
        CHECK (status IN ('draft', 'submitted', 'processing', 'completed', 'failed')),
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE match_results (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    outcome VARCHAR(20) NOT NULL
        CHECK (outcome IN ('results', 'no_match', 'error')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    match_result_id INTEGER NOT NULL REFERENCES match_results(id),
    profile_id INTEGER NOT NULL REFERENCES developer_profiles(id),
    rank INTEGER NOT NULL,
    score NUMERIC(5,2) NOT NULL,
    explanation TEXT NOT NULL,
    limited_evidence BOOLEAN NOT NULL DEFAULT FALSE
);