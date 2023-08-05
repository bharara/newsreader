import streamlit as st
import data_manager

import ui
import utils

import logging
logging.basicConfig(level = logging.INFO, format = "%(asctime)s; %(levelname)s; %(message)s",
                    handlers = [logging.FileHandler('reader.log'), logging.StreamHandler()])

st.set_page_config(
    layout="wide",
    page_title="AllNewsReader",
)
st.title("Reader")


lb = ui.logbox()
utils.initiateState()
selected_date = ui.datePickerRow(lb)
ui.sideBar()

df = data_manager.getStories(selected_date)
if df is None:
    lb.warning("Stories not fetched yet. Press fetch first")
else:
    lb.info(f"Stories for {selected_date}")
    ui.table(df, lb)