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