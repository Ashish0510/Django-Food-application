# Generated by Django 4.0.4 on 2022-05-10 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chotaapp', '0008_alter_cart_product_alter_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=False, max_length=300, null=True)),
                ('add', models.CharField(default=False, max_length=300, null=True)),
                ('district', models.CharField(default=False, max_length=300, null=True)),
                ('state', models.CharField(default=False, max_length=300, null=True)),
                ('pincode', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
