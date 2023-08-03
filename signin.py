from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from exceptions import LoginFailed

import logging

class SigninHandler:
    
    SIGNIN_PAGE_URL = f'https://www.wsj.com/client/login?target=https%3A%2F%2Fwww.wsj.com%2F'

    def __init__(self, email:str, password:str):
        self.email = email
        self.password = password
        self.logger = logging.getLogger(__name__)

    def isLoggedIn(self, driver:webdriver):
        return len(driver.find_elements(By.ID, 'cx-snippet-promotion')) < 1
    

    def login(self, driver: webdriver):
        self.logger.info(f"Logging in")
        
        try:
            driver.get(SigninHandler.SIGNIN_PAGE_URL)

            emailInput = driver.find_element(By.ID, 'username')
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(emailInput)).click()
            emailInput.send_keys(self.email)

            continuePasswordButton = driver.find_element(By.CLASS_NAME, 'continue-submit')
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(continuePasswordButton)).click()

            passordInput = driver.find_element(By.ID, 'password-login-password')
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(passordInput)).click()
            passordInput.send_keys(self.password)

            passwordButton = driver.find_elements(By.CLASS_NAME, 'basic-login-submit')[-1]
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(passwordButton)).click()
            sleep(5)

            self.logger.info(f"Logged in")

        except TimeoutException as e:
            self.logger.error(f"TimeoutException occurred while logging in: {e}")
            raise LoginFailed("Login attempt timed out.")