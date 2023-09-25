from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.urls import include, path

admin.site.index_title = "CCompliance"
admin.site.site_header = "CCompliance"
admin.site.site_title = "CCompliance"

empty_redirect = lambda request: HttpResponseRedirect(
    reverse("admin:index")
)

fuck_off = lambda request: HttpResponse(
    "<p>Fuck off</p>", 
    content_type="text/html"
)

urlpatterns = [
    path('', view=empty_redirect),
    path('fuck-off', view=fuck_off, name='fuck-off'),
    path('admin/', admin.site.urls),
    path('admin-actions/', include('compliance_projects.urls', namespace='admin-actions'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, 
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
