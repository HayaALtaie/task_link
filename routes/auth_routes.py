#auth_routes


from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.user_model import User  # استيراد نموذج المستخدم

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if User.query.filter_by(email=email).first():
            return "البريد الإلكتروني موجود مسبقاً", 400

        # تشفير كلمة المرور باستخدام generate_password_hash
        hashed_password = generate_password_hash(password, method='sha256')  
        
        role = 'admin'
        new_user = User.create_user(email, hashed_password, name, role)
        login_user(new_user)

        # تسجيل الدخول تلقائياً
        session['user'] = email
        session['role'] = role

        # التوجيه إلى لوحة تحكم الإدمن
        return redirect(url_for('auth.login'))  # التوجيه إلى لوحة تحكم الإدمن

    return render_template('register_admin.html')  # عرض صفحة التسجيل للإدمن فقط


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # تسجيل دخول المستخدم باستخدام flask_login
            
            # توجيه المستخدم إلى لوحة التحكم بناءً على الدور
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))  # لوحة تحكم الإدمن
            else:
                return redirect(url_for('dashboard.user_dashboard'))  # لوحة تحكم المستخدم العادي
        else:
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')  # استخدام flash لعرض رسائل الخطأ

    return render_template('login.html')






@auth_bp.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        # تأكد من أن البريد الإلكتروني غير مكرر
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            abort(400, description="البريد الإلكتروني موجود بالفعل")  # إرجاع خطأ إذا كان البريد موجودًا


        # إضافة المستخدم إلى قاعدة البيانات
        user = User.create_user(email, password, name, 'user')
        login_user(user)

        # تسجيل الدخول مباشرة بعد التسجيل
        session['user'] = user.email
        session['role'] = user.role

        # إعادة التوجيه إلى صفحة تسجيل الدخول بعد التسجيل بنجاح
        return redirect(url_for('auth.login'))

    return render_template('register_user.html')  # عرض نموذج التسجيل

@auth_bp.route('/logout')
@login_required  # إضافة login_required
def logout():
    logout_user()  # استخدام logout_user() من flask_login
    return redirect(url_for('auth.login'))
