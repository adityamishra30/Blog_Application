# Discover — Minimalist Premium Publishing Platform

**Discover** is a production-ready, minimalist publishing platform built with **Django** and styled with **Tailwind CSS**. Inspired by leading modern editorial platforms like *Medium*, *Notion*, *Hashnode*, and *GitHub*, Discover provides a distraction-free environment for writers and readers with high-performance, dynamic backend capabilities.

---

## 🎨 Official Design System & Reference UI

The application UI faithfully adheres to the official minimalist Discover Editorial design language:

### 1. Home Editorial Feed Design
![Discover Home Feed Design Reference](assets/design_references/ref_home_feed.png)

---

### 2. Story Editor & Publisher Design
![Discover Story Editor Design Reference](assets/design_references/ref_create_post.png)

---

### 3. User Profile & Published Works Design
![Discover User Profile Design Reference](assets/design_references/ref_profile.png)

---

### 4. Search & Topic Exploration Design
![Discover Search & Explore Design Reference](assets/design_references/ref_explore.png)

---

### 5. Profile Customization & Bio Design
![Discover Edit Profile Design Reference](assets/design_references/ref_edit_profile.png)

---

## 📸 Live Application Implementation Screenshots

### 1. Home Feed (Backend Live Data)
A clean single-hero & 3-column grid highlighting published stories, author details, dates, and cover imagery.

![Home Editorial Feed Live](assets/screenshots/home_feed.png)

---

### 2. Distraction-Free Story Creator
Focus-first story creator with cover image uploader, title input, story content area, and working action buttons for **Publishing** or **Saving as Draft**.

![Distraction-Free Story Editor Live](assets/screenshots/create_post.png)

---

### 3. User Profile & Account Logout
Clean personal space displaying user statistics, published articles, saved drafts, edit profile actions, and account logout.

![User Profile Live](assets/screenshots/profile_page.png)

---

### 4. Search & Exploration Engine
Real-time keyword search filtering through story titles and content with zero duplicate cards.

![Search & Explore Live](assets/screenshots/search_page.png)

---

### 5. Profile Customization Page
Minimalist avatar uploader, live bio character counter (250 max limit), and profile metadata manager.

![Edit Profile Live](assets/screenshots/edit_profile.png)

---

## ✨ Key Features

- **Distraction-Free Writing Interface**: Clean cover image dropzone, title field, and content area with direct **Publish** or **Save as Draft** controls.
- **Editorial Home Feed**: Hero post highlight and 3-column recent stories grid synced with Django database models.
- **User Authentication & Auto-Login**: Instant account registration with automatic session authentication that redirects straight to the home feed.
- **Profile & Bio Customization**: Custom profile avatar upload, bio character limit enforcement, and draft management.
- **Draft Posts Management**: Dedicated `/drafts/` page allowing writers to review, preview, and publish draft stories.
- **Search Engine**: Real-time Django queryset filtering across published titles and story contents.

---

## 🛠️ Technology Stack

- **Backend Framework**: Python 3.x, Django 5.x
- **Frontend & Styling**: Tailwind CSS v4, HTML5, Vanilla JavaScript
- **Database**: SQLite3
- **Image Processing**: Pillow (Django `ImageField`)
- **Icons**: Heroicons (SVG)

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.10+ and Node.js installed on your system.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/adityamishra30/Blog_Application.git
   cd Blog_Application
   ```

2. **Set Up Python Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run Database Migrations**
   ```bash
   cd django_blog
   python manage.py migrate
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

---

## 📁 Repository Structure

```text
Blog_App/
├── assets/
│   ├── design_references/   # Official Reference Design Mockups
│   └── screenshots/         # Live Application Screenshots
├── django_blog/
│   ├── blog/
│   │   ├── migrations/      # Database Migration Files
│   │   ├── static/          # Compiled Tailwind CSS Output
│   │   ├── templates/blog/  # Django HTML Templates
│   │   ├── admin.py         # Django Admin Configuration
│   │   ├── forms.py         # ModelForms (BlogForm, ProfileForm)
│   │   ├── models.py        # Blog & Profile Database Models
│   │   ├── signals.py       # Automatic Profile Creation Signals
│   │   ├── urls.py          # App URL Routing
│   │   └── views.py         # App Views & Controller Logic
│   └── django_blog/         # Core Project Settings
└── README.md
```

---

## 📄 License
This project is licensed under the MIT License — free for personal and commercial use.
