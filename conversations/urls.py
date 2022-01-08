app_name = "conversations"

urlpatterns = []
from django.urls import path, include
from . import views

app_name = "conversations"

urlpatterns = [
    path("create/<int:a_pk>/<int:b_pk>/", views.ConversationView),
]
