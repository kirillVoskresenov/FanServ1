from django import forms
from .models import Post, Comment
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = '__all__'

class CommForm(forms.ModelForm):
   class Meta:
       model = Comment
       fields = '__all__'


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='authors')
        basic_group.user_set.add(user)
        return user

class MediaForm(forms.ModelForm):
    file = forms.FileField(label='Загрузить файл')
    class Meta:
        model = Post
        fields = ('title', 'file')