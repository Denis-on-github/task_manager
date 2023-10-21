"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main.admin import task_manager_admin_site
from main.views import TagViewSet, TaskViewSet, UserViewSet
from test.test_rollbar import index

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
    path('api/rollbar/', index, name='rollbar')
]
