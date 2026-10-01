# 🏛️ Kyklos — Student Community & Hostel Management Platform

> *Note: This project was originally created when I was in Grade 11, back before I started actively using GitHub and version control. It represents my early journey into full-stack web development with Python & Django. It has now been cleaned up, optimized, and modernized to be fully runnable, efficient, and reproducible.*

---

## 📖 Overview

**Kyklos** is an all-in-one web portal designed to assist high-school and university students with:
- **Hostel Finder & Portal**: Browse collaborative student hostels with verified pricing, ratings, and location details.
- **Warden Maintenance & Complaint Tracking**: Direct complaint submission interface for students to notify wardens of plumbing, electrical, or facility issues (with image attachment support and email alerts).
- **Study Space & Subject Communities**: Dedicated subject study hubs (Physics, Computer Science, Mathematics, Biology) where students can share resources and study guides.
- **Gamified Rewards System**: Students earn credit points by answering academic quizzes and contributing study resources, which can be redeemed for rewards.
- **Discussion Forum**: Community board for asking questions, answering peers, and collaborative learning.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13 / Django 6.1 (with support for SQLite and PostgreSQL)
- **Frontend**: Django Templates, HTML5, CSS3, JavaScript
- **Database**: SQLite (default zero-config) / PostgreSQL (via environment configuration)
- **Authentication**: Custom authentication supporting Django PBKDF2 password hashing with legacy fallback
- **File Handling**: Django Media & Static file pipeline (Pillow)

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Sangam067/Kyklos.git
cd Kyklos
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_data
```

### 5. Launch the Server
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 🔑 Preconfigured Demo Accounts

When seeded via `python manage.py seed_data`, the following test accounts are immediately ready:

| Role | Username | Password | Details |
| :--- | :--- | :--- | :--- |
| **Student** | `demo_student` | `student123` | Pre-loaded with 350 credit score |
| **Warden (Hostel 1)** | `warden_bagbazzar` | `warden123` | Bagbazzar Fancy Hostel |
| **Warden (Hostel 2)** | `warden_maitighar` | `warden123` | Maitighar Hostel |
| **Warden (Hostel 3)** | `warden_boysdream` | `warden123` | Boys Dream Hostel |

---

## 🧪 Running Automated Tests

Kyklos includes a full unit test suite covering authentication, dashboards, discussion forums, rewards, and complaint endpoints:

```bash
python manage.py test
```

---

## 📂 Project Structure

```
Kyklos/
├── kyklos/                 # Project core configuration (settings, root urls, wsgi)
├── main/                   # Main Django application
│   ├── management/commands # Custom CLI commands (seed_data)
│   ├── migrations/         # Database migrations
│   ├── static/             # Images, styles, and static assets
│   ├── templates/          # HTML templates (discussion, hostel, complaint, home, etc.)
│   ├── admin.py            # Custom Django Admin registrations
│   ├── models.py           # Database models (Student, Hostel, Warden, Discussion, Resource, Complaint)
│   ├── tests.py            # Comprehensive test suite
│   ├── urls.py             # Application URL routing
│   └── views.py            # Optimized views and business logic
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── manage.py               # Django management script
├── requirements.txt        # Python dependency manifest
└── README.md               # Documentation
```
