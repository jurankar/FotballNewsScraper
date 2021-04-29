import datetime


class News:
    def __init__(self, player_name, team_name, news_headline, news_article, date_on_website, injury_status):
        self.date_added = datetime.datetime.now()
        self.player_name = player_name
        self.team_name = team_name
        self.news_headline = news_headline
        self.news_article = news_article
        self.date_on_website = date_on_website
        self.injury_status = injury_status