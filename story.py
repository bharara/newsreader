import json
from selenium import webdriver
from signin import SigninHandler
from selenium.webdriver.common.by import By
from time import sleep
from exceptions import LoginFailed
from summary_openai import summarize_article
import logging
import re

class Story:
    def __init__(self, url, title="", category="", published="", content="", summary=""):
        self.url = url
        self.title = title
        self.category = category
        self.published = published
        self.content =  content
        self.summary = summary

        self.logger = logging.getLogger(__name__)

    def getSummary(self):
        if self.summary == "":
            self.summary = summarize_article(self.content)
            self.summary = self.content[:100]
        return self.summary

    def getStoryContent(self, driver: webdriver, signInHandler: SigninHandler):
        self.logger.info(f"Getting story {self.title[:20]}")
        driver.get(self.url)

        try:
            if not signInHandler.isLoggedIn(driver):
                sleep(15)
                signInHandler.login(driver)
                driver.get(self.url)

            paras = driver.find_elements(By.TAG_NAME, "p")
            self.logger.info(f"Got {len(paras)} paras")
            self.content = self.__sanitize_text__("\t\t".join([para.text for para in paras]))

        except LoginFailed as e:
            self.logger.error(
                f"LoginFailed exception occurred while getting the story: {e}"
            )
            raise Exception("Failed getting story.")

    def toDict(self):
        return {
            "url": self.url,
            "title": self.title,
            "category": self.category,
            "published": self.published,
            "content": self.content,
            "summary": self.summary,
        }

    def __sanitize_text__(self, text):
        clean_text = re.sub(r'<.*?>', '', text)
        clean_text = clean_text.replace(',', ';')
        clean_text = clean_text.replace('\n', '\t\t')
        clean_text = re.sub(r'[\'"“”‘’]', '', clean_text)
        clean_text = clean_text.strip()
        return clean_text

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.toDict())
