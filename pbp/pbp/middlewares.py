# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .settings import db
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

                yield {
                    'tbc_player_id': r['tbc_player_id'],
                    'pitcher_handedness': ph,
                    'batter_handedness': bh,
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'tbc_team_id': r['tbc_team_id']
                }
            return

        elif spider.name == 'pbp':
            def get_player_id_from_od(first_name, last_name, od):
                for player_id, v in od.items():
                    if v['last_name'].lower() == last_name.lower():
                        if first_name:
                            if first_name.lower() in v['first_name'].lower():
                                return player_id
                        else:
                            return player_id
                raise Exception('Player Not Found: {} {}'.format(first_name, last_name))

            def get_player_id_from_od_and_string(s, od):
                name_dict = get_first_and_last_name(s)
                return get_player_id_from_od(
                    name_dict['first_name'],
                    name_dict['last_name'],
                    od
                )

            def get_defense_team_from_info(offense_team, info):
                if offense_team == info['away_team']:
                    return info['home_team']
                elif offense_team == info['home_team']:
                    return info['away_team']
                raise Exception('offense_team is not away or home team')

            def get_first_and_last_name(s):
                d = {}
                if ' ' in s and ',' in s and '.' in s:
                    # Dunn, J.
                    pattern = re.compile(r"([\w']+), ((?<= )[\w']+)")
                    match = re.match(pattern, s)
                    if bool(match) and len(match.groups()) == 2:
                        d['first_name'] = match.group(2)
                        d['last_name'] = match.group(1)
                elif ' ' in s and ',' in s:
                    # O'Laughlin, Casey
                    pattern = re.compile(r"([\w']+), ((?<= )[\w']+)")
                    match = re.match(pattern, s)
                    if bool(match) and len(match.groups()) == 2:
                        d['first_name'] = match.group(2)
                        d['last_name'] = match.group(1)
                elif ' ' in s:
                    # Grant Suponchick
                    pattern = re.compile(r"([\w'.]+) ([\w']+)")
                    match = re.match(pattern, s)
                    if bool(match) and len(match.groups()) == 2:
                        d['first_name'] = match.group(1)
                        d['last_name'] = match.group(2)
                elif ',' in s:
                    # Thibodeau,C
                    pattern = re.compile(r"([\w']+),([\w']+)")
                    match = re.match(pattern, s)
                    if bool(match) and len(match.groups()) == 2:
                        d['first_name'] = match.group(2)
                        d['last_name'] = match.group(1)
                else:
                    d['first_name'] = ''
                    d['last_name'] = s
                return d

            def get_result(s):
                STOLENBASE = 'SB'
                SINGLE = '1B'
                DOUBLE = '2B'
                TRIPLE = '3B'
                HOMERUN = 'HR'
                GROUNDOUT = 'G'
                LINEOUT = 'L'
                FLYOUT = 'F'
                ERRORORFIELDERSCHOICE = 'E/FC'
                STRIKEOUT = 'K'
                WALK = 'BB'
                HITBYPITCH = 'HBP'
                UNKNOWN = 'UNKNOWN'

                results = {
                    'stole': STOLENBASE,
                    'singled': SINGLE,
                    'doubled': DOUBLE,
                    'tripled': TRIPLE,
                    'homered': HOMERUN,
                    'grounded': GROUNDOUT,
                    'lined': LINEOUT,
                    'flied': FLYOUT,
                    'popped': FLYOUT,
                    'reached': ERRORORFIELDERSCHOICE,
                    'struck out looking': STRIKEOUT,
                    'struck out swinging': STRIKEOUT,
                    'walked': WALK,
                    'hit by pitch': HITBYPITCH,
                }

                if s in results:
                    return results[s]

                return UNKNOWN

            def get_location(s):
                PITCHER = 'P'
                FIRSTBASE = '1B'
                SECONDBASE = '2B'
                THIRDBASE = '3B'
                SHORTSTOP = 'SS'
                LEFTFIELD = 'LF'
                CENTERFIELD = 'CF'
                RIGHTFIELD = 'RF'
                LEFTCENTER = 'LC'
                RIGHTCENTER = 'RC'
                LEFTSIDE = 'LS'
                MIDDLE = 'M'
                RIGHTSIDE = 'RS'
                UNKNOWN = 'UNKNOWN'

                locations = {
                    'p': PITCHER,
                    '1b': FIRSTBASE,
                    'first base': FIRSTBASE,
                    '2b': SECONDBASE,
                    'second base': SECONDBASE,
                    '3b': THIRDBASE,
                    'third base': THIRDBASE,
                    'ss': SHORTSTOP,
                    'lf': LEFTFIELD,
                    'left field': LEFTFIELD,
                    'cf': CENTERFIELD,
                    'center field': CENTERFIELD,
                    'rf': RIGHTFIELD,
                    'right field': RIGHTFIELD,
                    'left center': LEFTCENTER,
                    'right center': RIGHTCENTER,
                    'left side': LEFTSIDE,
                    'middle': MIDDLE,
                    'right side': RIGHTSIDE,
                }

                if s in locations:
                    return locations[s]

                return UNKNOWN

            pbp = list(result)
            info = pbp[0]
            d = list(filter(lambda a: a['play'] != 'No play.', pbp[1:]))

            info['away_starting_pitcher'] = get_player_id_from_od_and_string(
                info['away_starting_pitcher'], info['players'][info['away_team']])
            info['home_starting_pitcher']=get_player_id_from_od_and_string(
                info['home_starting_pitcher'], info['players'][info['home_team']])

            pitcher_against={
                info['away_team']: info['home_starting_pitcher'],
                info['home_team']: info['away_starting_pitcher']
            }

            for play in d:
                # add pitcher col
                play['pitcher'] = pitcher_against[play['offense_team']]

                # update pitcher_against
                pattern = r"(\w+'?\w+\,[A-Z]|\w+'?\w+,\s[A-Z].|\w+'?\w+)(?= to p for)"
                match = re.search(pattern, play['play'])
                if bool(match):
                    defense_team = get_defense_team_from_info(
                        play['offense_team'], info)
                    pitcher_against[play['offense_team']]=get_player_id_from_od_and_string(
                        match.group(0), info['players'][defense_team])
                    continue

                # catch substitutions
                pattern=r"(\w+'?\w+\,[A-Z]|\w+'?\w+,\s[A-Z].|\w+'?\w+)(?= to (1b|2b|3b|ss|lf|cf|rf) for)"
                match=re.search(pattern, play['play'])
                if bool(match):
                    continue

                # add name col
                pattern=r"(\w+'?\w+\,[A-Z]|\w+'?\w+,\s[A-Z].|\w+'?\w+)"
                match=re.match(pattern, play['play'])
                if bool(match):
                    play['name']=get_player_id_from_od_and_string(
                        match.group(0), info['players'][play['offense_team']])
                else:
                    raise Exception('No Name: {}'.format(play['play']))

                # add pa_result col
                    # stole
                pattern=r"(stole)"
                match=re.search(pattern, play['play'])
                if bool(match):
                    play['pa_result']=get_result(match.group(0))

                    # struck out looking, struck out swinging, walked, hit by pitch
                pattern=r"(struck out looking|struck out swinging|walked|hit by pitch)"
                match=re.search(pattern, play['play'])

                if bool(match):
                    play['pa_result']=get_result(match.group(0))

                    # ground, lined, flied ... and batted_ball_location col
                pattern=r"(grounded|lined|flied|popped|reached|singled|doubled|tripled|homered).*(p|1b|2b|3b|ss|lf|cf|rf|left field|center field|right field|first base|second base|third base|left center|right center|left side|middle|right side)\b"
                match=re.search(pattern, play['play'])

                if bool(match):
                    play['pa_result']=get_result(match.group(1))
                    play['batted_ball_location']=get_location(match.group(2))

                # batted_ball_location for double play
                pattern=r"(grounded|lined|flied|popped|reached|singled|doubled|tripled|homered).*(?<!to )(p|1b|2b|3b|ss|lf|cf|rf)\b"
                match=re.search(pattern, play['play'])

                if bool(match):
                    play['batted_ball_location']=get_location(match.group(2))

                yield play

        else:
            for r in result:
                yield r
            return

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
        s=cls()
        crawler.signals.connect(
            s.spider_opened, signal = signals.spider_opened)
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
