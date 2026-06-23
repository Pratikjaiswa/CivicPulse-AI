# 🚀 CivicPulse AI

An AI-powered Civic Complaint Management System built using **Python, Flask, Machine Learning, and MySQL**.

CivicPulse AI automatically classifies citizen complaints, assigns priorities, enables department and officer tracking, provides an administrative dashboard, and generates analytics for complaint management.

---

## 📌 Project Overview

CivicPulse AI is an end-to-end web application designed to demonstrate the practical implementation of Machine Learning in a real-world civic complaint management workflow.

The system allows citizens to submit complaints, automatically predicts the complaint category using an NLP-based Machine Learning model, stores complaint records in a MySQL database, and provides dashboards for tracking and analytics.

This project was developed as a portfolio project for AI/ML and Data Analytics applications.

---

## ✨ Features

- 🤖 AI-powered complaint classification
- 📝 Online complaint submission
- 🗂 Automatic category prediction using NLP
- ⚡ Priority assignment
- 🏢 Department allocation
- 👮 Officer assignment and tracking
- 📊 Analytics dashboard with visual reports
- 📈 Complaint status monitoring
- 📱 Responsive modern UI
- 💾 MySQL database integration

---

## 🛠 Technology Stack

| Category | Technologies |
|-----------------|--------------------------------|
| Programming | Python 3 |
| Backend | Flask |
| Machine Learning | Scikit-learn |
| NLP | TF-IDF Vectorization |
| Database | MySQL |
| Frontend | HTML5, CSS3 |
| Visualization | Chart.js |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```
CivicPulse-AI/
│
├── APPS/
│   ├── app.py
│   ├── static/
│   └── templates/
│
├── DATA/
│   └── RAW DATA/
│
├── DATA BASE/
│   └── sql code.sql
│
├── MODELS/
│   ├── complaint_classifier.pkl
│   └── vectorizer.pkl
│
├── NOTEBOOK/
│   └── complaint_model_v2.ipynb
│
├── generate_dataset.py
├── requirements.txt
└── README.md
```

---

## ⚙️ System Workflow

```
Citizen Complaint
        │
        ▼
Flask Application
        │
        ▼
TF-IDF Vectorizer
        │
        ▼
Machine Learning Model
        │
        ▼
Predicted Category
        │
        ▼
Priority Assignment
        │
        ▼
Department & Officer Assignment
        │
        ▼
MySQL Database
        │
        ▼
Dashboard & Analytics
```

---

## 📊 Complaint Categories

The AI model classifies complaints into multiple civic categories including:

- Road Damage
- Garbage Management
- Water Leakage
- Traffic Issues
- Street Light Problems
- Drainage Issues
- Public Cleanliness
- Illegal Parking
- Noise Complaints
- Civic Infrastructure

---

## 📈 Analytics Dashboard

The project includes visual dashboards for:

- Complaint Distribution
- Category-wise Analysis
- Status Distribution
- Priority Distribution
- Department-wise Complaints
- Officer-wise Complaints

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CivicPulse-AI.git
```

Navigate to the project

```bash
cd CivicPulse-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure MySQL database and update connection details inside `app.py`.

Run the Flask application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## 🔮 Future Enhancements

- Google Maps integration
- Email & SMS notifications
- Real-time complaint updates
- Admin authentication
- Image-based complaint classification
- Deep Learning model integration
- Deployment on Render/AWS

---

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Machine Learning
- Natural Language Processing
- Flask Web Development
- MySQL Database Integration
- Dashboard Design
- CRUD Operations
- Data Visualization
- End-to-End AI Application Development

---

## ⚠️ Disclaimer

This project is developed for educational and portfolio demonstration purposes. It is not intended to replace official government civic complaint or emergency response systems.

---

## 👨‍💻 Author

**Pratik Jaiswal**

AI • Machine Learning • Data Analytics • Python • Flask • MySQL

GitHub: https://github.com/Pratikjaiswa

---

### ⭐ If you found this project useful, consider giving it a star.
