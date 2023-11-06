from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home_view(request):
    context = {
        'test': 'some test'
    }
    return render(request, 'home.html', context)