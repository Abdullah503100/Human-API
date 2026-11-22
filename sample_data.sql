-- Sample data for testing (fake people only, FR-50)

INSERT INTO skills (name, description) VALUES
('Python', 'Programming language'),
('Java', 'Programming language'),
('JavaScript', 'Web programming language'),
('React', 'Frontend library'),
('SQL', 'Database query language'),
('PostgreSQL', 'Relational database'),
('Flask', 'Python web framework'),
('Machine Learning', 'Building predictive models'),
('Docker', 'Containers and deployment'),
('UI Design', 'Designing user interfaces'),
('Testing', 'Unit and integration testing'),
('Networking', 'Computer networks');

INSERT INTO developer_profiles (name, job_title) VALUES
('Sara Ali', 'Backend Developer'),
('Omar Khalid', 'Frontend Developer'),
('Lina Hassan', 'Data Scientist'),
('Yousef Saeed', 'Full Stack Developer'),
('Mariam Nasser', 'QA Engineer'),
('Khalid Omar', 'DevOps Engineer'),
('Noor Ahmed', NULL),
('Hamad Rashid', 'Junior Developer');

INSERT INTO profile_skills (profile_id, skill_id) VALUES
(1, 1), (1, 5), (1, 6), (1, 7),
(2, 3), (2, 4), (2, 10),
(3, 1), (3, 8), (3, 5),
(4, 1), (4, 3), (4, 4), (4, 5), (4, 7),
(5, 11), (5, 1),
(6, 9), (6, 12), (6, 1),
(8, 2);

INSERT INTO projects (name, description) VALUES
('Payroll System', 'Backend API for salary processing with PostgreSQL'),
('Company Website', 'Responsive website built with React'),
('Sales Prediction', 'Machine learning model to predict monthly sales'),
('Cloud Migration', 'Moving services to Docker containers');

INSERT INTO project_participation (profile_id, project_id, role) VALUES
(1, 1, 'Backend developer'),
(4, 1, 'API developer'),
(2, 2, 'Frontend developer'),
(4, 2, 'Full stack developer'),
(3, 3, 'Data scientist'),
(6, 4, 'DevOps engineer'),
(5, 1, 'Tester');

INSERT INTO completed_work (profile_id, project_id, title, description) VALUES
(1, 1, 'Built salary REST API', 'Created Flask endpoints and PostgreSQL queries'),
(2, 2, 'Homepage redesign', 'Built React components for the homepage'),
(3, 3, 'Sales model', 'Trained a Python machine learning model'),
(4, 2, 'Login page', 'Built login form in React and Flask backend'),
(5, 1, 'API test suite', 'Wrote automated tests for the payroll API'),
(6, 4, 'Docker setup', 'Containerized services with Docker'),
(7, NULL, 'Internal wiki', 'Wrote documentation pages');