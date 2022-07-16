from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from quiz.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('quiz/', include('quiz.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
