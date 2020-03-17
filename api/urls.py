"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings # debug-toolbar

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from tldrss.views import ArticleViewSet, FeedViewSet, SummaryViewSet, UserViewSet
from tldrss.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'article', ArticleViewSet)
router.register(r'feed', FeedViewSet)
router.register(r'summary', SummaryViewSet)
router.register(r'user', UserViewSet)

urlpatterns = router.urls + [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
