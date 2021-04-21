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
        if news_headline not in old_news:
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



def run_scanner(old_news, first_time):
    new_news = get_latest_news(old_news)
    for i in new_news:
        analyse_news(i)
        news_headline = i.find_element_by_class_name("news-update__headline").text
        old_news.append(news_headline)


if __name__ == '__main__':
    old_news = []
    run_scanner(old_news, True)
    print("\n\n\n NEW NEWS:")
    while True:
        run_scanner(old_news, False)
        time.sleep(60)

