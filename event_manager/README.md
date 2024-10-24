# Event Management System

## Overview
The Event Management System is a beginner-friendly Django web app that allows users to create, manage, and participate in events. It demonstrates core Django concepts, providing hands-on experience for new developers.

## Features
- User registration & authentication
- Event creation, editing, and deletion
- Event browsing & search functionality
- Event registration & user dashboard

## Technologies Used
- Django 4.2
- Python 3.9+
- HTML/CSS
- JavaScript
- SQLite (default database, can be changed to PostgreSQL for production)


## Project Structure
```
event_management/
├── event_management/  # Project settings
├── events/            # Main app
│   ├── models.py      # Event and Registration models
│   ├── views.py       # View functions
│   ├── urls.py        # URL patterns
│   ├── forms.py       # Forms for event creation and registration
│   └── templates/     # HTML templates
├── manage.py
└── requirements.txt
```

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `python manage.py runserver`