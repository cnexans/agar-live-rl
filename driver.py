from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from constants import chromedriverPathExecutable, gameUrl, defaultBotName, adblockExtension, browserFrameHeight, taskbarHeight
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import numpy as np
import pyautogui


class AgarLiveWebdriver():
    def __init__(self, botName = defaultBotName, start = True):
        self.botName = botName
        self.velocityFactors = {
            'fast': 500,
            'balanced': 250,
            'slow': 100
        }
        self.__createWebdriver()
        screenWidth, screenHeight = pyautogui.size()
        self.ballCenter = {
            'x': screenWidth // 2,
            'y': (screenHeight - browserFrameHeight - taskbarHeight) // 2 + browserFrameHeight
        }
        if start:
            self.__deactivateAds()
            self.__startGame()

    def flush(self):
        self.driver.close()

    def move(self, angle, velocity):
        # Move to given direction
        velocityFactor = self.velocityFactors[velocity]
        y = int(velocityFactor * np.sin(angle))
        x = int(velocityFactor * np.cos(angle))
        pyautogui.moveTo(self.ballCenter['x'] + x, self.ballCenter['y'] - y)
        
    def __isGameDone(self):
        driver = self.driver
        try:
            driver.find_element_by_id('statsContinue')
            return False
        except NoSuchElementException:
            return True

    def __startGame(self):
        driver = self.driver
        botName = self.botName

        wait = WebDriverWait(driver, 10)

        # Enter nickname
        nickInput = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "[id='nick']")))
        nickInput.send_keys(botName)
        time.sleep(4)

        # Start to play!
        playButton = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-play-guest[type='submit']")))
        playButton.click()
        time.sleep(4)

    def __createWebdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f"load-extension={adblockExtension}");
        self.driver = webdriver.Chrome(chromedriverPathExecutable, options = options)
        self.driver.maximize_window()

    def __deactivateAds(self):
        driver = self.driver
        driver.get(gameUrl)
        if len(driver.window_handles) > 1:
            driver.switch_to_window(driver.window_handles[1])
            time.sleep(4)
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        time.sleep(4)
