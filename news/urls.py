from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from .views import NewsView

# api versioning
router = routers.DefaultRouter()
router.register('news', NewsView, 'news')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('docs/', include_docs_urls(title='News API'))
]