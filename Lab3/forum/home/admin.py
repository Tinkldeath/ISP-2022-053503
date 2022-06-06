from django.contrib import admin
from .models import Topic, Author, Tred, Comment, Reply

admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Tred)
admin.site.register(Comment)
admin.site.register(Reply)
