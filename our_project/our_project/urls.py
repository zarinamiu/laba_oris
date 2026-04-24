from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import home  # <-- Импортируем home
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API PinkStore",
        default_version='v1',
        description="API для интернет-магазина PinkStore 💗",
        contact=openapi.Contact(email="support@pinkstore.ru"),
        license=openapi.License(name="Лицензия MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница
    path('', home, name='home'),  # <-- Вот так!

    # Приложения
    path('catalog/', include('catalog.urls')),
    path('users/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('orders/', include('orders.urls')),

    # API документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)