#admin-route

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user  # استيراد current_user
from models.user_model import User
from models.task_model import Task
from helper import admin_required

# تعريف Blueprint الخاص بلوحة تحكم الإدمن
admin_bp = Blueprint('admin', __name__)

# المسار لعرض لوحة تحكم الإدمن
@admin_bp.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    # استخدام current_user للتحقق من الدور
    if current_user.role == 'admin':  
        users = User.query.all()
        return render_template('admin_dashboard.html', users=users)
    else:
        return redirect(url_for('auth.login')) 

# إدارة المستخدمين
@admin_bp.route('/manage_users')
@admin_required
def manage_users():
    users = User.query.all()  # استرجاع جميع المستخدمين
    return render_template('manage_users.html', users=users)

# المسار لإدارة المهام
@admin_bp.route('/manage_tasks')
@admin_required
def manage_tasks():
    tasks = Task.get_all_tasks()  # استرجاع جميع المهام من قاعدة البيانات
    return render_template('manage_tasks.html', tasks=tasks)


# المسار لعرض تقرير المهام
@admin_bp.route('/tasks_report')
@admin_required
def tasks_report():
    # جلب البيانات من الدوال في نموذج Task
    completed_tasks = Task.get_completed_tasks_count()  # عدد المهام المكتملة
    overdue_tasks = Task.get_overdue_tasks_count()      # عدد المهام المتأخرة
    top_performers = Task.get_top_performers()          # أفضل المؤدين

    # عرض البيانات في القالب
    return render_template('tasks_report.html',
                           completed_tasks=completed_tasks,
                           overdue_tasks=overdue_tasks,
                           top_performers=top_performers)
