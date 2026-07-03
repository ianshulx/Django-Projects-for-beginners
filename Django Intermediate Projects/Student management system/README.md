# Student Management System

A Django-based student management system for managing students, staff, subjects, courses, sessions, attendance, leave requests, feedback, and student results. The project includes separate dashboards for HOD, staff, and students.

## Project Overview

This project is a beginner-friendly Django application that demonstrates role-based access with three main user types:

- HOD / Admin
- Staff / Teacher
- Student

It is designed as a learning project and can be extended for real-world use.

## Main Features

### Admin / HOD
- View dashboard summaries and charts
- Add, update, and delete staff
- Add, update, and delete students
- Manage courses and subjects
- Manage academic sessions
- View attendance records
- Review student and staff feedback
- Approve or reject leave requests

### Staff
- View staff dashboard
- Take and update student attendance
- Add or update student results
- Apply for leave
- Send feedback to admin

### Student
- View personal attendance and results
- Apply for leave
- Send feedback to admin
- Update profile details

## Tech Stack
- Python
- Django
- SQLite
- HTML, CSS, JavaScript
- Bootstrap / AdminLTE-style UI templates

## Project Structure
- `student_management_system/` – project settings and root URL configuration
- `student_management_app/` – main app containing models, views, forms, URLs, templates, and middleware
- `static/` – CSS, JavaScript, and image assets
- `media/` – uploaded profile pictures and other media

## Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd "Student management system"
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations
   ```bash
   python manage.py migrate
   ```

5. Run the development server
   ```bash
   python manage.py runserver
   ```

6. Create a superuser (optional)
   ```bash
   python manage.py createsuperuser
   ```

## Default Login Notes
You can also use the demo-style credentials if available in the project setup, but it is recommended to create a new superuser for a clean environment.

## Recent Fixes Applied
The project had missing AdminLTE theme assets referenced by the templates. These were updated so the dashboard UI loads correctly.

## Notes for Future Improvements
- Upgrade Django and dependencies to a supported version
- Replace hard-coded defaults in user creation signals with safer setup logic
- Improve authentication flow to use Django's standard `authenticate()` function consistently
- Add tests for login, attendance, and CRUD workflows
- Add proper environment variable handling for secret keys and database settings
- Improve file upload handling for profile pictures

