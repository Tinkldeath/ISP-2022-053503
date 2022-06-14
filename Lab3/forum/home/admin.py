from django.contrib import admin
from .models import Topic, Author, Tred, Comment, Reply

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'user', 'rating')
    search_fields = ('name', 'role')
    list_editable = ('role', 'rating')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'approved')
    search_fields = ('title', 'description')
    list_editable = ('approved',)

class TredAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'approved')
    search_fields = ('title', 'content', 'author')
    list_editable = ('approved',)

admin.site.register(Topic, TopicAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tred, TredAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
