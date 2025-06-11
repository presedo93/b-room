import streamlit as st


def header_buttons():
    c1, c2 = st.columns(2)

    with c1:
        st.button("Exchanges")
        # st.page_link("dashboard/exchanges.py", label="exchanges", icon="💹")

    with c2:
        st.button("Backtester")
        # st.page_link("dashboard/backtester.py", label="b-room", icon="🖥️")
