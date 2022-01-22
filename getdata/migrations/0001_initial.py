# Generated by Django 3.2.11 on 2022-01-22 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Naver_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_email', models.CharField(default='', max_length=320)),
                ('title', models.CharField(default='', max_length=300)),
                ('price', models.IntegerField(default=0)),
                ('delivery', models.IntegerField(default=0)),
                ('price_sum_delivery', models.IntegerField(default=0)),
                ('org_thumbnail', models.CharField(default='', max_length=2000)),
                ('sub_thumbnail', models.CharField(default='', max_length=2000)),
                ('img_detailed', models.CharField(default='', max_length=2000)),
                ('cannel_id', models.CharField(default='', max_length=300)),
                ('product_id', models.CharField(default='', max_length=300)),
                ('date', models.DateField()),
                ('img_width', models.IntegerField(default=0)),
                ('img_height', models.IntegerField(default=0)),
                ('three_day', models.IntegerField(default=0)),
                ('six_mon', models.IntegerField(default=0)),
                ('review', models.IntegerField(default=0)),
                ('review_score', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Problem_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_email', models.CharField(max_length=320)),
                ('product_num', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=320)),
                ('etitle', models.CharField(max_length=50)),
                ('product_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Prohibition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=320)),
                ('admin_email', models.CharField(max_length=320)),
                ('keyword', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Secret_Key',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_email', models.CharField(max_length=320)),
                ('key', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Sourcing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_title', models.CharField(max_length=300)),
                ('tag', models.CharField(max_length=300)),
                ('constructor', models.CharField(max_length=300)),
                ('manager', models.CharField(max_length=300)),
                ('change_thumbnail', models.CharField(max_length=2000)),
                ('status', models.IntegerField(default=0)),
                ('date', models.DateTimeField()),
                ('cannel_id', models.CharField(max_length=100)),
                ('product_id', models.CharField(default='', max_length=300)),
                ('admin_email', models.CharField(max_length=320)),
                ('item_id', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=320)),
                ('nickname', models.CharField(max_length=30)),
                ('admin', models.BooleanField()),
                ('admin_email', models.CharField(max_length=320)),
                ('tax', models.FloatField(default=1.2)),
                ('goods_max', models.IntegerField(default=9999999)),
                ('goods_day', models.IntegerField(default=90)),
                ('three_day', models.IntegerField(default=3)),
                ('six_mon_s', models.IntegerField(default=1)),
                ('six_mon_e', models.IntegerField(default=10)),
                ('review_s', models.IntegerField(default=0)),
                ('review_e', models.IntegerField(default=10)),
                ('price_max', models.IntegerField(default=9999999)),
                ('price_min', models.IntegerField(default=1)),
                ('problem_product', models.BooleanField(default=True)),
                ('status', models.CharField(default='', max_length=50)),
                ('jab', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sourcing_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('korTitle', models.CharField(max_length=300)),
                ('margin', models.IntegerField(default=0)),
                ('weightPrice', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=0)),
                ('memo', models.CharField(max_length=1000)),
                ('isClothes', models.BooleanField(default=False)),
                ('isShoes', models.BooleanField(default=False)),
                ('brand', models.CharField(max_length=300)),
                ('sourcing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.sourcing')),
            ],
            options={
                'db_table': 'sourcing_product',
            },
        ),
        migrations.CreateModel(
            name='Sourcing_Option_Deep_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(max_length=300)),
                ('sale_price', models.CharField(max_length=300)),
                ('origin_price', models.CharField(max_length=300)),
                ('skuid', models.CharField(max_length=300)),
                ('stock', models.CharField(max_length=300)),
                ('sourcing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.sourcing')),
            ],
            options={
                'db_table': 'sourcing_option_deep_category',
            },
        ),
        migrations.CreateModel(
            name='Sourcing_Option_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=300)),
                ('ctg_name', models.CharField(max_length=300)),
                ('ctg_korTypeName', models.CharField(max_length=2000)),
                ('vid', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=300)),
                ('korTypeName', models.CharField(max_length=300)),
                ('image', models.CharField(max_length=2000)),
                ('select', models.BooleanField(default=False)),
                ('sourcing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.sourcing')),
            ],
            options={
                'db_table': 'sourcing_option_category',
            },
        ),
        migrations.CreateModel(
            name='Main_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(max_length=2000)),
                ('sourcing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.sourcing')),
            ],
            options={
                'db_table': 'main_images',
            },
        ),
        migrations.CreateModel(
            name='Content_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(max_length=2000)),
                ('sourcing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.sourcing')),
            ],
            options={
                'db_table': 'content_images',
            },
        ),
    ]
