# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # تهيئة قاعدة البيانات

from .user_model import User  # إضافة هذا السطر لاستيراد User
