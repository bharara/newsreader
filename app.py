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

if st.session_state.get("df") is None:
    lb.warning("Stories not fetched yet. Press fetch first")
else:
    ui.table(lb) 
