from django.urls import path

from .api import views


urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='user_registration'),
    path('activate/<str:token>/', views.UserActivateView.as_view(), name='user_activate')
]
