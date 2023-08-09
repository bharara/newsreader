from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import logging
from datetime import date, timedelta
import pandas as pd

class Archiver:
    stories = []

    def __init__(self, dates: (date, date), driver: webdriver):
        self.start_date, self.end_date = dates
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def url(self, date:date, page=1):
        return f"https://www.wsj.com/news/archive/{date.year}/{date.month:02d}/{date.day:02d}?page={page}"
    
    def getStories(self):
        current_date = self.start_date
        while current_date <= self.end_date:
            self.__getStoriesForDate__(current_date)
            current_date += timedelta(days=1)

    def __getStoriesForDate__(self, date:date):
        self.logger.info(f"Getting stories for {date.year}/{date.month:02d}/{date.day:02d}")
        page = 1
        count = 51
        while count >= 50:
            count = self.__getStoriesForPage__(page, date)
            page += 1
        self.logger.info(f"Got {len(self.stories)} stories in total")

    def __getStoriesForPage__(self, page:int, date:date):
        self.logger.info(f"Getting page {page}")
        self.driver.get(self.url(date, page))
        self.__acceptCookies__()
        articles = self.driver.find_elements(By.CSS_SELECTOR, "article")
        self.logger.info(f"Found {len(articles)} articles for page {page}")

        for article in articles:
            url = article.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            category = article.find_element(
                By.CSS_SELECTOR, "div.WSJTheme--articleType--34Gt-vdG"
            ).text
            title = article.find_element(
                By.CSS_SELECTOR, "span.WSJTheme--headlineText--He1ANr9C"
            ).text
            timestamp = article.find_element(By.CSS_SELECTOR, "p").text
            self.stories.append({
                'url': url,
                'title': title,
                'category': category,
                'published': timestamp,
                'score': 0,
                'date': date
            })

        return len(articles)

    def __acceptCookies__(self):
        try:
            iframe = self.driver.find_element(By.ID, "sp_message_iframe_718122")
            self.driver.switch_to.frame(iframe)
            cookies_btn = self.driver.find_element(By.CLASS_NAME, "sp_choice_type_11")
            cookies_btn.click()
            self.driver.switch_to.default_content()
            self.logger.info(f"Accepted Cookies")

        except NoSuchElementException:
            pass

    def mergeWithDf(self, df:pd.DataFrame):
        df = pd.concat([df, pd.DataFrame(self.stories)], ignore_index=True)
        df = df.drop_duplicates(subset='url', keep='first')
        return df