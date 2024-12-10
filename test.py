import unittest
from app import create_app, db
from models import User, Notification
from flask_login import login_user

class TestNotificationsAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """ إعداد التطبيق للاختبارات """
        cls.app = create_app('testing')  # تأكد من أنك تستخدم إعدادات الاختبار
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        
        # إنشاء مستخدم وهمي
        cls.user = User(email='testuser@example.com', password='password123')
        db.session.add(cls.user)
        db.session.commit()
        
        # إنشاء إشعار وهمي
        cls.notification = Notification(message="Test Notification", user_email=cls.user.email, is_read=False)
        db.session.add(cls.notification)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """ تنظيف البيانات بعد انتهاء الاختبارات """
        db.session.remove()
        cls.app_context.pop()

    def test_mark_as_read(self):
        """ اختبار وضع الإشعار كمقروء """
        # تسجيل الدخول للمستخدم
        with self.client:
            login_user(self.user)
            response = self.client.post(f'/api/notifications/mark-as-read/{self.notification.id}')
            
            # تحقق من حالة الاستجابة
            self.assertEqual(response.status_code, 200)
            self.assertIn('تم وضع علامة على الإشعار كمقروء', response.json['message'])

            # التحقق من أن الإشعار قد تم تحديثه
            updated_notification = Notification.query.get(self.notification.id)
            self.assertTrue(updated_notification.is_read)

if __name__ == '__main__':
    unittest.main()
