from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.CategoryView, name='category'),
    path('ingredient/', views.IngredientView, name='ingredient'),
    path('tag/', views.TagView, name='tag'),
    path('unit/', views.UnitView, name='unit'),
    path('recipe/', views.RecipeView, name='recipe'),
    path('amount/', views.AmountView, name='amount'),
]