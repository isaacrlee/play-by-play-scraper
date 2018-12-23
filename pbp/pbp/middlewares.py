# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from pbp.items import PlayerItem
import re


class PbpSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        if spider.name == 'player':
            for r in result:
                pattern = re.compile(r'(?<=-)\w')
                search = re.search(pattern, r['handedness'])
                ph = search.group(0) if search else 'U'

                pattern = re.compile(r'\w(?=-)')
                search = re.search(pattern, r['handedness'])
                bh = search.group(0) if search else 'U'

                yield PlayerItem(
                    tbc_player_id=r['tbc_player_id'],
                    pitcher_handedness=ph,
                    batter_handedness=bh,
                    first_name=r['first_name'],
                    last_name=r['last_name'],
                    team=r['team']
                )
            return

        if spider.name != 'pbp':
            for r in result:
                yield r
            return

        d = []
        pbp = list(result)
        info = pbp[0]
        # info['away_team'] = team_ids[info['away_team']]
        # info['home_team'] = team_ids[info['home_team']]
        pitcher_against = {
            info['away_team']: info['home_starting_pitcher'],
            info['home_team']: info['away_starting_pitcher']
        }

        for half_inning in pbp[1:]:
            d.extend([{
                'half_inning': half_inning['half_inning'],
                'play': p,
                'offense_team': half_inning['offense_team']
            } for p in half_inning['plays']])

        # REMOVE 'NO PLAY'
        d = list(filter(lambda a: a['play'] != 'No play.', d))

        # Extract pa_result and batted_ball_location
        for play in d:
            play['pitcher'] = pitcher_against[play['offense_team']]
            # get name
            pattern = r"(\w+'?\w+\,[A-Z]|\w+'?\w+,\s[A-Z].|\w+'?\w+)"
            match = re.match(pattern, play['play'])
            if bool(match):
                play['name'] = match.group(0)
            else:
                print('No name')

            # get pitcher substitution
            pattern = r"to p for"
            match = re.search(pattern, play['play'])
            if bool(match):
                pitcher_against[play['offense_team']] = play['name']

            # if possible, get result
            # stolen base
            pattern = r"(stole)"
            match = re.search(pattern, play['play'])
            if bool(match):
                pa_result = match.group(0)

            # struck out looking, struck out swinging, walked, hit by pitch
            pattern = r"(struck out looking|struck out swinging|walked|hit by pitch)"
            match = re.search(pattern, play['play'])

            if bool(match):
                pa_result = match.group(0)

            # ground, lined, flied ...
            pattern = r"(grounded|lined|flied|popped|reached|singled|doubled|tripled|homered).*(p|1b|2b|3b|ss|lf|cf|rf|left field|center field|right field|first base|second base|third base|left center|right center|left side|middle|right side)\b"
            match = re.search(pattern, play['play'])

            if bool(match):
                pa_result = match.group(1)
                batted_ball_location = match.group(2)

            # double play
            pattern = r"(grounded|lined|flied|popped|reached|singled|doubled|tripled|homered).*(?<!to )(p|1b|2b|3b|ss|lf|cf|rf)\b"
            match = re.search(pattern, play['play'])

            if bool(match):
                batted_ball_location = match.group(2)

            if batted_ball_location:
                #         print(name, pa_result, batted_ball_location)
                play['pa_result'] = pa_result
                play['batted_ball_location'] = batted_ball_location
            else:
                #         print(name, pa_result)
                play['pa_result'] = pa_result

            name = ''
            pa_result = ''
            batted_ball_location = ''

        # Must return an iterable of Request, dict or Item objects.
        for i in d:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PBPDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
