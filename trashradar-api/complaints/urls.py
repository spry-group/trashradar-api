from django.conf.urls import include, url
from rest_framework import routers

from complaints.views import ComplaintViewSet, EntityViewSet

router = routers.SimpleRouter(trailing_slash=False)
# Accounts Routes
router.register(r'complaints', ComplaintViewSet, 'complaints')
router.register(r'entities', EntityViewSet, 'entities')

urlpatterns = [
    url(r'^', include(router.urls)),
]
