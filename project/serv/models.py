from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.dispatch import receiver



class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='guests')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )



Tanks = 'TN'
Healers = 'HL'
DD = 'DD'
Trader = 'ME'
GuildMasters = 'GM'
QuestGivers = 'QG'
Blacksmiths = 'BS'
Tanners = 'TS'
PotionMakers = 'PM'
SpellMasters = 'SM'

CATEGORYES = [
    (Tanks, 'Танки'),
    (DD, 'ДД'),
    (Healers, 'Хиллеры'),
    (Trader, 'Торговцы'),
    (GuildMasters, 'Гилдмастера'),
    (QuestGivers, 'Квестгиверы'),
    (Blacksmiths, 'Кузнецы'),
    (Tanners, 'Кожевники'),
    (PotionMakers, 'Зельевары'),
    (SpellMasters, 'Мастера заклинаний'),
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username.title()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category_type = models.CharField(max_length=15, choices=CATEGORYES, default=None)

    def __str__(self):
        return self.name.title()





class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    article_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    text = models.TextField()
    file = models.FileField(blank=True, upload_to='media/')

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def preview(self):
        return self.text[0:124] + '...'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    class Meta:
        db_table = 'project_image'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text




