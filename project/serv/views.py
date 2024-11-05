import os
from django.views.generic import ListView, DetailView, UpdateView,\
    DeleteView, CreateView, TemplateView
from .models import Post, Comment, BaseRegisterForm
from .filters import PostFilter
from .forms import PostForm, CommForm, MediaForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string



class AuthView(LoginRequiredMixin, TemplateView):
    template_name = 'authorization/auth.html'

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
    permission_required = ('serv.add_post')

class PostUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    permission_required = ('serv.change_post')

class PostDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('startpage')
    permission_required = ('serv.delete_post')


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
    form_class = CommForm
    model = Comment
    template_name = 'comment_edit.html'
    permission_required = ('serv.add_comment')
    success_url = reverse_lazy('startpage')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = User.objects.get(id=self.request.user.id)
            post.post = Post.objects.get(id=self.kwargs['pk'])
            post.save()

        send_mail(
            subject=f'Получен отклик по объявлению "{post.user}"',
            # имя клиента и дата записи будут в теме для удобства
            message=f'Получен новый отклик по вашему объявлению: "{post.text}"',
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[post.user.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        messages.success(self.request, 'Ваш отклик успешно отправлен!')
        return super().form_valid(form)


class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    permission_required = ('serv.view_comment')

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
    model = Comment
    template_name = 'comment_edit.html'
    permission_required = ('serv.change_comment')
    success_url = reverse_lazy('startpage')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.post = Post.objects.get(id=self.kwargs['pk'])
            post.save()
        return super().form_valid(form)



class CommentDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('startpage')
    permission_required = ('serv.delete_comment')



def upload_media(request, **kwargs):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html', {'form': form, 'obj': obj})
    else:
        form = MediaForm()
    return render(request, 'upload.html', {'form': form})

