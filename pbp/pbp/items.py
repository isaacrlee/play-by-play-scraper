# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Game(scrapy.Item):
    home_team_id = scrapy.Field()
    away_team_id = scrapy.Field()
    date = scrapy.Field()

class Play(scrapy.Item):
    offense = scrapy.Field()
    pitcher = scrapy.Field()
    player = scrapy.Field()
    pa_result = scrapy.Field()
    batted_ball_location = scrapy.Field()
