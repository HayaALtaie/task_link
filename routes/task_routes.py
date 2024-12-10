# task_routes.py

# from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# from models.task_model import Task
# from models.user_model import User  # استيراد نموذج المستخدم
# from helper import login_required, admin_required
# from datetime import datetime

# task_bp = Blueprint('task', __name__)

# # صفحة إنشاء المهمة
# @task_bp.route('/create_task', methods=['GET', 'POST'])
# def create_task():
#     if request.method == 'POST':
#         # الحصول على البيانات من النموذج
#         title = request.form.get('title')
#         description = request.form.get('description')
#         assigned_to = request.form.get('assigned_to')
#         created_by = request.form.get('created_by')
#         due_date = request.form.get('due_date')

#         # التحقق من وجود جميع البيانات
#         if not title or not description or not assigned_to or not created_by:
#             return "Missing required fields", 400

#         # تحويل تاريخ الاستحقاق إلى تنسيق تاريخي (اختياري)
#         due_date = datetime.strptime(due_date, '%Y-%m-%d')

#         # إنشاء المهمة باستخدام الدالة create_new_task
#         new_task = Task.create_new_task(
#             title=title,
#             description=description,
#             assigned_to=assigned_to,
#             created_by=created_by,
#             due_date=due_date,
#             status='In Progress'  # يمكنك تخصيص حالة المهمة هنا
#         )

#         # إعادة التوجيه إلى صفحة عرض المهام
#         return redirect(url_for('task.view_all_tasks'))

#     # في حالة استخدام GET، استرجاع جميع المستخدمين لعرضهم في القائمة المنسدلة
#     users = User.query.filter_by(role='user').all() 
#     admins = User.query.filter_by(role='admin').all()  
#     return render_template('create_task.html', users=users ,admins=admins)




# # عرض المهام الخاصة بالمستخدم
# @task_bp.route('/my_tasks')
# @login_required
# def view_my_tasks():
#     user_email = session['user']
#     tasks = Task.get_tasks_for_user(user_email)
#     return render_template('user_tasks.html', tasks=tasks)


# # عرض المهام التي اقترب موعد استحقاقها
# @task_bp.route('/due_tasks')
# @admin_required
# def view_due_tasks():
#     due_tasks = Task.get_due_tasks()
#     return render_template('due_tasks.html', tasks=due_tasks)


# # عرض جميع المهام
# @task_bp.route('/all_tasks')
# def view_all_tasks():
#     tasks = Task.get_all_tasks()
#     return render_template('all_tasks.html', tasks=tasks)


# # تحديث حالة المهمة
# @task_bp.route('/update_task_status/<int:task_id>', methods=['GET', 'POST'])
# @admin_required
# def update_task_status_route(task_id):
#     task = Task.get_task_by_id(task_id)
#     if not task:
#         flash('المهمة غير موجودة', 'danger')
#         return redirect(url_for('task.view_all_tasks'))

#     if request.method == 'POST':
#         new_status = request.form['status']
#         if new_status not in ['In Progress', 'Completed', 'Pending']:  # تحقق من الحالات الصالحة
#             flash('الحالة غير صالحة', 'danger')
#             return redirect(url_for('task.update_task_status_route', task_id=task_id))
        
#         Task.update_task_status(task_id, new_status)
#         flash('تم تحديث حالة المهمة بنجاح', 'success')
#         return redirect(url_for('task.view_all_tasks'))

#     return render_template('update_task_status.html', task=task)


# # تحديث المكلف بالمهمة
# @task_bp.route('/tasks/update_assignee/<int:task_id>', methods=['POST'])
# @admin_required
# def update_task_assignee(task_id):
#     new_assignee = request.form.get('assigned_to')
#     task = Task.update_task_assignee(task_id, new_assignee)
#     if task:
#         flash('تم تحديث المكلف بنجاح', 'success')
#         return redirect(url_for('task.view_all_tasks'))
#     flash('المهمة غير موجودة', 'danger')
#     return redirect(url_for('task.all_tasks'))


# # حذف المهمة
# @task_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
# @admin_required
# def delete_task(task_id):
#     task = Task.get_task_by_id(task_id)
#     if task:
#         Task.delete_task(task_id)
#         flash('تم حذف المهمة بنجاح', 'success')
#         return redirect(url_for('task.all_tasks'))
#     flash('المهمة غير موجودة', 'danger')
#     return redirect(url_for('task.all_tasks'))


from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.task_model import Task
from models.user_model import User
from datetime import datetime
from helper import login_required, admin_required
from models import db
from models.notification_model import Notification

task_bp = Blueprint('task', __name__)

# صفحة إنشاء المهمة
@task_bp.route('/create_task', methods=['GET', 'POST'])
@admin_required  # يمكن إضافة حماية بحيث يمكن للمسؤولين فقط إضافة مهام
def create_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')
        created_by = request.form.get('created_by')
        due_date_str = request.form.get('due_date')  # تغيير اسم المتغير لتجنب تضارب الأسماء

        # التحقق من وجود جميع البيانات
        if not all([title, description, assigned_to, created_by, due_date_str]):  # استخدام all للتحقق من صحة جميع المتغيرات
            flash('الرجاء ملء جميع الحقول', 'danger')
            return redirect(url_for('task.create_task'))

        try:
            # تحويل تاريخ الاستحقاق من نص إلى كائن datetime
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('تنسيق تاريخ الاستحقاق غير صحيح. يجب أن يكون بتنسيق YYYY-MM-DD.', 'danger')
            return redirect(url_for('task.create_task'))

        # إنشاء المهمة باستخدام الدالة create_new_task
        try:
            new_task = Task.create_new_task(
                title=title,
                description=description,
                assigned_to=assigned_to,
                created_by=created_by,
                due_date=due_date,
                status='In Progress'
            )
            notification = Notification(
            user_email=new_task.assigned_to, 
            message=f'تم تخصيص مهمة جديدة لك: {new_task.title}'
        )
            db.session.add(notification)
            db.session.commit()

            flash('تم إنشاء المهمة بنجاح', 'success')
            return redirect(url_for('task.view_all_tasks'))
        except Exception as e:
            db.session.rollback()
            print(f"Error creating task: {e}")
            flash('حدث خطأ أثناء إنشاء المهمة', 'danger')
            return redirect(url_for('task.create_task'))
            
    users = User.query.filter_by(role='user').all()
    admins = User.query.filter_by(role='admin').all()
  
    return render_template('create_task.html', users=users, admins=admins)

# عرض المهام الخاصة بالمستخدم
@task_bp.route('/my_tasks')
@login_required
def view_my_tasks():
    user_email = session['user']
    tasks = Task.get_tasks_for_user(user_email)
    return render_template('user_tasks.html', tasks=tasks)

# عرض جميع المهام
@task_bp.route('/all_tasks')
@admin_required
def view_all_tasks():
    tasks = Task.get_all_tasks()
    return render_template('all_tasks.html', tasks=tasks)

# تحديث حالة المهمة
@task_bp.route('/update_task_status/<int:task_id>', methods=['GET', 'POST'])
@admin_required
def update_task_status_route(task_id):
    task = Task.get_task_by_id(task_id)
    if not task:
        flash('المهمة غير موجودة', 'danger')
        return redirect(url_for('task.view_all_tasks'))

    if request.method == 'POST':
        new_status = request.form['status']
        valid_statuses = ['In Progress', 'Completed', 'Pending']  # تعريف قائمة بالحالات الصالحة
        if new_status not in valid_statuses:
            flash('الحالة غير صالحة', 'danger')
            return redirect(url_for('task.update_task_status_route', task_id=task_id))

        try:
            Task.update_task_status(task_id, new_status)
            flash('تم تحديث حالة المهمة بنجاح', 'success')
            return redirect(url_for('task.view_all_tasks'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating task status: {e}")
            flash('حدث خطأ أثناء تحديث حالة المهمة', 'danger')
            return redirect(url_for('task.update_task_status_route', task_id=task_id))

    return render_template('update_task_status.html', task=task)

# حذف المهمة
@task_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
@admin_required
def delete_task(task_id):
    try:
        if Task.delete_task(task_id):  # استخدام قيمة الإرجاع من delete_task للتحقق من نجاح العملية
            flash('تم حذف المهمة بنجاح', 'success')
        else:
            flash('المهمة غير موجودة', 'danger')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting task: {e}")
        flash('حدث خطأ أثناء حذف المهمة', 'danger')
    return redirect(url_for('task.view_all_tasks'))


# تعديل مهمة
@task_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@admin_required
def edit_task(task_id):
    task = Task.get_task_by_id(task_id)
    if not task:
        flash('المهمة غير موجودة', 'danger')
        return redirect(url_for('task.view_all_tasks'))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.assigned_to = request.form.get('assigned_to')

        # تحويل due_date من string إلى datetime.date
        due_date_str = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

        db.session.commit()  # حفظ التغييرات في قاعدة البيانات
        flash('تم تعديل المهمة بنجاح', 'success')
        return redirect(url_for('task.view_all_tasks'))

    # إذا كانت طريقة الطلب GET، اعرض نموذج تعديل المهمة
    return render_template('edit_task.html', task=task)


@task_bp.route('/user_tasks/<user_email>')
@login_required
def view_user_tasks(user_email):
    # الحصول على المهام المرتبطة بالمستخدم
    tasks = Task.query.filter_by(assigned_to=user_email).all()  # استرجاع المهام التي تم تعيينها للمستخدم
    return render_template('user_tasks.html', tasks=tasks)



@task_bp.route('/task/view_task/<int:task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('view_task.html', task=task)


# @task_bp.route('/reports')
# @admin_required
# def reports():
#     completed_tasks = Task.get_completed_tasks_count()
#     overdue_tasks = Task.get_overdue_tasks_count()
#     top_performers = Task.get_top_performers()

#     return render_template('reports.html',
#                            completed_tasks=completed_tasks,
#                            overdue_tasks=overdue_tasks,
#                            top_performers=top_performers)