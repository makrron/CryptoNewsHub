from rest_framework import viewsets

from .models import New
from .serializer import NewsSerializer


# Create your views here.
class NewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = New.objects.order_by('-date')
