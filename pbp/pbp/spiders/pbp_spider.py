import scrapy

class PbpSpider(scrapy.Spider):
    name = "pbp"

    start_urls = [
        'https://nusports.com/boxscore.aspx?path=baseball&id=13350',
    ]

    def parse(self, response):
        pitching_statistics = response.css('section[aria-label="Team Individual Pitching Statistics"]')
        away_pitching_statistics_table = pitching_statistics.css('table')[0]
        home_pitching_statistics_table = pitching_statistics.css('table')[1]
        teams = response.css('article.box-score h1 span::text').extract()
        yield {
            'away_starting_pitcher': away_pitching_statistics_table.css('tbody th a::text').re_first(r'^(\w+,? \w+)') if away_pitching_statistics_table.css('tbody th a') else away_pitching_statistics_table.css('tbody th::text').re_first(r'^(\w+,? \w+)'),
            'home_starting_pitcher': home_pitching_statistics_table.css('tbody th a::text').re_first(r'^(\w+,? \w+)') if home_pitching_statistics_table.css('tbody th a') else home_pitching_statistics_table.css('tbody th::text').re_first(r'^(\w+,? \w+)'),
            'away_team': teams[0],
            'home_team': teams[1]
        }
        for half_inning in response.css('div#inning-all table.play-by-play'):
            yield {
                'half_inning': half_inning.css('caption::text').extract_first(),
                'offense_team': half_inning.css('caption::text').re_first(r'^\w+'),
                'plays': half_inning.css('th[scope=row]::text').extract()
            }
