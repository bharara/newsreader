import streamlit as st
import data_manager

import ui
import utils

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s; %(levelname)s; %(message)s",
    handlers=[logging.FileHandler("reader.log"), logging.StreamHandler()],
)

st.set_page_config(
    layout="wide",
    page_title="AllNewsReader",
)
st.title("Reader")


lb = ui.logbox()
utils.initiateState()
ui.datePickerRow(lb)
ui.sideBar()

df = st.session_state.get("df")
if df is None:
    lb.warning("Stories not fetched yet. Press fetch first")
else:
    date_range = st.session_state.get("selected_dates")
    if len(date_range) == 2:
        selected_stories = data_manager.getStoriesForDate(date_range, df)
        lb.info(f"Stories for {date_range[0].strftime('%B %d, %Y')} to {date_range[1].strftime('%B %d, %Y')}")
        ui.table(selected_stories, lb) 
