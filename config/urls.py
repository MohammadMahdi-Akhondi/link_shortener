from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # urls of admin django
    path('admin/', admin.site.urls),

    # endpoint of my apps
    path('api/v1/account/', include('account.api.urls')),
]
