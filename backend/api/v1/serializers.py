from rest_framework import serializers

from .models import TestMp3


class TestMp3ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestMp3
        fields = '__all__'