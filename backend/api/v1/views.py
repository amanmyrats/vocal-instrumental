from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.viewsets import ModelViewSet

import librosa

from .models import TestMp3
from .serializers import TestMp3ModelSerializer


class TestMp3View(ModelViewSet):
    queryset = TestMp3.objects.all()
    serializer_class = TestMp3ModelSerializer
