from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, FormView
from django.contrib.postgres.search import TrigramSimilarity

from men.forms import MenForm, SendUserEmailForm
from men.models import Men, Category, Tags
from men.utils import MenMixin


class HomePageView(MenMixin, ListView):
    model = Men
    template_name = 'men/home.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        return Men.objects.all().filter(is_published='PUBLISHED')


class AboutSitePageView(TemplateView):
    template_name = 'men/about-site.html'


class DetailPageView(LoginRequiredMixin, DetailView):
    model = Men
    template_name = 'men/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Men.published, slug=self.kwargs[self.slug_url_kwarg])


class CatPageList(MenMixin, ListView):
    model = Men
    template_name = 'men/home.html'
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cat_id'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        return context

    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


class TagPageList(MenMixin, ListView):
    model = Men
    template_name = 'men/home.html'
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tag_id'] = Tags.objects.get(slug=self.kwargs['tag_slug'])
        return context

    def get_queryset(self):
        return Men.published.filter(tag__slug=self.kwargs['tag_slug']).select_related('cat')


class CreateFormView(LoginRequiredMixin, PermissionRequiredMixin , MenMixin, CreateView):
    template_name = "men/add_page.html"
    form_class = MenForm
    permission_required = 'men.add_men'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tags.objects.all()
        return context

    def form_valid(self, form):
        raw_form = form.save(commit=False)
        raw_form.author = self.request.user
        return super().form_valid(form)


class SendEmailPageView(FormView):
    template_name = 'men/communicate.html'
    form_class = SendUserEmailForm
    success_url = reverse_lazy('men:home')

    def form_valid(self, form):
        cd = form.cleaned_data
        message = f'{cd.get("name")} \n ' \
                  f'{cd.get("email")} said : ' \
                  f'{cd.get("comments")}'
        send_mail(
            subject='hello',
            message=message,
            from_email='vinogradovpavel32@gmail.com',
            recipient_list=[f'{settings.EMAIL_HOST_USER}', ], )
        print('send')
        return super().form_valid(form)


class SearchListView(MenMixin, ListView):
    '''
    search by site
    '''
    template_name = 'men/search.html'
    model = Men
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('search', default='')
        result = self.model.published.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        print(result.count())
        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get('search', default='')
        result = self.model.published.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        query_params = self.request.GET.copy()
        query = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = urlencode(query_params)
        context['query'] = self.request.GET.get('search')
        context['result'] = result.count()
        return context
