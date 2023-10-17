from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import *
from django.views.generic import ListView, DetailView, CreateView, FormView
from .utils import *

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статтю", 'url_name': 'add_page'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
        {'title': "Вхід", 'url_name': 'login'}]


class NewsHome(DataMixin, ListView):
    model = News
    template_name = 'site_app/index.html'
    context_object_name = 'posts'
    # extra_context = {'title': 'Головна сторінка'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = News.objects.all()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Головна сторінка',
#                'cat_selected': 0,
#                }
#     return render(request, 'site_app/index.html', context=context)



# @login_required
def about(request):
    contact_list = News.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'site_app/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'Про сайт'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'site_app/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Створення статті')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#             # print(form.cleaned_data)
#             # try:
#             #     News.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             #
#             # except:
#             #     form.add_error(None, 'Помилка')
#     else:
#         form = AddPostForm()
#     return render(request, 'site_app/addpage.html', {'form': form, 'menu': menu, 'title': 'Додавання публікацій'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'site_app/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зворотній зв`язок')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизація")


class ShowPost(DataMixin, DetailView):
    model = News
    template_name = 'site_app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context



# def show_post(request, post_slug):
#     post = get_object_or_404(News, slug=post_slug)
#     context = {'post': post,
#                'menu': menu,
#                'title': post.title,
#                'cat_selected': post.cat_id,
#                }
#
#     return render(request, 'site_app/post.html', context=context)


class NewsCategory(DataMixin, ListView):
    model = News
    template_name = 'site_app/index.html'
    context_object_name = 'posts'
    allow_empty = False
    # extra_context = {'title': 'Головна сторінка'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категорія: ' + str(c.name),
                                      cat_selected=c.pk)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


# def show_category(request, cat_slug):
#     cat = Category.objects.filter(slug=cat_slug)
#     posts = News.objects.filter(cat_id=cat[0].id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Рубрики',
#                'cat_selected': cat[0].id,
#                }
#     return render(request, 'site_app/index.html', context=context)


# def categories(request, catid):
#     if request.GET:
#         print(request.GET)
#
#     return HttpResponse(f"<h1>Категорії новин</h1><p>{catid}</p>")
#
#
# def archive(request, year):
#     if int(year) > 2020:
#         return redirect('home', permanent=True)
#
#     return HttpResponse(f"<h1>Архів по рокам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'site_app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зареєструватися')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'site_app/login.html'
    # success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')