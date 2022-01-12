from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = "users"

router = DefaultRouter()
router.register("", viewset=views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "activate/<str:uidb64>/<str:token>/",
        views.UserActive.as_view(),
        name="activate",
    ),
    path("login/kakao", views.KakaoLogin.as_view()),
    path("login/kakao/callback", views.KakaoCallback.as_view()),
]
