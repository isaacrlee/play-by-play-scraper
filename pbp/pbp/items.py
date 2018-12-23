# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field
from scrapy_djangoitem import DjangoItem

from pbpdata.models import Team, Player

class TeamItem(DjangoItem):
    django_model = Team

class PlayerItem(DjangoItem):
    django_model = Player