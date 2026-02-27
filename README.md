# 💼 JobPortal — Django Job Portal Web App

A full-stack job portal built with Django, featuring real-time job fetching from Indeed, LinkedIn & Google Jobs via the JSearch API. Dark-themed, mobile responsive UI with user profiles, resume uploads, and admin management.

---
Live Demo: https://job-portal-k062.onrender.com

## 🚀 Features

- 🔐 **User Authentication** — Register, Login, Logout with hashed passwords
- 📊 **Dashboard** — Profile completion tracker, stats, recent jobs
- 👤 **User Profiles** — Mobile, location, qualification, job preferences, work experience
- 📄 **Resume Upload** — PDF/DOC/DOCX upload stored per user
- 💼 **Job Listings** — Filter by category and skill, dynamic dropdown from DB
- 🔍 **Job Detail** — Full job description, similar jobs, apply link
- 📝 **Post a Job** — Staff-only job posting with logo upload
- 🌐 **Real-time Jobs** — Fetch live jobs from Indeed/LinkedIn via JSearch API
- 🛠️ **Admin Panel** — Full job management with logo preview
- 📱 **Mobile Responsive** — Works on all screen sizes

---
---

## 📁 Project Structure

```
jobportal/
├── jobportal/               # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                # Auth + User profiles
│   ├── models.py            # UserProfile model
│   ├── views.py             # register, login, logout, dashboard, profile
│   ├── urls.py
│   └── admin.py
│
├── jobs/                    # Job listings
│   ├── models.py            # Job model
│   ├── views.py             # home, job_list, job_detail, apply, post_job
│   ├── urls.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── fetch_jobs.py  # JSearch API command
│
├── core/                    # Shared/misc
│   └── models.py
│
├── templates/
│   ├── base.html
│   ├── navbar.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── profile.html
│   ├── core/
│   │   └── home.html
│   └── jobs/
│       ├── job_list.html
│       ├── job_detail.html
│       └── post_job.html
│
├── static/
│   └── css/
│       └── style.css
│
└── media/                   # Uploaded files (auto-created)
    ├── logos/               # Job company logos
    └── resumes/             # User resumes
```
## 👨‍💻 Author

Built with ❤️ using Django + JSearch API.  
Feel free to star ⭐ the repo if you found it useful!
