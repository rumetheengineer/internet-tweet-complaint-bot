from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

load_dotenv()

# Internet speed threshold in Mbps
UPLOAD_SPEED = 20
DOWNLOAD_SPEED = 20

# Twitter credentials from environment variables
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASS = os.getenv("TWITTER_PASS")
TWITTER_USER = os.getenv("TWITTER_USER")
ISP_TWITTER_HANDLE = os.getenv("ISP_TWITTER_HANDLE")


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.down = 0
        self.up = 0
        self.get_internet_speed()
        self.check_speed()

    def get_internet_speed(self):
        self.driver.get(url="https://www.speedtest.net/")
        self.driver.maximize_window()

        time.sleep(5)
        go = self.driver.find_element(By.XPATH, value="//div[2]/div/div[2]/a/span[4]")
        go.click()
        time.sleep(90)

        up_speed = self.driver.find_element(By.CLASS_NAME, value='upload-speed')
        down_speed = self.driver.find_element(By.CLASS_NAME, value='download-speed')
        self.up = float(up_speed.text)
        self.down = float(down_speed.text)
        self.driver.quit()
        print(f"Upload Speed: {self.up} Mbps")
        print(f"Download Speed: {self.down} Mbps")
        return self.up, self.down

    def check_speed(self):
        if self.up <= UPLOAD_SPEED or self.down <= DOWNLOAD_SPEED:
            print("Internet speed is below the expected threshold.")
            self.tweet_complaint()
            return False
        else:
            print("Internet speed is acceptable.")
            self.driver.quit()
            return True

    def tweet_complaint(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url="https://x.com/i/flow/login")
        wait = WebDriverWait(self.driver, 20)

        email = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)

        try:
            password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        except TimeoutException:
            username =wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username.send_keys(TWITTER_USER)
            username.send_keys(Keys.ENTER)
            password = wait.until(EC.presence_of_element_located((By.NAME, "password")))

        password.send_keys(TWITTER_PASS)
        password.send_keys(Keys.ENTER)

        wait = WebDriverWait(self.driver, 20)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Home']")))
            # Trying multiple selectors for the tweet box
            try:
                tweet_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Tweet text']")))
            except TimeoutException:
                tweet_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox']")))

            tweet_box.click()
            tweet = (f"Hey Internet Provider, {ISP_TWITTER_HANDLE}, why is my internet speed"
                     f" {self.down}down/{self.up}up when my package claims to be 20Mbps?")
            tweet_box.send_keys(tweet)

            tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='tweetButtonInline']")))
            tweet_button.click()
        except TimeoutException:
            print("Could not find tweet box or button. Here is the page source for debugging:")
            print(self.driver.page_source)
        else:
            print("Tweet sent successfully!")
        finally:
            time.sleep(5)
            self.driver.quit()
            return


new = InternetSpeedTwitterBot()
