import scrapy
from pbpdata.models import Team


class PlayerSpider(scrapy.Spider):
    name = "player"

    start_urls = [
        'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20037',
    ]

    def parse(self, response):
        players = response.css('.dataRow')
        team = Team.objects.get(tbc_team_id=20037)
        for player in players:
            cols = player.css('td')
            yield {
                'tbc_player_id': cols[1].css('a::attr(href)')[
                    0].re_first(r'(?<=ID=)\w+'),
                'first_name': cols[1].css('a::text')[0].re_first(r'^\w+'),
                'last_name': cols[1].css('a::text')[
                    0].re_first(r'(?<= )[\w\']+'),
                'handedness': cols[5].css('::text').extract_first(),
                'team': team
            }
