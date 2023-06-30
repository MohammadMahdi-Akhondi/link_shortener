from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_schema_view(
   openapi.Info(
      title=_('Link shortener'),
      default_version='v1',
      description='Link shortener service implemented using Django Formwork and Django Rest',
      contact=openapi.Contact(email='mohammadmahdi.developer@gmail.com'),
      license=openapi.License(name="GNU GENERAL PUBLIC LICENSE"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   # urls of admin django
   path('admin/', admin.site.urls),

   # endpoint of my apps
   path('api/v1/account/', include('account.urls')),
   path('api/v1/link/', include('link.urls')),
   path('api/v1/payment/', include('payment.urls')),

   # endpoints of JWT authentication
   path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   # URLs of the documents
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
