from django import forms
from . models import Comment

class EmailPostForm(forms.Form):
    """Форма для создания и отправки рекомендации на пост по e-mail
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    """Форма создания комментария к посту
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']