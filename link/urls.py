from django.urls import path

from .api import views


urlpatterns = [
    path('create/', views.CreateLinkView.as_view(), name='create_link'),
]
