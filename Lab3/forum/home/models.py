from django.shortcuts import reverse, get_object_or_404
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager

User = get_user_model()


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    bio = HTMLField()
    points = models.IntegerField(default=0)
    photo = ResizedImageField(size=[50, 80], quality=100, upload_to='authors', default=None, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super(Author, self).save(*args, **kwargs)

    def num_treds(self):
        return Tred.objects.filter(approved=True, author=self).count()


class Topic(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "topics"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    @property
    def num_treds(self):
        return Tred.objects.filter(topics=self).count()

    @property
    def last_tred(self):
        return Tred.objects.filter(topics=self).latest("date")

    def get_url(self):
        return reverse('treds', kwargs={
            'slug': self.slug
        })


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
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    topics = models.ManyToManyField(Topic)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)
    image = ResizedImageField(size=[1280, 720], quality=100, upload_to='images', default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tred, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('detail', kwargs={
            "slug": self.slug
        })

    @property
    def last_comment(self):
        return self.comments.latest("date")
