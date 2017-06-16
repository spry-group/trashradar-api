"""trashradar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from accounts.urls import urlpatterns as accounts_urls
from complaints.urls import router as complaints_router

trashradar_urls = accounts_urls + complaints_router.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(trashradar_urls, namespace='v1')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
