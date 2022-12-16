from .models import Comment
from django import forms  # forms : django에서 지원해줌

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )