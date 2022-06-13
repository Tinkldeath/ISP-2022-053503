import uuid
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Topic(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=200, default=uuid.uuid4)
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    @property
    def treds(self):
        return Tred.objects.filter(topic=self, approved=True).count()

    @property
    def last_tred(self):
        return Tred.objects.filter(topic=self, approved=True).latest('date')

    def get_url(self):
        return reverse('topic', kwargs={
            'slug': self.slug
        })


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    role = models.CharField(max_length=40, default='Member')
    slug = models.SlugField(max_length=200, default=uuid.uuid4)
    bio = models.TextField(max_length=1000, default='Empty')
    rating = models.IntegerField(default=0)

    def num_treds(self):
        return Tred.objects.filter(approved=True, author=self).count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('profile', kwargs={
            "slug": self.slug
        })

    def get_treds(self):
        return Tred.objects.filter(author=self, approved=True)


class Reply(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField(default="comment")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "replies"

    def __str__(self):
        return self.content[:100]


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField(default="comment")
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.content[:100]


class Tred(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default=uuid.uuid4)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    comments = models.ManyToManyField(Comment, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tred, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('tred', kwargs={
            "slug": self.slug
        })

    @property
    def last_comment(self):
        return self.comments.latest("date")

    @property
    def num_comments(self):
        return self.comments.count()
    
