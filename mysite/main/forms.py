from django import forms
from .models import Articles, Comments
from django.contrib.auth.forms import PasswordChangeForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'summary', 'full_text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'full_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Share your opinion...'
            }),
        }

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in ["old_password", "new_password1", "new_password2"]:
            self.fields[name].widget.attrs.update({
                "class": "form-control",  
            })