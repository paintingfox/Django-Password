from django.urls import path
from Login import views

app_name = 'login_app'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('user_login/', views.user_login, name="user_login"),
]