from django.urls import path

from .api import views


urlpatterns = [
    path('user/registration/', views.UserRegistrationView.as_view(), name='user_registration'),
]
