from rest_framework import viewsets, mixins

from .models import New
from .serializer import NewsSerializer


class NewsView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = NewsSerializer
    queryset = New.objects.order_by('-date')
