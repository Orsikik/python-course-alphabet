
# Generated by Django 2.2.2 on 2019-06-28 17:20

from django.db import migrations


def update_db(apps, schema_editor):
    """ Updates titles for Article table """

    Article = apps.get_model('article', 'Article') # название прилоржения и название таблицы
    for article in Article.objects.all():
        article.title = "Data migration title"
        article.save()

class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20190704_1528'),
    ]

    operations = [
        migrations.RunPython(update_db),
    ]
