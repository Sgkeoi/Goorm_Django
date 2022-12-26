from .models import Board
from django import forms  # forms : django에서 지원해줌

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']