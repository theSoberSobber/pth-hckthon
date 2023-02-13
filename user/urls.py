from django.urls import path
from .views import *

urlpatterns = [
    path('',UserLogin.as_view()),
    path('login/',UserLogin.as_view(), name="login"),
    path('register/',UserRegistration.as_view(), name="register"),
    path('dashboard/',UserDashboard.as_view(), name="dashboard"),
    path('logout/',UserLogout.as_view(), name="logout"),
]

