from django.urls import path
from django.contrib.auth import views as auth_views
# LoginView redirect после логина определяется переменной settings.LOGIN_REDIRECT_URL

app_name = 'account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), 
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]