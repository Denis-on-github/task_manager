from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main.admin import task_manager_admin_site
from main.views import TagViewSet, TaskViewSet, UserViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager",
        default_version="v1",
        description="Task Manager, something very similar to Jira and other tools.",
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
