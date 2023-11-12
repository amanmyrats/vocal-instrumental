from rest_framework.viewsets import ModelViewSet

from .models import TestMp3
from .serializers import TestMp3ModelSerializer


class TestMp3View(ModelViewSet):
    queryset = TestMp3.objects.all()
    serializer_class = TestMp3ModelSerializer
