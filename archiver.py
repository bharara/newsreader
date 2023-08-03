from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from story import Story
import logging
from datetime import date
import data_manager

class Archiver:
    stories = []

    def __init__(self, date:date):
        self.date = date.day
        self.month = date.month
        self.year = date.year
        self.logger = logging.getLogger(__name__)

    def url(self, page=1):
        return f"https://www.wsj.com/news/archive/{self.year}/{self.month:02d}/{self.date:02d}?page={page}"
    
    def getStories(self, driver:webdriver):
        self.logger.info(f"Getting stories for {self.year}/{self.month:02d}/{self.date:02d}")
        page = 1
        count = 50
        while count > 0:
            count = self.__getStoriesForPage__(driver, page)
            page += 1
        self.logger.info(f"Got {len(self.stories)} stories")
        
    def __getStoriesForPage__(self, driver:webdriver, page):
        self.logger.info(f"Getting page {page}")
        driver.get(self.url(page))
        self.__acceptCookies__(driver)
        articles = driver.find_elements(By.CSS_SELECTOR, 'article')
        self.logger.info(f"Found {len(articles)} articles")

        for article in articles:
            url = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            category = article.find_element(By.CSS_SELECTOR, 'div.WSJTheme--articleType--34Gt-vdG').text
            title = article.find_element(By.CSS_SELECTOR, 'span.WSJTheme--headlineText--He1ANr9C').text
            timestamp = article.find_element(By.CSS_SELECTOR, 'p').text
            self.stories.append(Story(url, title, category, timestamp))

        return len(articles)
    
    def __acceptCookies__(self, driver:webdriver):
        try:
            iframe = driver.find_element(By.ID, "sp_message_iframe_718122")
            driver.switch_to.frame(iframe)
            cookies_btn = driver.find_element(By.CLASS_NAME, "sp_choice_type_11")
            cookies_btn.click()
            driver.switch_to.default_content()
            self.logger.info(f"Accepted Cookies")

        except NoSuchElementException:
            pass

    
    def toCSV(self):
        self.logger.info(f"Saving stories to csv for {self.year}/{self.month:02d}/{self.date:02d}")
        output_path = data_manager.saveStories(self.stories, self.year, self.month, self.date)
        self.logger.info(f"Saved stories to csv at {output_path}/{self.date:02d}.csv")