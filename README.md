# Task Manager

A Django-based task management application with user authentication, task prioritization, and API support.

## Features

- Custom User Model (email-based authentication)
- Task Management (CRUD operations)
- Task Prioritization and Categories
- User Permissions and Groups
- REST API Support
- Admin Dashboard
- Responsive Frontend

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/MarouaneOuchala/-TaskMaster.git
cd -TaskMaster
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
task_manager/
├── manage.py
├── config/ (Django settings)
├── users/ (Custom User Model, Auth)
├── tasks/ (Task Management)
├── templates/ (HTML templates)
├── static/ (CSS, JS)
├── db.sqlite3
└── requirements.txt
```

## Technologies Used

- Django 4.0
- Django REST Framework
- PostgreSQL/SQLite
- Bootstrap 5
- Crispy Forms 