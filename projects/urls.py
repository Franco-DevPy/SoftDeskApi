from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet
from .views import ContributorViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")


router.register(r"contributors", ContributorViewSet, basename="contributor")


urlpatterns = router.urls
