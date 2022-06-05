from django.shortcuts import render, get_object_or_404
from .models import Author, Tred, Topic
# Create your views here.


def home(request):
    topics = Topic.objects.all()
    context = {
        'topics': topics
    }
    return render(request, 'topics.html', context)


def detail(request, slug):
    tred = get_object_or_404(Tred, slug=slug)
    context = {
        'tred': tred
    }
    return render(request, 'detail.html', context)


def treds(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    treds = Tred.objects.filter(approved=True, topics=topic)
    context = {
        'treds': treds,
        'topic': topic
    }
    return render(request, 'treds.html', context)
