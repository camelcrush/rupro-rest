from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("", views.UsersView.as_view()),
    path("login/", views.login),
    path("me/", views.MeView.as_view()),
    path("<int:pk>/", views.user_detail),
    path("me/blocking/", views.BlockView.as_view()),
    path("me/following/", views.FollowingView.as_view()),
    path("me/game_list/", views.GameListView.as_view()),
]
