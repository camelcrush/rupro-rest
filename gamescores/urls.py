from rest_framework.routers import DefaultRouter
from . import views

app_name = "gamescores"

router = DefaultRouter()
router.register("", viewset=views.GameScoreViewSet)

urlpatterns = router.urls
