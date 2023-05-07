from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('list/<int:num>', views.list, name='list'),
    path('find', views.find, name='find'),
    path('find/<int:num>', views.find, name='find'),
    path('large_category', views.large_category, name='large_category'),
    path('medium_category', views.medium_category, name='medium_category'),
    path('small_category', views.small_category, name='small_category'),
    path('favorite', views.favorite, name='favorite'),
    path('favorite/<int:num>', views.favorite, name='favorite'),
    path('favorite_confirm', views.favorite_confirm, name='favorite_confirm'),
    path('favorite_result', views.favorite_result, name='favorite_result'),
    path('favorite_js', views.favorite_js, name='favorite_js'),
    path('favorite_js/<int:num>', views.favorite_js, name='favorite_js'),
    path('favorite_page', views.favorite_page, name='favorite_page'),
    path('favorite_page/<int:num>', views.favorite_page, name='favorite_page'),
    #下記、データ登録用のページ(アクセスするとinsertが走る)
#    path('rakuten_recipe', views.rakuten_recipe, name='rakuten_recipe'),
]