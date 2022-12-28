from django import template
from django.utils.safestring import mark_safe
import math

register = template.Library()

@register.simple_tag
def star_rating(points):
    filled_stars = float(points) if points else 0.0

    half_star = 0

    stars_html = "<div class='stars mx-auto'>"

    if filled_stars > 5:
        filled_stars = 5
    elif filled_stars % 1 != 0:
        if filled_stars % 1 >= 0.5:
            half_star = 1
        filled_stars = math.floor(filled_stars)

    empty_stars = 5 - filled_stars - half_star

    for _ in range(int(filled_stars)):
        stars_html += "<i class='fas fa-star'></i>"

    for _ in range(int(half_star)):
        stars_html += "<i class='fas fa-star-half-alt'></i>"
    
    for _ in range(int(empty_stars)):
        stars_html += "<i class='far fa-star'></i>"

    stars_html += "</div>"
    
    return mark_safe(stars_html)

@register.simple_tag
def favorite_mark(user_obj, recipe_id, css_class):
    if user_obj.favorite_set.filter(recipe_id=recipe_id).count() > 0:
        heart = f"<button type='button' class='btn btn-link p-0'><i id='heart-{recipe_id}' class='fas fa-heart {css_class}'></i></button>"
    else:
        heart = f"<button type='button' class='btn btn-link p-0'><i id='heart-{recipe_id}' class='far fa-heart {css_class}'></i></button>"
    return mark_safe(heart)