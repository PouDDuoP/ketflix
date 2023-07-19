from rest_framework.routers import DefaultRouter

from series.api.views import EpisodesApiView, SerieApiView

router = DefaultRouter()

router.register(prefix='series', basename='series', viewset=SerieApiView)
router.register(prefix='episodes', basename='episodes', viewset=EpisodesApiView)
# router.register('', SerieApiView, basename="series")

urlpatterns = router.urls