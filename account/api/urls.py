from django.urls import path

from . import views


urlpatterns = [
    path('user/registration/', views.UserRegistrationView.as_view(), name='user_registration')
]
