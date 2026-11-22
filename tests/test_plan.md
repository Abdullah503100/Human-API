# Test Plan - Human API

| ID | Feature | Steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| TC01 | Protected page (FR-02) | Open the home page without logging in | Redirected to login with "Please log in to continue." | Redirected to login with the message | Pass |
| TC02 | Login, wrong password (FR-01) | Log in with admin@humanapi.test / wrong | "Wrong email or password. Please try again." | Message shown, stayed on login | Pass |
| TC03 | Login, correct (FR-01) | Log in with admin@humanapi.test / admin123 | Home page with developer list | Home page shown with 8 developers | Pass |
| TC04 | Logout (FR-03) | Click Log out | Back at login with "You have been logged out." | Message shown | Pass |
| TC05 | Session after logout (FR-03) | Open the home page after logging out | Redirected to login | Redirected to login | Pass |
| TC06 | Empty task form (FR-06, FR-07) | Submit with both fields empty | Both error messages shown | Both errors shown | Pass |
| TC07 | Title only (FR-08) | Submit with only a title | Description error, title kept | Error shown, title kept | Pass |
| TC08 | Valid task (FR-09, FR-10) | Submit "Payroll API" / "Need Python, Flask and PostgreSQL experience" | "Submitted and matched", status completed | Shown as expected | Pass |
| TC09 | Ranking and explanations (FR-31 to FR-37) | Same task as TC08 | Ranked list, Sara Ali first with skills, project and work listed | Sara Ali first (score 13), explanations shown | Pass |
| TC10 | Limited evidence (FR-38) | Submit "Java bug fix" / "Fix a small Java issue" | Hamad Rashid with "Limited evidence" note | Hamad Rashid shown with the note | Pass |
| TC11 | No match (FR-39) | Submit "Garden design" / "Plan an underwater basket weaving garden" | "No developer profile matches this task." | Message shown | Pass |