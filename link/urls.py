from django.urls import path

from .api import views

app_name = 'link'


urlpatterns = [
    path('create/', views.CreateLinkView.as_view(), name='create_link'),
    path('list/', views.ListLinkView.as_view(), name='list_link'),
    path('detail/<int:link_id>/', views.DetailLinkView.as_view(), name='detail_link'),
    path('update/<int:link_id>/', views.UpdateLinkView.as_view(), name='update_link'),
    path('delete/<int:link_id>/', views.DeleteLinkView.as_view(), name='delete_link'),
    path('<str:token>/', views.RedirectLinkView.as_view(), name='redirect_link'),
]
