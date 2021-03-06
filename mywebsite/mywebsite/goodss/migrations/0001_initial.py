# Generated by Django 2.1 on 2018-10-02 04:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccount', models.IntegerField(verbose_name='购买数量')),
                ('totalprice', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='总价')),
                ('cstastus', models.BooleanField(default=False, verbose_name='购物车状态')),
            ],
            options={
                'verbose_name': '购物车管理',
                'verbose_name_plural': '购物车管理',
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('gtype', models.CharField(max_length=50, null=True, verbose_name='商品类型')),
                ('desc', models.TextField(verbose_name='商品描述')),
                ('units', models.CharField(max_length=20, verbose_name='单位')),
                ('gpicture', models.ImageField(upload_to='gimg', verbose_name='商品图片')),
                ('gprice', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('gstatus', models.IntegerField(choices=[(1, '上架'), (2, '审核'), (3, '下架'), (4, '非卖品')], default=2, verbose_name='商品状态')),
            ],
            options={
                'verbose_name': '商品管理',
                'verbose_name_plural': '商品管理',
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderno', models.CharField(max_length=80, verbose_name='订单号码')),
                ('ocals', models.TextField(verbose_name='商品订单详细')),
                ('address', models.CharField(max_length=200, verbose_name='送货地址地址')),
                ('ostatus', models.IntegerField(choices=[(1, '等待支付'), (2, '已支付'), (3, '订单已取消')], default=1, verbose_name='订单状态')),
                ('ogid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='goodss.Goods', verbose_name='购买的商品')),
                ('ouid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='购买用户')),
            ],
            options={
                'verbose_name': '订单管理',
                'verbose_name_plural': '订单管理',
                'db_table': 'order',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='cgid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='goodss.Goods', verbose_name='购买的商品'),
        ),
        migrations.AddField(
            model_name='cart',
            name='cuid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='购买用户'),
        ),
    ]
