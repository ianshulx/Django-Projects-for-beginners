# Django To-Do App

A full-featured **Django To-Do List** application with user authentication, task management, and priority tracking. Designed for clean code, security, and scalability.

---

## 🚀 Features

- **User Authentication**  
  Register, login, and logout functionality with Django's built-in auth system.

- **Task Management (CRUD)**  
  - Create, read, update, delete tasks
  - Tasks are user-specific; each user can only access their own tasks

- **Task Attributes**
  - Title, Description, Priority (Low, Medium, High)
  - Completion status
  - Due date with validation (cannot be in the past)

- **User Feedback**
  - Success and error messages for all actions using Django messages framework

- **Security & Best Practices**
  - LoginRequiredMixin for views
  - UserPassesTestMixin to prevent unauthorized access
  - CSRF protection in all forms
  - Proper validation in forms

- **Responsive UI**
  - Modern design with Bootstrap 5
  - Unified form template for create/update tasks
  - Styled task list and homepage

- **Testing**
  - Unit tests for models, forms, and views
  - Permission tests to prevent users from accessing others' tasks

---

## 📦 Installation

1. Clone the repository:
   ```
   git clone https://github.com/reza-khalili-dev/django-todo.git
   cd django-todo
Create and activate virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Apply migrations:

python manage.py migrate
Create a superuser (optional):

python manage.py createsuperuser
Run the development server:

python manage.py runserver
🧪 Running Tests
Run all unit tests with:

python manage.py test
🖌️ Code Quality
Code formatted with Black

Imports sorted with isort

Linting with flake8

⚙️ Deployment
Separate settings for development and production

Use PostgreSQL in production

Static files served via Whitenoise

Environment variables for sensitive data (SECRET_KEY, DEBUG, etc.)

Recommended deployment platforms: Render, Railway, or Fly.io

📂 Project Structure

django-todo/
│
├── config/          # Django project settings
├── tasks/           # Main app for task management
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── tests.py
│   └── urls.py
├── venv/
├── manage.py
└── requirements.txt

💡 Future Improvements
Drag & drop task ordering

Task notifications/alerts

Export tasks (CSV/JSON)

REST API with Django REST Framework

Mobile-friendly interface

📄 License
This project is licensed under the MIT License.