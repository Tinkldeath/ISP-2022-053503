from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Tred, Author, Comment, Reply
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm, TopicForm, TredForm, ChangeAuthorForm


def home(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        try:
            author = Author.objects.get(user=user)
            context.update({
                'author': author
            })
        except:
            print('Author is not registered')
    topics = Topic.objects.filter(approved=True)
    if topics.count() == 0:
        topics = []
    context.update({
        'topics': topics
    })
    return render(request, 'home.html', context)


def topic(requset, slug):
    context = {}
    user = requset.user
    if user.is_authenticated:
        try:
            author = Author.objects.get(user=user)
            context.update({
                'author': author
            })
        except:
            return redirect('update')
    topic = get_object_or_404(Topic, slug=slug)
    treds = Tred.objects.filter(topic=topic, approved=True)
    context.update({
        'treds': treds,
        'topic': topic
    })
    return render(requset, 'topic.html', context)


def tred(request, slug):
    tred = get_object_or_404(Tred, slug=slug)
    user = request.user
    context = {}
    if user.is_authenticated:
        try:
            author = Author.objects.get(user=user)
            context.update({
                'author': author
            })
        except:
            return redirect('update')
    if 'comment-form' in request.POST:
        content = request.POST.get('comment')
        new_comment, created = Comment.objects.get_or_create(author=author, content=content)
        tred.comments.add(new_comment.id)
    if 'reply-form' in request.POST:
        content = request.POST.get('reply')
        comment_id = request.POST.get('comment-id')
        comment = Comment.objects.get(id=comment_id)
        new_reply, created = Reply.objects.get_or_create(author=author, content=content)
        comment.replies.add(new_reply.id)
    context.update({
        'tred': tred
    })
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
            return redirect('update')

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


@login_required
def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def update(request):
    user = request.user
    try:
        author = Author.objects.get(user=user)
        return redirect('home')
    except:
        print('Adding user')
    form = UpdateForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = user
            update_profile = form.save()  # ← assign the user to a variable
            update_profile.save()
            return redirect('home')
    return render(request, 'update.html', {'form': form})


def add_topic(request):
    user = request.user
    if user.is_anonymous:
        return redirect('signin')
    context = {}
    if user.is_authenticated:
        try:
            author = Author.objects.get(user=user)
            context.update({
                'author': author
            })
        except:
            return redirect('update')
    form = TopicForm(request.POST, request.FILES)
    context.update({
        'form': form
    })
    if request.method == 'POST':
        if form.is_valid():
            author = Author.objects.get(user=user)
            author.rating += 1
            if author.rating > 10:
                author.role = "Active Member"
            elif author.rating > 50:
                author.role = "God"
            author.save()
            new_topic = form.save(commit=False)
            new_topic.save()
            return redirect('home')
    return render(request, 'addtopic.html', context)


def add_tred(request):
    user = request.user
    if user.is_anonymous:
        return redirect('signin')
    context = {}
    if user.is_authenticated:
        try:
            author = Author.objects.get(user=user)
            context.update({
                'author': author
            })
        except:
            return redirect('update')
    form = TredForm(request.POST, request.FILES)
    context.update({
        'form': form
    })
    if request.method == 'POST':
        if form.is_valid():
            author = Author.objects.get(user=user)
            author.rating += 1
            if author.rating > 10:
                author.role = "Active Member"
            elif author.rating > 50:
                author.role = "God"
            author.save()
            new_tred = form.save(commit=False)
            new_tred.author = author
            new_tred.save()
            return redirect('home')
    return render(request, 'addtred.html', context)


def search_view(request):
    return render(request, 'search.html')


def profile(request, slug):
    user = request.user
    if user.is_anonymous:
        return redirect('signin')
    context = {}
    if user.is_authenticated:
        try:
            author = Author.objects.get(user=user)
            context.update({
                'author': author
            })
        except:
            return redirect('update')
    form = ChangeAuthorForm(request.POST, request.FILES)
    context.update({
        'form': form
    })
    user_as_author = Author.objects.get(user=user)
    author = Author.objects.get(slug=slug)
    if not author:
        redirect('update')
    is_user = user_as_author.slug == slug
    context.update({
        'is_user': is_user
    })
    if request.method == 'POST':
        if is_user:
            if form.is_valid():
                user_as_author.name = form.cleaned_data['name']
                user_as_author.bio = form.cleaned_data['bio']
                user_as_author.image = form.cleaned_data['image']
                user_as_author.save()
                redirect('home')
    return render(request, 'profile.html', context)
