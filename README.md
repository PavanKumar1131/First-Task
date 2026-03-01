# Productivity Tracker - Web Application

A complete task management and productivity tracking web application built with Flask, SQLite, and vanilla JavaScript. This project allows users to manage tasks, track time, analyze productivity through charts, and export reports.

## 📋 Project Overview

This productivity tracker helps users:
- Create and manage tasks with categories
- Track time spent on each task
- View productivity analytics through interactive charts
- Export data as CSV or PDF reports

Built as an internship project demonstrating full-stack web development skills.

## 🏗️ Architecture

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **SQLite** - Lightweight database

### Frontend'
- **HTML5** - Semantic markup
- **CSS3** - Custom styles with Flexbox & Grid
- **JavaScript ES6** - Timer functionality and interactivity
- **Chart.js** - Data visualization
- **jsPDF** - Client-side PDF generation

## 📁 Folder Structure

```
productivity_tracker/
├── app.py              # Main Flask application
├── models.py           # Database models (User, Task)
├── auth.py             # Authentication routes
├── tasks.py            # Task management routes
├── static/
│   ├── css/
│   │   └── style.css   # All custom styles
│   └── js/
│       ├── timer.js    # Task timer functionality
│       └── charts.js   # Chart rendering
├── templates/
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── dashboard.html  # Main dashboard with charts
│   └── tasks.html      # Task list and management
├── exports/            # Export files directory
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/productivity-tracker.git
   cd productivity-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional for development)
   ```bash
   # Create .env file
   echo SECRET_KEY=your-secret-key-here > .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🌐 Deployment on Render

### Steps to Deploy

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_URL
   git push -u origin main
   ```

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure settings:
     - **Name**: productivity-tracker
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

4. **Set Environment Variables**
   - Add `SECRET_KEY` with a secure random string
   - Add `FLASK_DEBUG` = `False`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### Environment Variables for Production

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Random string for session security |
| FLASK_DEBUG | Set to False in production |
| DATABASE_URL | Database connection (optional) |

## ✨ Features

### User Authentication
- Secure registration with password hashing
- Login with remember me option
- Protected routes require authentication

### Task Management
- Add tasks with title, description, category
- Edit and delete tasks
- Mark tasks as completed/pending
- Categories: Work, Study, Personal, Health, Other

### Time Tracking
- Start/pause timer for each task
- Auto-save on timer pause
- Time displayed in HH:MM:SS format
- Tracks total time across all tasks

### Analytics Dashboard
- Weekly completed tasks bar chart
- Time spent per category doughnut chart
- Task status pie chart (completed vs pending)
- Summary statistics cards

### Export Options
- CSV export of all tasks (server-side with pandas)
- PDF productivity report (client-side with jsPDF)



## 🛠️ Technologies Used

- Python 3.8+
- Flask 2.3.3
- Flask-Login 0.6.2
- Flask-SQLAlchemy 3.0.5
- pandas 2.0.3
- Chart.js (CDN)
- jsPDF (CDN)

