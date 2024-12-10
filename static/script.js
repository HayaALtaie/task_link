// script.js

function toggleTheme() {
    const body = document.body;
    const currentTheme = body.classList.contains('bg-dark') ? 'dark' : 'light';

    if (currentTheme === 'light') {
        body.classList.add('bg-dark');
        document.getElementById('theme-toggle').textContent = '🌞'; // Change button to sun icon
    } else {
        body.classList.remove('bg-dark');
        document.getElementById('theme-toggle').textContent = '🌙'; // Change button to moon icon
    }
}

const notificationIcon = document.getElementById('notification-icon');
const notificationBadge = document.getElementById('notification-badge');
const notificationList = document.getElementById('notification-list');

function checkNotifications() {
  fetch('/api/notifications')
    .then(response => response.json())
    .then(data => {
        console.log(data.notifications)
      if (data.notifications.length > 0) {
        // تغيير لون أيقونة الجرس
        notificationIcon.style.color = 'red';

        // تحديث شارة الإشعارات
        notificationBadge.textContent = data.notifications.length;
        notificationBadge.style.display = 'block';

        // عرض الإشعارات في القائمة المنسدلة
        const notificationListUl = notificationList.querySelector('ul');
        notificationListUl.innerHTML = ''; // مسح القائمة الحالية

        // Adding a clear all button inside the list
        const clearAllButton = document.createElement('button');
        clearAllButton.textContent = 'مسح الكل';
        clearAllButton.classList.add('btn', 'btn-sm', 'btn-outline-danger', 'mt-2');
        clearAllButton.addEventListener('click', () => {
          fetch('/api/notifications/clear-all', { method: 'POST' })
            .then(() => {
              // تحديث قائمة الإشعارات بعد مسحها
              checkNotifications();
            });
        });

        data.notifications.forEach(notification => {
          const listItem = document.createElement('li');
          listItem.classList.add('list-group-item');
          listItem.textContent = notification.message;

          // إضافة معالج حدث للنقر على الإشعار
          listItem.addEventListener('click', () => {
            fetch(`/api/notifications/mark-as-read/${notification.id}`, { method: 'POST' })
              .then(() => {
                // تحديث قائمة الإشعارات بعد وضع علامة على الإشعار كمقروء
                checkNotifications();
              });
          });

          notificationListUl.appendChild(listItem);
        });

        // Add the 'clear all' button at the end of the list
        notificationListUl.appendChild(clearAllButton);
      } else {
        notificationIcon.style.color = ''; // Reset color
        notificationBadge.style.display = 'none';
        notificationList.style.display = 'none'; // Hide the notification list when there are no notifications
      }
    });
}

notificationIcon.addEventListener('click', () => {
  if (notificationList.style.display === 'none') {
    notificationList.style.display = 'block';
  } else {
    notificationList.style.display = 'none';
  }
});

// استدعاء الدالة كل 10 ثوانٍ
setInterval(checkNotifications, 10000);

notificationIcon.addEventListener('click', () => {
  if (notificationList.style.display === 'none') {
    notificationList.style.display = 'block';
  } else {
    notificationList.style.display = 'none';
  }
});

// إضافة زر لمسح جميع الإشعارات
const clearAllButton = document.createElement('button');
clearAllButton.textContent = 'مسح الكل';
clearAllButton.classList.add('btn', 'btn-sm', 'btn-outline-danger', 'mt-2');
clearAllButton.addEventListener('click', () => {
  fetch('/api/notifications/clear-all', { method: 'POST' })
    .then(() => {
      // تحديث قائمة الإشعارات بعد مسحها
      checkNotifications();
    });
});
notificationList.appendChild(clearAllButton);

// استدعاء الدالة كل 10 ثوانٍ
setInterval(checkNotifications, 10000);