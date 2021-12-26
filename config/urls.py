from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/posts/", include("posts.urls")),
    path("api/v1/boards/", include("boards.urls")),
    path("api/v1/conversations/", include("conversations.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
