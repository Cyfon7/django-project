# Generated by Django 4.1.4 on 2022-12-24 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipe_user_review_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='visit_counter',
            field=models.IntegerField(default=0),
        ),
    ]