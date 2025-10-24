Project Title: Book Club Manager
Team: Group 12
Participant: Michael Somuah
Category: DevOps — Ecowas Software Development Tournament 2025
1. Overview
As  Group 12, we designed and implemented the Book Club Manager — a Streamlit web application connected to a MySQL database that helps book clubs organize books, meetings, and discussions.
The project was developed following DevOps principles, focusing on collaboration, automation, and continuous improvement.

2. Personal Roles and Responsibilities
Role	Responsibilities	Tasks Completed
Project Manager & UI Lead	Designed the user interface and managed the overall project workflow.	Created the sidebar form for adding books, layout for tabs, and presentation slides.
Backend Developer	Developed backend logic and database connectivity.	Integrated MySQL, handled CRUD operations, and implemented data validation and updates.
Data Specialist	Structured and maintained the database.	Created database schema (bookclubdb), ensured referential integrity, and wrote bookclub_setup.sql.
Visualization & Analytics Developer	Implemented data visualization using Plotly.	Designed bar charts for genre distribution and histograms for reading progress.
Feature Developer & QA Tester	Added login authentication and tested full system.	Built login page (Group12 / Devops), tested all CRUD features, and debugged validation issues.

3. Key Contributions
Connected the app to MySQL for data persistence.
Implemented user authentication with SHA-256 password hashing.
Developed all CRUD functionalities for adding, editing, and deleting books.
Added a meeting planner feature to schedule book discussions.
Designed Plotly Express analytics for genre and progress visualization.
Created CSV export functionality for data reports.
Authored the README.md, presentation slides, and demo script.

4. Tools and Technologies Used
Programming Language: Python
Framework: Streamlit
Database: MySQL
Libraries: Pandas, Plotly Express, mysql-connector-python
Version Control: Git & GitHub
Environment: VS Code and XAMPP

5. Challenges and Solutions
Challenge	Solution
Database connection errors	Configured connection using mysql.connector and ensured correct host/user setup.
Password security	Implemented SHA-256 password hashing before saving to database.
Chart visualization	Used Plotly Express to create interactive charts dynamically from database records.
Input validation	Added error handling for page count and empty fields in Streamlit forms.
6. Reflection

This project enhanced my understanding of full-stack development, database management, and DevOps principles such as collaboration, automation, and testing.
It helped me build confidence in integrating Python with MySQL and developing secure, data-driven applications.

7. Conclusion

As the only developer in Group 12, I successfully designed, built, and deployed the Book Club Manager app from scratch — fulfilling all rubric requirements and implementing additional advanced features such as authentication and analytics.
This project represents a complete, professional-grade solution for managing book clubs.