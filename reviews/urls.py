from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "reviews"

router = DefaultRouter()
router.register("", viewset=views.ReviewViewSet)

urlpatterns = router.urls
