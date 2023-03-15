from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="hhapp/")),
    path("social_auth/", include("social_django.urls", namespace="social")),
    path("hhapp/", include("hhapp.urls", namespace="hhapp")),
    path("authapp/", include("authapp.urls", namespace="authapp")),
    path("applicantapp/", include("applicantapp.urls", namespace="applicant")),
    path("employerapp/", include("employerapp.urls", namespace="employerapp")),
    path("news/", include("newsapp.urls", namespace="news")),
    path("service/", include("serviceapp.urls", namespace="service")),
    path("support/", include("supportapp.urls", namespace="support")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
