from datetime import date

import streamlit as st

import data_manager
import utils
from story import Story


def logbox():
    return st.info("Logs")


def sideBar():
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
    colms = st.columns((1, 5, 2, 2, 3, 1, 10))
    fields = [
        "№",
        "Headline",
        "Published",
        "Category",
        "Action",
        "Relevance Score",
        "Summary",
    ]
    # print(df)
    for col, field_name in zip(colms, fields):
        col.write(field_name)

    for x, title in enumerate(df["title"]):
        c1, c2, publ, c3, c4, rel, c5 = st.columns((1, 5, 2, 2, 3, 1, 10))
        c1.write(x)
        c2.write(title)
        publ.write(df["published"][x])
        c3.write(df["category"][x])
        button_phold = c4.empty()
        do_action = button_phold.button("Summarize", key=x)
        rel.write(df["relvence_score"][x])
        c5.write(df["content"][x].__str__()[0:500])
        if do_action:
            lb.info(f"Fetching article {df['title'][x]}")
            story = Story(
                df["url"][x],
                df["title"][x],
                df["category"][x],
                df["published"][x],
                content=df["content"][x],
                summary=df["summary"][x],
            )
            lb.info(f"Summarizing article with length {len(story.content)}")
            summary = story.getSummary()
            c5.write(summary)
