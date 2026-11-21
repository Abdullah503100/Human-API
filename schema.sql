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