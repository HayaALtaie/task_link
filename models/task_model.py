#models/task_model

from sqlalchemy import desc, func
from datetime import datetime
from . import db  # تأكد من أن db تم استيراده بشكل صحيح

class Task(db.Model):
    __tablename__ = 'tasks'  # اسم الجدول في قاعدة البيانات

    # تعريف الأعمدة
    id = db.Column(db.Integer, primary_key=True)  # العمود الأساسي (primary key)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    assigned_to = db.Column(db.String(120))
    status = db.Column(db.String(50))
    created_by = db.Column(db.String(120))
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # الدوال الخاصة بالـ Model
    def __init__(self, title, description, assigned_to, status, created_by, due_date=None):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.status = status
        self.created_by = created_by
        self.due_date = due_date

    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"

    @staticmethod
    def create_new_task(title, description, assigned_to, status, created_by, due_date=None):
        try:
            new_task = Task(
                title=title,
                description=description,
                assigned_to=assigned_to,
                status=status,
                created_by=created_by,
                due_date=due_date
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task
        except Exception as e:
            db.session.rollback()
            print(f"Error creating task: {e}")
            return None

    @staticmethod
    def get_tasks_for_user(user_email):
        return Task.query.filter_by(assigned_to=user_email).all()

    @staticmethod
    def get_all_tasks():
        return Task.query.all()

    @staticmethod
    def get_due_tasks():
        return Task.query.filter(Task.due_date < datetime.utcnow(), Task.status != 'completed').all()

    @staticmethod
    def get_task_by_id(task_id):
        return Task.query.get(task_id)

    @staticmethod
    def update_task_status(task_id, new_status):
        task = Task.get_task_by_id(task_id)
        if task:
            setattr(task, 'status', new_status)
            db.session.commit()
            return task
        return None

    @staticmethod
    def update_task_assignee(task_id, new_assignee):
        """
        تحديث الشخص المكلف بالمهمة
        """
        task = Task.get_task_by_id(task_id)
        if task:
            setattr(task, 'assigned_to', new_assignee)
            db.session.commit()
            return task
        return None

    @staticmethod
    def delete_task(task_id):
        """
        حذف المهمة من قاعدة البيانات
        """
        task = Task.get_task_by_id(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_task(task_id, **kwargs):
        task = Task.get_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            db.session.commit()
            return task
        return None

    @staticmethod
    def get_completed_tasks_count():
        return Task.query.filter_by(status='Completed').count()

    @staticmethod
    def get_overdue_tasks_count():
        return Task.query.filter(Task.due_date < datetime.now(), Task.status != 'Completed').count()

    @staticmethod
    def get_user_performance(user_email):
        user_tasks = Task.query.filter_by(assigned_to=user_email)
        total_tasks = user_tasks.count()
        completed_tasks = user_tasks.filter_by(status='Completed').count()
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        }

    @staticmethod
    def get_top_performers(limit=5):
        # Calculate completion rate for each user
        subquery = db.session.query(
            Task.assigned_to,
            func.count(Task.id).label('total_tasks'),
            func.sum(Task.status == 'Completed').label('completed_tasks')
        ).group_by(Task.assigned_to).subquery()

        # Calculate completion rate and sort by it
        top_performers = db.session.query(
            subquery.c.assigned_to,
            (subquery.c.completed_tasks / subquery.c.total_tasks).label('completion_rate')
        ).order_by(desc('completion_rate')).limit(limit).all()

        return top_performers