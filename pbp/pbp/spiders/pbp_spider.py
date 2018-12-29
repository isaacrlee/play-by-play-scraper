import scrapy
import re
from ..settings import team_index, db


class PbpSpider(scrapy.Spider):
    name = "pbp"

    start_urls = ['https://nusports.com/boxscore.aspx?path=baseball&id=13350',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=14097',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13351',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13352',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13353',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13354',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13355',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=15104',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13356',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13357',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13359',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13360',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13361',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13362',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13363',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13364',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13365',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13366',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13367',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13368',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13369',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13371',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13372',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13373',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13374',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13375',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13376',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13377',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13378',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13379',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13380',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13381',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13382',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13383',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13384',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13385',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13386',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13387',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13388',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13389',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13390',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13391',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13392',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13393',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13394',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13395',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13396',
                  'https://nusports.com/boxscore.aspx?path=baseball&id=13397']

    def parse(self, response):
        def parse_starting_pitcher(s):
            # Remove Win-Loss Record: First Last (W, 1-0) -> First Last
            pattern = re.compile(r" (\([WLS])")
            match = re.search(pattern, s)
            if bool(match):
                s = s[:s.index(match.group(0))]
            return s

        teams = response.css('article.box-score h1 span::text').re(
            r'(^[\w\s]+|(?<=# \d\d )[\w\s]+|(?<=# \d )[\w\s]+)')

        try:
            if teams[0] == 'UIC':
                away_team = team_index.search(
                    'Illinois-Chicago')['hits'][0]['tbc_team_id']
            else:
                away_team = team_index.search(
                    teams[0])['hits'][0]['tbc_team_id']
        except:
            raise Exception('Away Team Not Found {}'.format(teams[0]))

        try:
            if teams[1] == 'UIC':
                home_team = team_index.search(
                    'Illinois-Chicago')['hits'][0]['tbc_team_id']
            else:
                home_team = team_index.search(
                    teams[1])['hits'][0]['tbc_team_id']
        except:
            raise Exception('Home Team Not Found {}'.format(teams[1]))

        team_ids = {
            teams[0]: away_team,
            teams[1]: home_team
        }

        players = {
            away_team: db.child('players').order_by_child('tbc_team_id').equal_to(away_team).get().val(),
            home_team: db.child('players').order_by_child(
                'tbc_team_id').equal_to(home_team).get().val()
        }

        pitching_statistics = response.css(
            'section[aria-label="Team Individual Pitching Statistics"]')

        away_pitching_statistics_table = pitching_statistics.css('table')[0]
        home_pitching_statistics_table = pitching_statistics.css('table')[1]

        away_starting_pitcher_css = 'tbody th a::text' if away_pitching_statistics_table.css(
            'tbody th a') else 'tbody th::text'
        home_starting_pitcher_css = 'tbody th a::text' if home_pitching_statistics_table.css(
            'tbody th a') else 'tbody th::text'

        away_starting_pitcher = parse_starting_pitcher(away_pitching_statistics_table.css(
            away_starting_pitcher_css).extract_first()).strip()
        home_starting_pitcher = parse_starting_pitcher(home_pitching_statistics_table.css(
            home_starting_pitcher_css).extract_first()).strip()

        yield {
            'away_starting_pitcher': away_starting_pitcher,
            'home_starting_pitcher': home_starting_pitcher,
            'away_team': away_team,
            'home_team': home_team,
            'players':  players
        }

        for half_inning in response.css('div#inning-all table.play-by-play'):
            offense_team = team_ids[half_inning.css(
                'caption::text').re_first(r'^[\w\s]+(?= - )')]
            for play in half_inning.css('th[scope=row]::text').extract():
                yield {
                    'offense_team': offense_team,
                    'play': play
                }
