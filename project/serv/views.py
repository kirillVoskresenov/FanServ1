import os
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post, Comment, BaseRegisterForm, Appointment
from .filters import PostFilter
from .forms import PostForm, CommentForm, CommForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class PostsList(ListView):
    model = Post
    ordering = '-article_date'
    template_name = 'startpage.html'
    context_object_name = 'startpage'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'detail'

class PostCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'create.html'
    permission_required = ('create')

class PostUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    permission_required = ('edit')

class PostDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('startpage')


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    queryset = Post.objects.order_by('-article_date')
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_create.html'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return render(request, 'comment_create.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Comment(
            user=request.POST['user'],
            text=request.POST['text'],
        )
        appointment.save()

        html_content = render_to_string(
            'comment_create.html',
            {
                'appointment': appointment,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{appointment.user}',
            message=f'Получен новый комментарий по вашему объявлению: "{self.object.text}"',
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            recipient_list=[]
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        return redirect('/')



class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment

    def get_template_names(self):
        response = self.get_object()
        if response.post.author == self.request.user:
            self.template_name = 'comment_detail.html'
            return self.template_name
        else:
            raise PermissionDenied


class CommentList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment_list.html'
    context_object_name = 'comment_list'
    ordering = '-time_in'

class CommentUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    form_class = CommForm
    model = Post
    template_name = 'comment_edit.html'
    permission_required = ('comment_edit')

class CommentDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('startpage')