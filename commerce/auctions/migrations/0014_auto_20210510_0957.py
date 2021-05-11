# Generated by Django 3.1.7 on 2021-05-10 13:57

import auctions.modelsview
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20210430_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='Ends',
            field=models.DateTimeField(validators=[auctions.modelsview.is_auction_active]),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='Starting Price',
            field=models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0, message="Price can't be below zero (0)")]),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='auctioneer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='offer',
            field=models.DecimalField(decimal_places=2, max_digits=9, validators=[auctions.modelsview.check_bid]),
        ),
    ]