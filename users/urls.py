from rest_framework.routers import DefaultRouter
from . import views

app_name = "users"

router = DefaultRouter()
router.register("", viewset=views.UserViewSet)

urlpatterns = router.urls
