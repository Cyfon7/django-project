import json

from faker import Faker
from datetime import datetime
from random import sample, randint, random

def model_base(app_name, pk, fields):
    base = {
        "model": app_name,
        "pk": pk,
        "fields": {
            "created": str(datetime.now()),
            "updated": str(datetime.now())
        }
    }

    for k, v in fields.items():
        base['fields'][f"{k}"] = v

    return base

def build_fixture(name, data):
    with open(f"./fixtures/{name}.json", "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

def tag_seeder():
    food_tags = [
        "Easy",
        "Grill",
        "Meat",
        "Fish",
        "Chicken",
        "Pasta",
        "Bread",
        "Vegetable",
        "Hot",
        "Light",
        "Spicy",
        "Party",
        "Holiday",
        "Turkey",
        "Sauce",
        "Fruit",
        "Fresh",
        "Integral",
        "Cookie"
    ]

    data = []
    for index, food in enumerate(food_tags):
        data.append(model_base("recipes.tag", index + 1, { "name": food }))

    build_fixture("tags", data)

    return data

def categories_seeder():
    food_categories = [
        "Breakfast",
        "Lunch",
        "Beverages",
        "Appetizers",
        "Soups",
        "Salads",
        "Main dishes",
        "Side dishes",
        "Desserts",
        "Breads"
    ]

    data = []
    for index, category in enumerate(food_categories):
        data.append(model_base("recipes.category", index + 1, { "name": category }))
    
    build_fixture("categories", data)
    
    return data

def units_seeder():
    food_units = [
        "Und",
        "Kg",
        "gr",
        "lt",
        "ml",
        "mg"
    ]

    data = []

    for index, unit in enumerate(food_units):
        data.append(model_base("recipes.unit", index + 1, { "name": unit }))
    
    build_fixture("units", data)
    
    return data

def recipes_seeder():  

    fake = Faker()
    recipes = []
    ingredients = []
    amounts = []
    reviews = []
    favorites = []

    ing_counter = 0
    rev_counter = 0
    fav_counter = 0

    tags = tag_seeder()
    categories = categories_seeder()
    units = units_seeder()

    for i in range(20):
        recipes.append(model_base("recipes.recipe", i + 1,
            {
                'title': fake.sentence(nb_words=5),
                'description': fake.paragraph(nb_sentences=2),
                'steps': fake.paragraph(nb_sentences=15, variable_nb_sentences=False),
                'category': sample(categories, 1)[0]['pk'],
                'tag': sample(tags, 1)[0]['pk'],
                'user': 1
            }
        ))

        for _ in range(10):
            ing_counter += 1
            ingredients.append(model_base("recipes.ingredient", ing_counter,
                {
                    'name': fake.word().capitalize()
                }
            ))

            amounts.append(model_base("recipes.amount", ing_counter,
                {
                    'recipe': recipes[-1]['pk'],
                    'ingredient': ingredients[-1]['pk'],
                    'amount': round(randint(0, 10) + random(), 1),
                    'unit': sample(units, 1)[0]['pk']
                }
            ))
        
        for _ in range(8):
            rev_counter += 1
            reviews.append(model_base("recipes.review", rev_counter,
                {
                    'rate': 0.5,
                    'recipe': recipes[-1]['pk'],
                    'content': fake.paragraph(nb_sentences=2),
                    'user': 1
                }
            ))
        
        for _ in range(5):
            fav_counter +=1
            favorites.append(model_base("recipes.favorite", fav_counter,
                {
                    'recipe': recipes[-1]['pk'],
                    'user': 1
                }
            ))

    build_fixture("recipes", recipes)
    build_fixture("ingredients", ingredients)
    build_fixture("amounts", amounts)
    build_fixture("reviews", reviews)
    build_fixture("favorites", favorites)


def main():
    recipes_seeder()

main()