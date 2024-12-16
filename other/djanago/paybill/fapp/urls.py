from django.urls import path
from fapp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('addbill', views.addbill,name='addbill'),

]
