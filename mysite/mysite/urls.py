from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.templatetags.static import static as get_static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('favicon.ico', RedirectView.as_view(url=get_static('main/images/favicon.ico'), permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.DEBUG else settings.STATIC_ROOT)

