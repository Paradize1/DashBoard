from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import News
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, Category
from django.core.cache import cache


class NewsList(ListView):
    model = News
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = News
    template_name = 'news_number.html'
    context_object_name = 'news_number'


    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'news-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
            return obj

class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = NewsForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('news')
    raise_exception = True
    permission_required = ('news.add_post',)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_update.html'
    success_url = reverse_lazy('news')
    permission_required = ('news.add_post',)

class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')
    permission_required = ('news.add_post',)

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )