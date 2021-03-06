# Generated by Django 2.1 on 2018-10-08 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0003_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptitle', models.CharField(max_length=50, verbose_name='图片标题')),
                ('imgurl', models.ImageField(upload_to='static/pimg')),
            ],
            options={
                'verbose_name': '图片管理',
                'verbose_name_plural': '图片管理',
                'db_table': 'my_picture',
            },
        ),
    ]
