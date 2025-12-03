# OYO Clone

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Django CI](https://github.com/LordZeusIsBack/OYO-Clone/actions/workflows/django.yml/badge.svg)](https://github.com/LordZeusIsBack/OYO-Clone/actions/workflows/django.yml)
[![Django](https://img.shields.io/badge/django-4.x-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

**OYO Clone** is a full-stack web application built with Django. It replicates the core functionalities of the OYO platform, allowing users to search and book hotels, while providing hotel vendors with a dedicated dashboard to manage listings. The project is designed with a clean UI, a seamless user experience, and a robust backend powered by PostgreSQL.

## Features

- **User Management:**  
  - Registration, login, and OTP-based verification.
  - Separate interfaces for end-users and hotel vendors.

- **Hotel Management (Vendor Dashboard):**  
  - Add, edit, and delete hotel listings.
  - Upload images and manage hotel details.

- **Home & Landing Page:**  
  - Modern, responsive design.
  - Dynamic content seeded for an enhanced browsing experience.

- **CI/CD Pipeline:**  
  - Integrated GitHub Actions for automated testing on each push or pull request.

## Technologies Used

- **Backend:** Django, Python 3.11  
- **Frontend:** HTML, CSS (responsive design)
- **Database:** PostgreSQL (running on port 5432) with Django ORM migrations  
- **CI/CD:** GitHub Actions

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/LordZeusIsBack/OYO-Clone.git
   cd OYO-Clone
   ```

2. **Set up a virtual environment and activate it:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the PostgreSQL Database:**

   Ensure you have PostgreSQL installed and running (default port `5432`). Create a new database (e.g., `oyoclone`) and update the database settings in the project's `oyo_clone/settings.py` file. An example configuration might look like:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'oyoclone',
           'USER': <Username>,
           'PASSWORD': <Passwoord>,
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Seed initial data (if needed):**

   ```bash
   python manage.py runscript seed_data
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

8. **Access the application:**

   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Project Structure

```
OYO-Clone/
│
├── .github/                # GitHub Actions configuration for CI/CD
│   └── workflows/
│       └── django.yml      # CI workflow for testing with Python 3.11
│
├── accounts/               # Django app handling user and vendor accounts
│   ├── migrations/         # Database migration files
│   ├── templates/          # HTML templates for user/vendor interfaces
│   │   ├── user/           # User-specific pages (login, register, OTP)
│   │   └── vendor/         # Vendor-specific pages (dashboard, add/edit hotel, etc.)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
├── home/                   # Django app for the landing/home page
│   ├── migrations/         # Migrations for home app
│   ├── templates/          # Main homepage and shared UI components
│   │   └── utils/          # Shared template fragments (navbar, alerts, etc.)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── seed_data.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── oyo_clone/              # Main Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings including PostgreSQL configuration
│   ├── urls.py             # URL routing for the entire project
│   └── wsgi.py
│
├── .gitignore              # Files and directories to be ignored by Git
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request describing your changes.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue in the repository or contact [LordZeusIsBack](mailto:anubhavsharma5645@gmail.com).
