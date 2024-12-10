# #dashboard_routes

from models import db
from flask import Blueprint, render_template, session, redirect, url_for
from models.task_model import Task
from models.user_model import User  # تأكد من استيراد نموذج User
from helper import login_required, admin_required

dashboard_bp = Blueprint('dashboard', __name__)

# @dashboard_bp.route('/admin_dashboard')
# def admin_dashboard():
#     print(f"Session at admin dashboard: {session}")  # تحقق من الجلسة في هذه المرحلة
#     if 'user' in session and session.get('role') == 'admin':  # تحقق من الجلسة بشكل دقيق
#         user_email = session.get('user')  # الحصول على البريد الإلكتروني من الجلسة بشكل صحيح
#         tasks = Task.get_all_tasks()  # دالة لاسترجاع كل المهام
#         users = User.query.all()   # قاعدة بيانات المستخدمين أو دالة للحصول عليهم

#         return render_template('admin_dashboard.html', user_email=user_email, tasks=tasks, users=users)
#     else:
#         return redirect(url_for('auth.login'))  # إعادة التوجيه إلى صفحة تسجيل الدخول إذا لم يكن مستخدم إدمن


# لوحة تحكم المستخدم العادي
@dashboard_bp.route('/user_dashboard')
@login_required  # تأكد من أن المستخدم مسجل دخول
def user_dashboard():
    user_email = session.get('user')
    tasks = Task.get_tasks_for_user(user_email)  # استرجاع المهام الخاصة بالمستخدم
    return render_template('user_dashboard.html', tasks=tasks)  # عرض صفحة لوحة التحكم للمستخدم العادي



