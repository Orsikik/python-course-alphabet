# Generated by Django 2.2.2 on 2019-07-09 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20190709_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsoncomments',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article', verbose_name='Article'),
        ),
        migrations.AlterField(
            model_name='commentsoncomments',
            name='parent_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Comments', verbose_name='Basecomment'),
        ),
    ]
