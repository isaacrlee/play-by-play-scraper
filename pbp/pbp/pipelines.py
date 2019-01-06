# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .settings import db

class PbpPipeline(object):
    def process_item(self, item, spider):
        # Uncomment to build your own Firebase database
        # if spider.name == 'team':
        #     db.child('teams').child(item['tbc_team_id']).set(item)
        # if spider.name == 'player':
        #     db.child("players").child(item['tbc_player_id']).set(item)
        #     # db.child("players").child(item['tbc_player_id']).update(item)
        # if spider.name == 'pbp':
        #     db.child("plays").push(item)
        return item