from datetime import date

import streamlit as st

import data_manager
import utils
from story import Story


def logbox():
    return st.info("Logs")


def sideBar(lb):
    if st.sidebar.button("Exit App"):
        utils.exit()

    st.sidebar.markdown("---")

    st.sidebar.title("User Profile")
    st.sidebar.write("Enter your details below:")

    email, password, keywords = data_manager.getUserData()
    new_email = st.sidebar.text_input("Email", email)
    new_password = st.sidebar.text_input("Password", password, type="password")
    new_keywords = st.sidebar.text_area("Keywords (comma-separated)", keywords)

    if st.sidebar.button("Save"):
        data_manager.saveUserData(new_email, new_password, new_keywords)
        st.sidebar.success("Data saved successfully!")


def datePickerRow(lb):
    col1, col2 = st.columns([4, 1])
    selected_date = col1.date_input(
        "Select a date",
        max_value=date.today(),
        on_change=utils.dateChanged,
        key="selected_date",
    )
    col2.button("Fetch", on_click=utils.clickFetch, args=([lb]))
    return selected_date


def table(df, lb):
    colms = st.columns((1, 5, 2, 3, 10))
    fields = ["№", "Headline", "Category", "Action", "Summary"]
    for col, field_name in zip(colms, fields):
        col.write(field_name)

    for x, title in enumerate(df["title"]):
        c1, c2, c3, c4, c5 = st.columns((1, 5, 2, 3, 10))
        c1.write(x)
        c2.write(title)
        c3.write(df["category"][x])
        button_phold = c4.empty()
        do_action = button_phold.button("Summarize", key=x)
        c5.write("...")
        if do_action:
            lb.info(f"Fetching article {df['title'][x]}")
            story = Story(
                df["url"][x], df["title"][x], df["category"][x], df["published"][x]
            )
            try:
                story.getStoryContent(st.session_state.driver, st.session_state.handler)
                lb.info(f"Summarizing article with length {len(story.content)}")
                story.getSummary()
                c5.empty()
                c5.write(story.summary)
            except:
                lb.error(f"Error getting article  {story.title}")
