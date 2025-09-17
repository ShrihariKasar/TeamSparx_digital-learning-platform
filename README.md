# 📚 Digital Learning Platform  
> A Flask-based localized education system with content delivery, quizzes, community forums, and teacher dashboards.

[![Flask](https://img.shields.io/badge/Flask-2.0%2B-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Heroku-purple.svg)](https://heroku.com)

---

## ✨ Overview

A modern **Flask-based web application** that provides:

- 📘 **Localized Learning Content**
- 📝 **Interactive Quizzes**
- 👩‍🏫 **Teacher Dashboards**
- 👥 **Community Forums**
- 📊 **Progress Monitoring**
- 🛟 **Support System**

This platform aims to **bridge the digital education divide** by offering offline-first, language-inclusive tools for learners and educators.

---

## 🚀 Features  

- 🎓 **Learning Content** – Structured by subject, grade & language. Works offline.
- 📝 **Interactive Quizzes** – Auto-graded, immediate feedback with analytics.
- 👩‍🏫 **Teacher Dashboard** – Monitor student activity and progress.
- 👥 **Community Learning** – Forums for questions, collaboration, and peer answers.
- 🛠️ **Support System** – Raise tickets, get answers in local languages.
- 📊 **Progress Monitoring** – Graphs, analytics & exportable reports.

---

## 🛠 Tech Stack  

| Layer      | Tools Used                                      |
|------------|-------------------------------------------------|
| **Backend**| Flask (Python), Flask-SQLAlchemy, Flask-Login   |
| **Frontend**| HTML5, CSS3, Bootstrap 5, JS, Jinja2 Templates |
| **Database**| SQLite / PostgreSQL                            |
| **Auth**   | Flask-Login / Flask-JWT (optional)              |
| **Others** | FontAwesome, Flask-Migrate, WTForms             |

---

## 📁 Project Structure  

```

digital-learning-platform/
├── app.py                  # Main Flask app
├── models.py               # SQLAlchemy models
├── templates/              # HTML templates (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── support.html
│   ├── view\_ticket.html
│   ├── features.html
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── requirements.txt        # Dependencies
├── README.md               # You're reading it :)
├── config.py               # Configuration (env/db)
└── migrations/             # Flask-Migrate scripts

````

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShrihariKasar/digital-learning-platform.git
cd digital-learning-platform
````

### 2. Create a virtual environment

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the application

```bash
flask run
```

### 6. Open in browser

```
http://127.0.0.1:5000/
```

---

## 📸 Screenshots

### 🏠 Home / Features

<p align="center">
  <img src="static/images/screenshots/features.png" width="600" alt="Features Page">
</p>

### 👩‍🏫 Teacher Dashboard

<p align="center">
  <img src="static/images/screenshots/dashboard.png" width="600" alt="Teacher Dashboard">
</p>

### 📝 Quiz Interface

<p align="center">
  <img src="static/images/screenshots/quiz.png" width="600" alt="Quiz Page">
</p>

---

## 🚀 Deployment

### Deploy on Heroku / Render / Railway

Configure:

* `Procfile`
* `runtime.txt`
* `requirements.txt`
* `config.py` or `.env`

### Docker (Optional)

```bash
docker build -t digital-learning .
docker run -p 5000:5000 digital-learning
```

---

## 🔒 Environment Variables

Create a `.env` or configure in `config.py`:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///data.db  # or use PostgreSQL URL
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch (`feature/your-feature`)
3. Commit and push your changes
4. Open a Pull Request

---

## 🧪 Testing Tips

* Use Flask debug mode: `export FLASK_DEBUG=1`
* Enable testing database in `.env` if needed
* Use browser console and network tab to debug JS/CSS issues

---

## 📜 License

This project is licensed under the **MIT License**.
Feel free to use, modify, and distribute with attribution.

---

## 👨‍💻 Author

**Shrihari Kasar**
🖥️ Portfolio: [shriharikasarportfolio.netlify.app](https://shriharikasarportfolio.netlify.app)
🐙 GitHub: [@ShrihariKasar](https://github.com/ShrihariKasar)
📫 Email: [shreeharikasar@gamil.com](mailto:shreeharikasar@gamil.com)

---

## 🙌 Acknowledgements

Thanks to the open-source community for resources and inspiration.
Feel free to contribute and make education more accessible for all 🌍
