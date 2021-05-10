# BASICS
import datetime
import time
import requests
import random
import pickle

# SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# GRAPHS
import plotly.graph_objects as go
import plotly.io as pio

from News import News

# DRIVER = webdriver.Chrome("chromedriver.exe")


# Some names are different on website and our odds records  --> in this function we fix old_news team names to fit old_odds
def clean_team_name(team_name):
    if team_name[:2] == "/D" or team_name[:2] == "/M":
        team_name = team_name[2:]

    if team_name == "Brighton & Hove Albion":
        team_name = "Brighton and Hove Albion"

    if team_name == "Wolverhampton":
        team_name = "Wolverhampton Wanderers"

    if "West Brom" in team_name:
        team_name = "West Bromwich Albion"

    return team_name

def print_all_team_names():
    old_news = open_pkl("old_news.pkl")
    old_odds = open_pkl("old_odds.pkl")

    # print all team names in old_odds
    team_names_odds = []
    for odds_scan in old_odds:
        for match in odds_scan["request_data"]:
            if match["teams"][0] not in team_names_odds:
                team_names_odds.append(match["teams"][0])
            if match["teams"][1] not in team_names_odds:
                team_names_odds.append(match["teams"][1])
    team_names_odds.sort()
    print("old_odds teams:")
    print(team_names_odds)

    # print all team names in old_news
    teams_names_news = []
    for news in old_news:
        if clean_team_name(news.team_name) not in teams_names_news:
            teams_names_news.append(clean_team_name(news.team_name))
    teams_names_news.sort()
    print("\n\nold_news teams:")
    print(teams_names_news)







def get_latest_news(old_news):
    new_news = []
    # print("scanning for news")
    chrome_optionsss = Options()

    # Open the news site
    DRIVER.get("https://www.rotowire.com/soccer/news.php?league=1")
    WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(random.uniform(4.3, 6.9))

    # List all the news
    news = DRIVER.find_elements_by_class_name("news-update")
    for i in news:
        news_headline = i.find_element_by_class_name("news-update__headline").text
        if news_headline == "":
            break

        news_are_new = True
        for j in old_news:
            j_news_headline = j.news_headline
            if j_news_headline == news_headline:
                news_are_new = False
                break

        if news_are_new:
            new_news.append(i)

    return new_news


def run_scanner(old_news):
    new_news = get_latest_news(old_news)
    for news in new_news:
        #analyse_news(i)
        player_name = news.find_element_by_class_name("news-update__player-link").text
        team_name = news.find_element_by_class_name("news-update__meta").find_elements_by_tag_name("div")[0].text[1:]
        news_headline = news.find_element_by_class_name("news-update__headline").text
        news_text = news.find_element_by_class_name("news-update__news").text
        date_on_website = news.find_element_by_class_name("news-update__timestamp").text
        try:
            injury_status = news.find_element_by_class_name("news-update__inj").text
        except:
            injury_status = False

        news_to_add = News(player_name, team_name, news_headline, news_text, date_on_website, injury_status)
        old_news.append(news_to_add)
    return old_news



def get_odds(old_odds, api_key):

    req = requests.get("https://api.the-odds-api.com/v3/odds/?apiKey=" + api_key + "&sport=soccer_epl&region=uk&mkt=h2h").json()
    if req["success"] == "false":
        print("Status: " + req["status"])
        print("Msg: " + req["msg"])

    data = req["data"]
    # for match in data:
    #     print("Teams: " + match["teams"][0] + " : " + match["teams"][1])
    #     print("Odds:  1:" + str(match["sites"][0]["odds"]["h2h"][0]) + " | 0:" + str(match["sites"][0]["odds"]["h2h"][1]) + " | 2:" + str(match["sites"][0]["odds"]["h2h"][2]) + "\n\n")    # TODO swithc 0 to some particular site

    curr_odds = {}
    curr_odds["date_captured"] = datetime.datetime.now()
    curr_odds["request_data"] = data

    old_odds.append(curr_odds)
    return old_odds


def open_pkl(filename):
    try:
        with open(filename, 'rb') as input:
            array = pickle.load(input)
    except:
        array = []
    return array

def write_pkl(filename, array):
    with open(filename, 'wb') as output:
        pickle.dump(array, output, pickle.HIGHEST_PROTOCOL)


def capture_data():
    API_KEYS = ["9d72a9036fddbe605e78611480bfc9ae", "c85365bd502f040a8ad6c98fd813b26e", "a0b0c30b16620276f351ee9f00ab529d"]
    api_key_index = 0

    # we open old news and old odds
    old_news = open_pkl("old_news.pkl")
    old_odds = open_pkl("old_odds.pkl")

    loop_counter = 0
    while True:

        if loop_counter != 0 and loop_counter%498 == 0:
            api_key_index += 1
            api_key_index = 0 if api_key_index == 3 else api_key_index  # we come full circle


        old_news = run_scanner(old_news)
        old_odds = get_odds(old_odds, API_KEYS[api_key_index])

        if loop_counter != 0 and loop_counter%5 == 0:
            print("start writing")
            write_pkl("old_odds.pkl", old_odds)
            write_pkl("old_news.pkl", old_news)
            print("finish writing")

        loop_counter += 1
        time.sleep(1800)

# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
def show_graph(x_axis, y_axis, title):
    data = [go.Scatter(x=x_axis, y=y_axis)]
    layout = go.Layout(title=go.layout.Title(text=title))
    fig = go.Figure(data, layout)
    fig.show()

def get_team_odds_over_time(old_odds, team_name, betting_site_name="marathonbet"):
    match_odds_history = []
    capture_dates = []
    matches_commence_times = []    # we use this to serperate matches of this team
    teams_competing = []

    for odds_captured in old_odds:
        date = odds_captured["date_captured"]
        capture_dates.append(date)
        for match in odds_captured["request_data"]:
            if team_name in match["teams"]:
                # add commence time if not already added
                if match["commence_time"] not in matches_commence_times:
                    matches_commence_times.append(match["commence_time"])
                    match_odds_history.append([])   # we append a new array of data for each match
                    teams_competing.append(match["teams"])

                # find out whitch match are we looking at --> the match_commence_time index cooresponds with the index of the array in match_odds_history we need
                match_index = matches_commence_times.index(match["commence_time"])

                # find odds
                for betting_site in match["sites"]:
                    if betting_site["site_key"] == betting_site_name:
                        odds = betting_site["odds"]["h2h"][0]
                        match_odds_history[match_index].append(odds)
                        break

    return [capture_dates, match_odds_history, teams_competing] # could be done with new class better prolly

def difference_min_max_odds(odds_over_time):
    min_val = min(odds_over_time)
    max_val = max(odds_over_time)
    difference = min_val/max_val
    return difference

def draw_selected_graphs(data, min_odds_difference, already_drawn_match_graphs):
    capture_dates = data[0]
    match_odds_history = data[1]
    teams_competing = data[2]   # in this array we save which teams were competing
    drawn_graphs = []   # here we store which matchups we drawn graphs for

    for match_index in range(len(match_odds_history)):
        if len(match_odds_history[match_index]) > 0 and difference_min_max_odds(match_odds_history[match_index]) <= min_odds_difference and teams_competing[match_index] not in already_drawn_match_graphs:
            drawn_graphs.append(teams_competing[match_index])
            match_title = teams_competing[match_index][0] + " VS " + teams_competing[match_index][1]
            show_graph(capture_dates, match_odds_history[match_index], match_title)
            print("---------------------------------------------")

    return drawn_graphs

def print_relevant_news(old_news, team_name, key_news_only = True):
    print("Printing news for " + team_name)
    for news in old_news:
        if clean_team_name(news.team_name) == team_name:
            if key_news_only:
                if news.injury_status != False:
                    print("Date: " + str(news.date_on_website) + "         " + news.news_article)
            else:
                print("Date: " + str(news.date_on_website) + "         " + news.news_article)

def analyse_news(min_odds_difference = 0.9):
    old_news = open_pkl("old_news.pkl")
    old_odds = open_pkl("old_odds.pkl")
    all_team_names = ['Arsenal', 'Aston Villa', 'Brighton and Hove Albion', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
     'Leeds United', 'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United', 'Newcastle United',
     'Sheffield United', 'Southampton', 'Tottenham Hotspur', 'West Bromwich Albion', 'West Ham United',
     'Wolverhampton Wanderers']

    already_drawn_match_graphs = [] # here we store which graphs we already showed

    # loop through all the teams
    for team_name in all_team_names:    # --> kind of inneficcient
        # get data on odds over time
        data = get_team_odds_over_time(old_odds, team_name)
        drawn_graphs = draw_selected_graphs(data, min_odds_difference, already_drawn_match_graphs)   # return a boolean, which tells us True, if we found some matches with difference_min_max_odds >= min_odds_difference
        for matchup in drawn_graphs:
            already_drawn_match_graphs.append(matchup)
            print(matchup[0] + " VS " + matchup[1])
            print_relevant_news(old_news, matchup[0], key_news_only=True)
            print_relevant_news(old_news, matchup[1], key_news_only=True)
            print("\n\n\n")



# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------

if __name__ == '__main__':
    # capture_data()
    analyse_news(0.85)



    # print_all_team_names()

# TODO For which team are the odds




























"""
def analyse_news(news):
    player_name = news.find_element_by_class_name("news-update__player-link").text
    team_name = news.find_element_by_class_name("news-update__meta").find_elements_by_tag_name("div")[0].text[1:]
    news_headline = news.find_element_by_class_name("news-update__headline").text
    news_text = news.find_element_by_class_name("news-update__news").text

    if news_headline == "":
        return "empty"

    try:
        injury_status = news.find_element_by_class_name("news-update__inj").text
    except:
        injury_status = False

    good_phrases_header = ["Starting"]
    bad_phrases_header = ["Out", "Not"]


    if injury_status != False:
        print(news_headline + "     Bad,  " + team_name + ",  " + player_name)
        return "bad"
    else:
        for i in good_phrases_header:
            if i in news_headline:
                print(news_headline + "     Good,  " + team_name + ",  " + player_name)
                return "good"

        for i in bad_phrases_header:
            if i in news_headline:
                print(news_headline + "     Bad,  " + team_name + ",  " + player_name)
                return "bad"

        print(news_headline + "     Not assigned,  " + team_name + ",  " + player_name)
        return "Not assigned"
"""
