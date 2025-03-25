from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('shop/', include('shop.urls', namespace='shop')),
                  path('users/', include('users.urls', namespace='users')),
                  path('social-auth/',
                       include('social_django.urls', namespace='social')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
