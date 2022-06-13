from django import forms
from .models import Author, Topic, Tred


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'bio')


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'description')


class TredForm(forms.ModelForm):
    class Meta:
        model = Tred
        fields = ('title', 'content', 'topic')


class ChangeAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'bio')
