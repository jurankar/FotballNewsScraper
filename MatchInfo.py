import datetime


class MatchInfo:
    def __init__(self, capture_dates, match_odds_history, teams_competing):
        self.capture_dates = capture_dates
        self.match_odds_history = match_odds_history
        self.teams_competing = teams_competing