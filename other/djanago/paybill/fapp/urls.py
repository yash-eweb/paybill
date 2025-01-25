from django.urls import path
from fapp import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('addbill', views.addbill,name='addbill'),
    path('update/<int:pk>',views.update , name='update'),
    path('delete/<int:pk>',views.delete , name='delete'),
    path('notifications', views.user_notifications ,name='notifications'),
    path('mark/<int:id>', views.mark_notification_as_read ,name='mark'),
    path('notification_status', views.admin_notification ,name='notification_status'),
    # path('admin/send-notifications/', views.admin_send_notifications, name='admin_send_notifications'),

    path('allexpense', views.allexpense ,name='allexpense'),
    path('addexpense', views.addexpense ,name='addexpense'),
    path('exupdate/<int:pk>',views.exupdate , name='exupdate'),
    path('exdelete/<int:pk>',views.exdelete , name='exdelete'),
    path('allop' ,views.allop ,name="allop"),

    # group 
    path('create_group', views.create_group, name="create_group"),
    path('group_detail/<int:id>', views.group_detail, name="group_detail"),
    path('allgroup', views.allgroup, name="allgroup"),
    # path('add_expense', views.add_expense, name="add_expense"),
    path('add_member/<int:id>', views.add_member, name="add_member"),
    path('add_group_expense/<int:id>', views.add_group_expense, name="add_group_expense"),
    path('update_group_name/<int:id>', views.update_group_name ,name="update_group_name"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
