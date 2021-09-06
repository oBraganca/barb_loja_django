from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static


from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('barb.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)