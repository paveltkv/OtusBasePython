from django.shortcuts import render

from .models import Channel


def index(request):
    all_channels = Channel.objects.all()
    context = {
        'all_channels': all_channels
    }
    return render(request, 'index.html', context=context)
