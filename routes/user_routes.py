#user_routes

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user_model import User
from werkzeug.security import generate_password_hash
from helper import admin_required
from models import db

user_bp = Blueprint('user', __name__)

# مسار لإضافة مستخدم جديد
@user_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            flash('البريد الإلكتروني موجود بالفعل', 'danger')
            return redirect(url_for('user.add_user'))

        try:
            # تشفير كلمة المرور قبل إنشاء المستخدم
            hashed_password = generate_password_hash(password, method='sha256')
            User.create_user(email, hashed_password, name, role)  # استخدام كلمة المرور المشفرة
            flash('تم إضافة المستخدم بنجاح', 'success')
            return redirect(url_for('admin.manage_users'))
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            flash('حدث خطأ أثناء إضافة المستخدم', 'danger')
            return redirect(url_for('user.add_user'))

    return render_template('add_user.html')

# مسار لتعديل بيانات مستخدم
@user_bp.route('/edit_user/<email>', methods=['GET', 'POST'])
@admin_required
def edit_user(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('المستخدم غير موجود', 'danger')
        return redirect(url_for('admin.manage_users'))

    if request.method == 'POST':
        try:
            user.name = request.form.get('name')
            user.email = request.form.get('email')
            user.role = request.form.get('role')
            db.session.commit()
            flash('تم تعديل بيانات المستخدم بنجاح', 'success')
            return redirect(url_for('admin.manage_users'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            flash('حدث خطأ أثناء تعديل بيانات المستخدم', 'danger')
            return redirect(url_for('user.edit_user', email=email))

    return render_template('edit_user.html', user=user)

# مسار لحذف مستخدم
@user_bp.route('/delete_user/<email>', methods=['GET', 'POST'])
@admin_required
def delete_user(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('المستخدم غير موجود', 'danger')
        return redirect(url_for('admin.manage_users'))

    if request.method == 'POST':
        try:
            db.session.delete(user)
            db.session.commit()
            flash('تم حذف المستخدم بنجاح', 'success')
            return redirect(url_for('admin.manage_users'))
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            flash('حدث خطأ أثناء حذف المستخدم', 'danger')
            return redirect(url_for('user.delete_user', email=email))

    return render_template('delete_user.html', user=user)

