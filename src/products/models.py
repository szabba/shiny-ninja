# -*- coding: utf-8 -*-

import os.path
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone


class Section(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __unicode__(self):

        return self.name


class Product(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    section = models.ForeignKey(Section)
    photo = models.ImageField(
        null=True,
        upload_to=os.path.join(
            settings.BASE_DIR,
            "static/images/products"))

    def __unicode__(self):

        return self.name

    def current_price(self, shop):

        now = timezone.now()

        prices = Price.objects.filter(
            shop=shop,
            since__lte=now).order_by('-since')

        if prices.count() == 0:
            
            return None

        return prices[0]
    
    def min_current_price(self):

        shops = Shop.objects.filter(
            price__product=self)

        min_price_value = None

        prices = []
        for shop in shops:

            price = self.current_price(shop)

            if price is not None:

                if min_price_value is None:

                    min_price_value = price.value
                    prices.append(price)

                elif price.value < min_price_value:

                    min_price_value = price.value
                    prices = [price]

                elif price.value == min_price_value:

                    prices.append(price)

        return prices

class Shop(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):

        return self.name


class Price(models.Model):

    value = models.DecimalField(max_digits=5, decimal_places=2)
    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    since = models.DateField(default=timezone.now)

    def __unicode__(self):

        return "%s for %s at %s since %s" % (
            self.value, self.product,
            self.shop, self.since.strftime("%Y-%m-%d"))