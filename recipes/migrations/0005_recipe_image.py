# Generated by Django 4.1.4 on 2022-12-28 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_review_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, upload_to='recipes/'),
        ),
    ]
