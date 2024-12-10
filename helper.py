#helpers.py

from flask import abort
from flask_login import current_user
from functools import wraps

# ديكوراتور للتحقق إذا كان المستخدم مسجلاً
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:  # استخدام current_user من flask_login
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ديكوراتور للتحقق إذا كان المستخدم هو مدير
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # عرض صفحة خطأ 403
        return f(*args, **kwargs)
    return decorated_function
