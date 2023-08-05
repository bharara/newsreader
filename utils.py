from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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
    # options.add_argument("-headless")
    st.session_state.driver = webdriver.Firefox(options=options)

    # Login Handler
    logging.info(f"Creating Signin Handler")
    email, password, _ = data_manager.getUserData()
    st.session_state.handler = SigninHandler(email, password)


def exit():
    if "driver" in st.session_state:
        st.session_state.driver.close()
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()
