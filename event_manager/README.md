# Event Management System

## Overview
The Event Management System is a Django-based web application that allows users to create, manage, and participate in events. This project is designed to demonstrate fundamental Django concepts and provide a practical example for beginners.

## Features
- User registration and authentication
- Create, edit, and delete events
- Browse and search for events
- Register for events
- User dashboard to manage created events and event registrations

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
