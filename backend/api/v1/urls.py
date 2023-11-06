from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TestMp3View


router = DefaultRouter()
router.register('test', TestMp3View, 'test-mp3')

from .views import TestMp3View
from separator.views import separate_view


urlpatterns = [
    path('', include(router.urls)), 
    path('separate', separate_view, name='separate')
]