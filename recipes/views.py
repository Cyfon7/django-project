from django.shortcuts import render

# Create your views here.

from django.views import generic
from .models import Category, Ingredient, Tag, Unit, Recipe, Amount

def index(request):
    tags = Tag.objects.all()
    categories = Category.objects.all()
    recipes = Recipe.objects.all()

    context = {
        'tags': tags,
        'categories': categories,
        'recipes': recipes
    }

    return render(request, 'recipes/index.html', context)

class CategoryView():
    template_name = 'recipes/categories.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return Category.objects.all()

class IngredientView():
    template_name = 'recipes/ingredients.html'
    context_object_name = 'ingredient_list'

    def get_queryset(self):
        return Ingredient.objects.all()

class TagView():
    template_name = 'recipes/tags.html'
    context_object_name = 'tag_list'

    def get_queryset(self):
        return Tag.objects.all()

class UnitView():
    template_name = 'recipes/units.html'
    context_object_name = 'unit_list'

    def get_queryset(self):
        return Unit.objects.all()

class RecipeView():
    template_name = 'recipes/recipes.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()

class AmountView():
    template_name = 'recipes/amount.html'
    context_object_name = 'amount_list'

    def get_queryset(self):
        return Amount.objects.all()