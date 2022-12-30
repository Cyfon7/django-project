from django.urls import path, include

from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/tag/<int:tag_id>', views.search_tag, name='search_tag'),
    path('search/category/<int:category_id>', views.search_category, name='search_category'),
    path('recipes/<int:recipe_id>', views.detail, name='detail'),
    path('favorite/create', views.favorite_create, name='heart'),
    path('favorite/delete', views.favorite_destroy, name='unheart'),
    path('review/create', views.review_create, name='review_create')
]