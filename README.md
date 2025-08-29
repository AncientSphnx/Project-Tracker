🌟 MySite2 – Project & Resource Management System






📌 Overview

MySite2 is a Django-based project & resource management system that helps students, mentors, and admins collaborate effectively.
It provides dashboards, progress tracking, and resource sharing features to streamline academic and organizational project workflows.

🚀 Features

✅ Authentication & Roles – Students, Mentors, and Admins
✅ Custom Dashboards – tailored to each role
✅ Project Management – create, update, delete projects with deadlines
✅ Phases & Tasks – organize projects into phases and track completion
✅ Progress Tracker – visualize project, phase, and task progress
✅ Resource Sharing – mentors ↔ students file exchange
✅ Profile Management – update profile picture & details
✅ Notifications & Updates – keep track of changes with comments

🏗️ Tech Stack

Backend: Django (Python) 🐍

Frontend: HTML + CSS 🎨

Database: SQLite (default, easily replaceable with PostgreSQL/MySQL)

Authentication: Custom User Model with Role-Based Access Control

📂 Project Structure
```MySite2/              # Django project config
├── manage.py
├── MySite2/          # Core project settings (urls, wsgi, asgi, settings)
└── MySiteApp/        # Main app
    ├── models.py     # Database models
    ├── views.py      # Views (dashboards, CRUD, auth, tracker)
    ├── forms.py      # Registration, login, project, task forms
    ├── urls.py       # Routes
    ├── templates/    # HTML templates
    └── static/       # CSS & assets
```
⚙️ Installation & Setup
1️⃣ Clone Repository
```
git clone https://github.com/yourusername/MySite2.git
cd MySite2
```
2️⃣ Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
4️⃣ Apply Migrations
```
python manage.py migrate
```
5️⃣ Create Superuser
```
python manage.py createsuperuser
```
6️⃣ Run Server
```
python manage.py runserver
```
🔑 User Roles

👨‍🎓 Student

- View assigned projects & tasks

-  resources for mentors

- Track progress

👨‍🏫 Mentor

- Supervise student projects

- Share resources with students

- View deadlines & progress reports

🛡️ Admin

- Full system control

- Manage users, projects, and resources

📝 License

📜 This project is licensed under the MIT License – free to use and modify.
