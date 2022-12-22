from django.contrib import admin

# Register your models here.

from .models import Category, Ingredient, Tag, Unit, Recipe, Amount, Rating, Favorite, Review

# Inlines
class AmountInline(admin.TabularInline):
    model = Amount
    exclude = ['deleted']
    extra = 1

# Admin models
class CommonAdmin(admin.ModelAdmin):
    exclude = ['deleted']

class RecipeAdmin(CommonAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'description', 'steps']}),
        ('Clasification', {'fields': ['tag', 'category'], 'classes': ['collapse']})
    ]
    inlines = [AmountInline]

class CategoryAdmin(CommonAdmin):
    pass

class IngredientAdmin(CommonAdmin):
    pass

class TagAdmin(CommonAdmin):
    pass

class UnitAdmin(CommonAdmin):
    pass

class AmountAdmin(CommonAdmin):
    pass

class RatingAdmin(CommonAdmin):
    pass

class FavoriteAdmin(CommonAdmin):
    pass

class ReviewAdmin(CommonAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Review, ReviewAdmin)