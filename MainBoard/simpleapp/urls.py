from django.urls import path
from .views import (
   NewsList, NewsDetail, NewsCreate,
   NewsUpdate, NewsDelete, subscriptions)
from django.views.decorators.cache import cache_page



urlpatterns = [
   path('', NewsList.as_view(), name='news'),
   path('<int:pk>', cache_page(60*10)(NewsDetail.as_view())),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),

]