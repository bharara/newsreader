from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import streamlit as st

import logging
import os
import psutil

import data_manager
from archiver import Archiver
from signin import SigninHandler


def dateChanged():
    pass


def clickFetch(lb):
    lb.info(f"Fetching stories for date {st.session_state.selected_date}")
    print (st.session_state)
    arch = Archiver(st.session_state.selected_date, st.session_state.driver, st.session_state.handler)
    arch.getStories()
    arch.getStoryDetails()
    lb.info(f"Saving stories to CSV")
    arch.toCSV()


@st.cache_resource
def initiateState():
    # WebDriver
    logging.info(f"Creating webdriver with options")
    options = Options()
    options.add_argument("-headless")
    st.session_state.driver = webdriver.Chrome(options=options)

    # Login Handler
    logging.info(f"Creating Signin Handler")
    email, password, keywords = data_manager.getUserData()
    st.session_state.handler = SigninHandler(email, password)
    st.session_state.keywords = keywords


def exit():
    if "driver" in st.session_state:
        st.session_state.driver.close()
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()

def calculate_relevance_score_for_keyword(keyword, column):
    if isinstance(column, str):
        return column.lower().count(keyword.lower())
    return 0

# Function to calculate total relevance score for all keywords in a row
def calculate_total_relevance_score(row):
    total_score = 0
    keywords = st.session_state.keywords or  []
    for keyword in keywords:
        total_score += (
            10 * calculate_relevance_score_for_keyword(keyword, row['title']) +
            20 * calculate_relevance_score_for_keyword(keyword, row['category']) +
            calculate_relevance_score_for_keyword(keyword, row['content'])
        )
    return total_score