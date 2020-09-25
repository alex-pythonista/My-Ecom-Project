from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop_app.urls')),
    path('account/', include('login_app.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
