from selenium import webdriver
from signin import SigninHandler
from selenium.webdriver.common.by import By

from exceptions import LoginFailed

import logging
import re
from time import sleep


class Story:
    def __init__(self, url, driver: webdriver, handler: SigninHandler):
        self.url = url
        self.driver = driver
        self.handler = handler
        self.logger = logging.getLogger(__name__)

    def getContent(self) -> str:
        self.logger.info(f"Getting story {self.url}")
        self.driver.get(self.url)

        try:
            if not self.handler.isLoggedIn(self.driver):
                sleep(5)
                self.handler.login(self.driver)
                self.driver.get(self.url)

            paras = self.driver.find_elements(By.TAG_NAME, "p")
            self.logger.info(f"Got {len(paras)} paras")
            return  self.__sanitize_text__(
                "\t\t".join([para.text for para in paras])
            )

        except LoginFailed as e:
            self.logger.error(
                f"LoginFailed exception occurred while getting the story: {e}"
            )
            raise Exception("Failed getting story.")


    def __sanitize_text__(self, text:str) -> str:
        clean_text = re.sub(r"<.*?>", "", text)
        clean_text = clean_text.replace(",", ";")
        clean_text = clean_text.replace("\n", "\t\t")
        clean_text = re.sub(r'[\'"“”‘’]', "", clean_text)
        clean_text = clean_text.strip()
        return clean_text