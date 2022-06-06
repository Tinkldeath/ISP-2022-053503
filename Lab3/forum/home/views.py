from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Tred
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout


def home(request):
    topics = Topic.objects.all
    context = {
        'topics': topics
    }
    return render(request, 'home.html', context)


def topic(requset, slug):
    topic = get_object_or_404(Topic, slug=slug)
    treds = Tred.objects.filter(topic=topic)
    context = {
        'treds': treds,
        'topic': topic
    }
    return render(requset, 'topic.html', context)


def tred(request, slug):
    tred = get_object_or_404(Tred, slug=slug)
    context = {
        'tred': tred
    }
    return render(request, 'tred.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

        else:
            return render(request, 'signup.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def signin(request):
    print(request.user)
    print(request.method)
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
            return render(request, 'signin.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('signin')
