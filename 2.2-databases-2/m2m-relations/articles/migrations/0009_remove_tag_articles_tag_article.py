# Generated by Django 4.1.3 on 2022-11-10 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_scope_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='articles',
        ),
        migrations.AddField(
            model_name='tag',
            name='article',
            field=models.ManyToManyField(related_name='tags', through='articles.Scope', to='articles.article'),
        ),
    ]
