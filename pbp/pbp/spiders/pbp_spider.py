import scrapy
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
        teams = response.css('article.box-score h1 span::text').extract()

        away_team = team_index.search(teams[0])['hits'][0]['tbc_team_id']
        home_team = team_index.search(teams[1])['hits'][0]['tbc_team_id']

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

        yield {
            'away_starting_pitcher': away_pitching_statistics_table.css('tbody th a::text').re_first(r'^(\w+,? \w+)') if away_pitching_statistics_table.css('tbody th a') else away_pitching_statistics_table.css('tbody th::text').re_first(r'^(\w+,? \w+)'),
            'home_starting_pitcher': home_pitching_statistics_table.css('tbody th a::text').re_first(r'^(\w+,? \w+)') if home_pitching_statistics_table.css('tbody th a') else home_pitching_statistics_table.css('tbody th::text').re_first(r'^(\w+,? \w+)'),
            'away_team': away_team,
            'home_team': home_team,
            'players':  players
        }

        for half_inning in response.css('div#inning-all table.play-by-play'):
            offense_team = team_ids[half_inning.css(
                'caption::text').re_first(r'^\w+')]
            for play in half_inning.css('th[scope=row]::text').extract():
                yield {
                    'offense_team': offense_team,
                    'play': play
                }
