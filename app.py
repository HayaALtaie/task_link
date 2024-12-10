from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.task_routes import task_bp
from routes.user_routes import user_bp
from routes.notification_routes import notification_bp

from models import db, User  # استيراد db و User من models

# تهيئة التطبيق
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # استبدل بمفتاح سري قوي وفريد

# إعدادات الاتصال بقاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite قاعدة البيانات
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # إيقاف تتبع التعديلات

# تهيئة SQLAlchemy
db.init_app(app)

# تهيئة Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # تحديد مسار تسجيل الدخول

@login_manager.user_loader
def load_user(user_id):
    # استخدام email كمعرف للمستخدم
    user = User.query.filter_by(email=user_id).first()  
    return user

# تسجيل الـ Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(task_bp, url_prefix='/task')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(notification_bp, url_prefix='/')

# راوت للصفحة الرئيسية (index)
@app.route('/')
def index():
    return render_template('index.html')  # عرض القالب index.html

# إنشاء الجداول في قاعدة البيانات عند بدء التطبيق لأول مرة
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)