from rest_framework.routers import DefaultRouter
from arsmoon.bitmex import api_views

router = DefaultRouter()
router.register(r'order', api_views.OrderBitmexViewSet, basename='order')


# urlpatterns = [
#
# ]

urlpatterns = router.urls
