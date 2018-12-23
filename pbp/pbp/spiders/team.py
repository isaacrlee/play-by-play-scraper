import scrapy
from pbp.items import TeamItem

class TeamSpider(scrapy.Spider):
    name = "team"

    start_urls = [
        'http://thebaseballcube.com/college/teams.asp?L=1',
    ]

    def parse(self, response):
        teams = response.css('.dataRow')

        for team in teams:
            cols = team.css('td')
            yield TeamItem(
                tbc_team_id = cols[0].css('a::attr(href)')[0].re_first(r'(?<=T=)\w+'),
                name = cols[0].css('a::text')[0].extract(),
                nickname = cols[1].css('a::text')[0].extract(),
                conference = cols[2].css('a::text')[0].extract()
            )
