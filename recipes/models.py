import math
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

    class Meta:
        abstract = True

# App models

class Category(NamedModel):
    pass
    
class Ingredient(NamedModel):
    def amount(self):
        return self.amount_set.all()[0].amount

    def units(self):
        return self.amount_set.all()[0].unit.name
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
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    visit_counter = models.IntegerField(default=0)
    image = models.ImageField(default=None, upload_to='recipes/')

    @classmethod
    def top_5_used(cls):
        return cls.objects.values('tag_id').annotate(count=models.Count('tag_id')).order_by('-count').values('tag_id', 'tag__name')[:5]

    @classmethod
    def top_popular(cls):
        return cls.objects.order_by('-visit_counter').values()[:3]

    @classmethod
    def recent_last(cls, number):
        return cls.objects.order_by('-created')[:number]

    @classmethod
    def top_5_rating(cls):
        return cls.objects.values().annotate(models.Avg('review__rate')).order_by('-review__rate__avg')[:5]

    @classmethod
    def search_query(self, query):
        if query:
            return self.objects.filter(        
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(steps__icontains=query) |
                models.Q(ingredients__name__icontains=query)
            ).order_by('-created').distinct('id')
        else:
            return self.objects.all()

    def __str__(self):
        return self.title

    def author(self):
        return self.user.username

    def time_dmy(self):
        temp_date = str(self.created).split(' ')[0].split('-')
        temp_date.reverse()
        return '-'.join(temp_date)

    def review_counter(self):
        return self.review_set.all().count()

    def avg_rate(self):
        if self.review_set.all().count() > 0:
            avg = float(self.review_set.aggregate(models.Avg('rate'))['rate__avg'])
            return round(avg, 1) if bool(avg) else 0
        else:
            return 0

    def counter_rate_by_range(self, value):
        range = {
            '0': models.Q(**{"%s__gte" % 'rate': 0}),
            '1': models.Q(**{"%s__gte" % 'rate': 0.5}) & models.Q(**{"%s__lt" % 'rate': 1.5}),
            '2': models.Q(**{"%s__gte" % 'rate': 1.5}) & models.Q(**{"%s__lt" % 'rate': 2.5}),
            '3': models.Q(**{"%s__gte" % 'rate': 2.5}) & models.Q(**{"%s__lt" % 'rate': 3.5}),
            '4': models.Q(**{"%s__gte" % 'rate': 3.5}) & models.Q(**{"%s__lt" % 'rate': 4.5}),
            '5': models.Q(**{"%s__gte" % 'rate': 4.5}) & models.Q(**{"%s__lte" % 'rate': 5})
        }
        return self.review_set.filter(range[str(value)]).count()

    def percentage(self, poblation, total):
        return math.floor((poblation / total) * 100) if total > 0 else 0

    def rating_table_calculation(self):
        results = []
        total_rates = self.counter_rate_by_range(0)

        for i in reversed(range(1,6)):
            results.append(self.percentage(self.counter_rate_by_range(i), total_rates))
        
        return results

class Amount(CommonModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=False)

class Favorite(UserRelationModel):
    pass

class Review(UserRelationModel):
    content = models.TextField()
    rate = models.DecimalField(decimal_places=1, max_digits=2)