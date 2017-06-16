from rest_framework import routers

from complaints.views import ComplaintViewSet, EntityViewSet

router = routers.SimpleRouter(trailing_slash=False)
# Accounts Routes
router.register(r'complaints', ComplaintViewSet)
router.register(r'entities', EntityViewSet)
