from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import streamlit as st

import logging
import os
import psutil
import pandas as pd

import data_manager
from scrapper import Scrapper
from signin import SigninHandler


def dateChanged():
    pass


def clickFetch(lb):
    date_range = st.session_state.get("selected_dates")
    lb.info(f"Fetching stories for date {date_range[0].strftime('%B %d, %Y')} to {date_range[1].strftime('%B %d, %Y')}")
    arch = Scrapper(date_range, st.session_state.driver, st.session_state.handler)
    arch.getStories()
    st.session_state.df = arch.mergeWithDf(st.session_state.df)
    
    for index, row in st.session_state.df.iterrows():
        if date_range[0] <= row['date'] <= date_range[1]:
            if row["content"] ==  "" or pd.isna(row['content']):
                st.session_state.df["content"][index] = arch.getStoryContent(row["url"])
                
    recalculateScore()
    data_manager.saveStoriesDf(st.session_state.df)


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
    st.session_state.df = data_manager.getStoriesDf()


def exit():
    if "driver" in st.session_state:
        st.session_state.driver.close()
    data_manager.saveStoriesDf(st.session_state.df)
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()


def calculate_relevance_score_for_keyword(keyword, column):
    if isinstance(column, str):
        return keyword.lower() in column.lower()
    return 0


def calculate_total_relevance_score(row):
    total_score = 0
    keywords = [x.strip(" ") for x in st.session_state.keywords.split(",")] or []
    for keyword in keywords:
        total_score += (
            20 * calculate_relevance_score_for_keyword(keyword, row["category"])
            + 10 * calculate_relevance_score_for_keyword(keyword, row["title"])
            + calculate_relevance_score_for_keyword(keyword, row["content"])
        )
    return total_score

def recalculateScore():
    st.session_state.df["score"] = st.session_state.df.apply(calculate_total_relevance_score, axis=1)
    st.session_state.df = st.session_state.df.sort_values(by="score", ascending=False)
    st.session_state.df = st.session_state.df.reset_index(drop=True)