from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title=_('Link shortener'),
      default_version='v1',
      description='Link shortener service implemented using Django Formwork and Django Rest',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact('mohammadmahdi.developer@gmail.com'),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # urls of admin django
    path('admin/', admin.site.urls),

    # endpoint of my apps
    path('api/v1/account/', include('account.urls')),

    # URLs of the documents
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
