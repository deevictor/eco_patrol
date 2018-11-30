from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from mezzanine.pages.views import page

admin.autodiscover()

urlpatterns = [
    url('^admin/', include(admin.site.urls)),
    url('^label/', include('label.urls')),
    url('^user/', include('user.urls')),
    url("^$", page, {"slug": "/"}, name="home"),
    url('^', include('mezzanine.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'mezzanine.core.views.page_not_found'
handler500 = 'mezzanine.core.views.server_error'
