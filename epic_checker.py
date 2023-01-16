from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd, time
from epic_config import *
from telegram.ext import Updater
from datetime import datetime
import traceback

def fetchTheGames():
    '''Fetches epic freebie games.'''
    # 1. Constants - We need to always do this
    website = 'https://store.epicgames.com/en-US'
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(version_main=104, use_subprocess=True, options=options)
    driver.maximize_window()
    driver.get(website)
    user_agent = driver.execute_script("return navigator.userAgent;")
    print("Your user agent for this run is: ",user_agent)
    time.sleep(2)
    driver.get('https://store.epicgames.com/en-US/free-games')
    # 2. Entering
    out = []
    try:
        all_claimable_games = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,"//a[contains(@aria-label,' Free Now, ')]")))
        for game in all_claimable_games:
            game_title = str(game.text).replace('\n','').replace('FREE NOW','').replace('Free Now -',',Free until')
            game_link = str(game.get_attribute('href'))
            print(f"title: {game_title}")
            print(f"link: {game_link}")
            out.append(f"{game_title} @ {game_link}")
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
    return out