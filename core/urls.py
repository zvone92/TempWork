
from django.contrib import admin
from django.urls import path, include
from temp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('temp/', include('temp.urls')),
    path('users/', include('users.urls')),
    path('messaging/', include('messaging.urls'))

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
