import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.
from django.db import models
from .models import Category, Ingredient, Tag, Unit, Recipe, Amount, Favorite, Review

def index(request):
    tags = Tag.objects.values()
    categories = Category.objects.values()
    recent_recipes = Recipe.recent_last(9)
    top_tags = Recipe.top_5_used()
    popular_recipes = Recipe.top_popular()
    top_recipes = Recipe.top_5_rating()

    context = {
        'tags': tags,
        'categories': categories,
        'top_tags': top_tags,
        'popular_recipes': popular_recipes,
        'recent_recipes': recent_recipes,
        'top_recipes': top_recipes
    }

    return render(request, 'recipes/index.html', context)

def detail(request, recipe_id):
    tags = Tag.objects.values()
    categories = Category.objects.all()
    recipe = Recipe.objects.get(pk=recipe_id)
    top_tags = Recipe.top_5_used()
    popular_recipes = Recipe.top_popular()
    reviews = recipe.review_set.all()

    context = {
        'recipe': recipe,
        'tags': tags,
        'categories': categories,
        'top_tags': top_tags,
        'popular_recipes': popular_recipes,
        'reviews': reviews
    }

    return render(request, 'recipes/detail.html', context)

def search(request):
    q = request.GET['q']

    recipes = Recipe.objects.filter(
        models.Q(title__icontains=q) |
        models.Q(description__icontains=q) |
        models.Q(steps__icontains=q) |
        models.Q(ingredients__name__icontains=q)
    )
    tags = Tag.objects.values()
    categories = Category.objects.values()
    top_tags = Recipe.top_5_used()
    popular_recipes = Recipe.top_popular()

    context = {
        'recipes': recipes,
        'top_tags': top_tags,
        'popular_recipes': popular_recipes,
        'tags': tags,
        'categories': categories,
        'query': f"Search: {q}"
    }

    return render(request, 'recipes/search/search.html', context)

def search_tag(request, tag_id):
    recipes = Recipe.objects.filter(tag=tag_id)
    tags = Tag.objects.values()
    categories = Category.objects.values()
    top_tags = Recipe.top_5_used()
    popular_recipes = Recipe.top_popular()
    tag = Tag.objects.get(pk=tag_id)

    context = {
        'recipes': recipes,
        'top_tags': top_tags,
        'popular_recipes': popular_recipes,
        'tags': tags,
        'categories': categories,
        'query': f"Tag: {tag.name}"
    }

    return render(request, 'recipes/search/search.html', context)

def search_category(request, category_id):
    recipes = Recipe.objects.filter(category=category_id)
    tags = Tag.objects.values()
    categories = Category.objects.values()
    top_tags = Recipe.top_5_used()
    popular_recipes = Recipe.top_popular()
    category= Category.objects.get(pk=category_id)

    context = {
        'recipes': recipes,
        'top_tags': top_tags,
        'popular_recipes': popular_recipes,
        'tags': tags,
        'categories': categories,
        'query': f"Category: {category.name}"
    }

    return render(request, 'recipes/search/search.html', context)

def favorite_create(request):
    data = json.loads(request.body)
    Favorite.objects.create(recipe_id=int(data['recipe_id']), user_id=request.user.id)
    
    return HttpResponse(data)

def favorite_destroy(request):
    data = json.loads(request.body)
    Favorite.objects.filter(recipe_id=int(data['recipe_id']), user_id=request.user.id).delete()

    return HttpResponse(data)

def review_create(request):
    review = Review.objects.create(
                recipe_id=int(request.POST['recipe_id']),
                user_id=int(request.POST['user_id']),
                rate=float(request.POST['rate']),
                content=request.POST['content']
            )
    return HttpResponseRedirect(reverse('recipes:detail', args=(int(review.recipe_id),)))

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return HttpResponseRedirect("/")
        messages.error(request, "Invalid data provided")
    else:
        form = SignUpForm()
    return render (request=request, template_name="recipes/registration/register.html", context={"form": form})

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