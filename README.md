# 🏫 Chinobaka Secondary School Website

A web application and official portal for **Chinobaka Secondary School**, a Zion Christian Church (ZCC) institution offering O-Level and A-Level education alongside boarding facilities in Chikanga, Mutare (Manicaland, Zimbabwe).

## 📌 Project Overview

This project provides a modern, responsive web portal designed to serve prospective parents, current students, staff, and church stakeholders. It highlights the school's academic pathways, ZCC Christian values, boarding life, and streamlined online admissions.

## ✨ Key Features

- **🎓 Academic Programs Display:** Detailed subject streams for both **O-Level** (Core, Technical, Commercials) and **A-Level** (Sciences, Commercials, Arts).
- **🏡 Boarding & Student Life:** Comprehensive info on hostel infrastructure, daily schedules, sports, and ZCC spiritual devotions.
- **📝 Online Admissions Portal:** Interactive application form for Form 1 and Lower 6 candidates (Day & Boarding).
- **📄 Download Center:** Direct access to PDF fee schedules, term calendars, uniform specifications, and boarding checklists.
- **🛡 Secure Backend & Database:** Python backend with parameterized SQL queries to handle admissions data safely and prevent SQL Injection attacks.

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (Jinja2 Templates)
- **Backend:** Python 3.x (Flask / FastAPI)
- **Database:** MySQL (via `mysql-connector-python` / SQLAlchemy ORM)
- **Environment:** Python Virtual Environment (`venv`)

## 📂 Directory Structure

```text
chinobaka-school/
├── app/
│   ├── static/          # CSS, JS, and image assets
│   ├── templates/       # HTML templates (Jinja2)
│   ├── routes.py        # Application routes & API endpoints
│   ├── database.py      # Database connection & queries
│   └── models.py        # Data models
├── uploads/             # Submitted application attachments
├── app.py               # Application entry point
├── requirements.txt     # Python dependencies
└── README.md
