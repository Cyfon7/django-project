from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CommonModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

    class Meta:
        abstract = True

class NamedModel(CommonModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True

class UserRelationModel(CommonModel):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# App models

class Category(NamedModel):
    pass
    
class Ingredient(NamedModel):
    pass

class Tag(NamedModel):
    pass

class Unit(NamedModel):
    name = models.CharField(max_length=10)

class Recipe(CommonModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    steps = models.TextField()
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    tag = models.ForeignKey(Tag, models.SET_NULL, blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='Amount')

    def __str__(self):
        return self.title
    
class Amount(CommonModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=False)

class Rating(UserRelationModel):
    points = models.DecimalField(decimal_places=1, max_digits=1)

class Favorite(UserRelationModel):
    pass

class Review(UserRelationModel):
    content = models.TextField()
    rate = models.DecimalField(decimal_places=1, max_digits=1)