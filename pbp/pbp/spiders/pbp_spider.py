import scrapy
import re
from ..northwestern_games import northwestern_games
from ..settings import team_index, db
from urllib.parse import urlparse, parse_qs


class PbpSpider(scrapy.Spider):
    name = "pbp"

    # CUSTOM: Northwestern Games
    start_urls = northwestern_games

    def parse(self, response):
        teams = response.css('article.box-score h1 span::text').re(
            r'(^[\w\s]+|(?<=# \d\d )[\w\s]+|(?<=# \d )[\w\s]+)')

        # CUSTOM: Searching for UIC doesn't return Illinois-Chicago
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

        away_starting_pitcher = PbpSpider.parse_starting_pitcher(away_pitching_statistics_table.css(
            away_starting_pitcher_css).extract_first()).strip()
        home_starting_pitcher = PbpSpider.parse_starting_pitcher(home_pitching_statistics_table.css(
            home_starting_pitcher_css).extract_first()).strip()

        yield {
            'game_id': PbpSpider.get_game_id(response.request.url),
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
    @staticmethod
    def parse_starting_pitcher(s):
            # Remove Win-Loss Record: First Last (W, 1-0) -> First Last
            pattern = re.compile(r" (\([WLS])")
            match = re.search(pattern, s)
            if bool(match):
                s = s[:s.index(match.group(0))]
            return s

    @staticmethod
    def get_game_id(url):
        o = urlparse(url)
        try:
            params = parse_qs(o.query)
            try:
                return int(params['id'][0])
            except:
                raise Exception('No id: {}'.format(params))
        except:
            raise Exception('No Query: {}'.format(o))