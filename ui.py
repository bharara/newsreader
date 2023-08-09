from datetime import date
import pandas as pd

import streamlit as st

import data_manager
import utils
import summary


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
    col1.date_input(
        "Select a date",
        (date.today(), date.today()),
        max_value=date.today(),
        on_change=utils.dateChanged,
        key="selected_dates",
    )
    col2.button("Fetch", on_click=utils.clickFetch, args=([lb]))


def table(lb):
    date_range = st.session_state.get("selected_dates")
    if len(date_range) != 2:
        return
    lb.info(f"Stories for {date_range[0].strftime('%B %d, %Y')} to {date_range[1].strftime('%B %d, %Y')}")

    colms = st.columns((1, 5, 2, 2, 3, 1, 10))
    fields = [
        "№",
        "Headline",
        "Published",
        "Category",
        "Action",
        "Score",
        "Summary",
    ]

    for col, field_name in zip(colms, fields):
        col.write(field_name)

    for x, row in st.session_state.df.iterrows():
        if date_range[0] > row["date"]  or row["date"] > date_range[1]:
            continue
        c1, c2, publ, c3, c4, rel, c5 = st.columns((1, 5, 2, 2, 3, 1, 10))
        c1.write(x)
        c2.write(row["title"])
        publ.write(row["published"])
        c3.write(row["category"])
        button_phold = c4.empty()
        do_action = button_phold.button("Summarize", key=x)
        rel.write(row["score"])
        c5.write(row["content"].__str__()[0:500])
        if do_action:
            if row["summary"] == "" or pd.isna(row["summary"]):
                lb.info(f"Summarizing article with length {len(row['content'])}")
                st.session_state.df["summary"][x] = summary.get_openai_summary(row["content"])
            c5.empty()
            c5.write(st.session_state.df["summary"][x])
