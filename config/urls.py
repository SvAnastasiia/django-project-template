from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            (
                [
                    # Swagger docs
                    path(
                        "schema/",
                        SpectacularAPIView.as_view(),
                        name="schema",
                    ),
                    path(
                        "documentation/",
                        SpectacularSwaggerView.as_view(
                            url_name="schema",
                        ),
                        name="swagger-ui",
                    ),
                ]
            )
        ),
    ),
]
