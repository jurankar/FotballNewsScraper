import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests
import random
import pickle

from News import News

DRIVER = webdriver.Chrome("chromedriver.exe")

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



def get_odds(old_odds):
    API_KEY = "a0b0c30b16620276f351ee9f00ab529d"
    req = requests.get("https://api.the-odds-api.com/v3/odds/?apiKey=a0b0c30b16620276f351ee9f00ab529d&sport=soccer_epl&region=uk&mkt=h2h").json()
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

if __name__ == '__main__':

    # we open old news and old odds
    old_news = open_pkl("old_news.pkl")
    old_odds = open_pkl("old_odds.pkl")

    while True:
        old_news = run_scanner(old_news)
        write_pkl("old_news.pkl", old_news)
        old_odds = get_odds(old_odds)
        write_pkl("old_odds.pkl", old_odds)
        time.sleep(600)

# TODO news analysis