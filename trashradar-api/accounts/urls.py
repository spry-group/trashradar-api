from django.conf.urls import url
from rest_framework import routers

from accounts.views import AccountViewSet, LoginView, LogoutView

router = routers.SimpleRouter(trailing_slash=False)
# Accounts Routes
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    url(r'^auth/login$', LoginView.as_view(), name='login'),
    url(r'^auth/logout$', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
