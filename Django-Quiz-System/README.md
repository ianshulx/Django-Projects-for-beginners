# Simple Quiz System

A super simple Django quiz app - **no login required!** Just create quizzes in admin and take them.

## ⚡ Quick Setup

```bash
# If venv already exists, just run:
venv/bin/python manage.py createsuperuser
venv/bin/python manage.py runserver

# If fresh setup:
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🎯 How to Use

1. **Go to Admin**: `http://127.0.0.1:8000/admin/` (login with your superuser)
2. **Create a Quiz**: 
   - Click "Quizzes" → "Add Quiz" 
   - Add title and description
   - Add questions inline (or create separately)
   - For each question, add 4 choices and mark one as correct ✓
3. **Take Quiz**: Visit `http://127.0.0.1:8000/` 
4. **See Score**: Submit to see your results!

## ✨ Features

- ✅ Home page showing all quizzes
- ✅ Quiz page with all questions at once
- ✅ Result page with score percentage
- ✅ Admin panel with inline editing
- ✅ **No login/registration needed** - anyone can take quizzes!
- ✅ Clean, minimal UI

## 📁 Project Files (Only 17 files!)

```
├── manage.py              # Django CLI
├── config/                # Settings (3 files)
├── quiz/                  # Main app (6 files)
│   ├── models.py          # 3 models: Quiz, Question, Choice
│   ├── views.py           # 2 views: home, quiz_detail
│   └── admin.py           # Admin config with inlines
├── templates/             # 3 HTML templates
│   ├── home.html          # Quiz list
│   ├── quiz.html          # Take quiz
│   └── result.html        # Show score
└── static/style.css       # Simple CSS (~100 lines)
```

## 💡 Super Simple Code

- **Models**: Just 3 models (25 lines)
- **Views**: 2 functions (25 lines)  
- **Admin**: Inline editing (15 lines)
- **Templates**: 3 simple HTML files
- **CSS**: One file, clean styling

No complicated auth, no user tracking, no database clutter!

## 🎓 Perfect For

- Learning Django basics
- Quick quizzes/polls
- Classroom use
- Simple testing

That's it! **Keep it simple!** 🎉
