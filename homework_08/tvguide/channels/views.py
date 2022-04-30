from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .models import Channel


def index(request):
    all_channels = Channel.objects.all()
    context = {
        'all_channels': all_channels
    }
    return render(request, 'channels/index.html', context=context)


class ChannelDetailView(DetailView):
    model = Channel


class ChannelCreateView(CreateView):
    model = Channel
    success_url = reverse_lazy('main')
    fields = '__all__'


class ChannelUpdateView(UpdateView):
    model = Channel
    success_url = reverse_lazy('main')
    fields = '__all__'


class ChannelDeleteView(DeleteView):
    model = Channel
    success_url = reverse_lazy('main')
    fields = '__all__'