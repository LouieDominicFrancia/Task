# 📝 Task Manager Web App (Django)

This is a simple Task Manager web application built with **Django**. It allows users to add, update, delete, and filter tasks based on status, priority, and due date.
---

## 🚀 Features

- ✅ Add, update, and delete tasks
- ✅ Mark tasks as completed or pending
- ✅ Filter by status, priority, and due date
- ✅ Input validation and error handling
- ✅ Fully persistent using a database backend

---

1. Clone the repository


git clone https://github.com/your-username/task-manager.git
cd task-manager

2. Create and activate a virtual environment

   
python -m venv env
source env/bin/activate       # On Linux/macOS
env\Scripts\activate          # On Windows

3. Install dependencies


pip install -r requirements.txt

4. Apply database migrations


python manage.py migrate

5. Run the development server


python manage.py runserver





Visit http://127.0.0.1:8000/ in your browser.



To use a different database, update the DATABASES section in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'task_db',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
