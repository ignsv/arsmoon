# Generated by Django 3.0.8 on 2020-07-28 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bitmex', '0004_auto_20200728_0452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderID', models.CharField(help_text='Maximum length is 255 symbols', max_length=255, unique=True, verbose_name='BitMex order id')),
                ('symbol', models.CharField(help_text='Maximum length is 255 symbols', max_length=255, verbose_name='BitMex Symbol')),
                ('volume', models.FloatField(verbose_name='Bitmex volume')),
                ('timestamp', models.DateTimeField(verbose_name='BitMex timestamp')),
                ('side', models.CharField(help_text='Maximum length is 255 symbols', max_length=255, verbose_name='BitMex side')),
                ('price', models.FloatField(verbose_name='Bitmex price')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='bitmex.Account', verbose_name='ClientAccountCounter')),
            ],
        ),
    ]