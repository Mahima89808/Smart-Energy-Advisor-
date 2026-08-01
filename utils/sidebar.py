import uuid

import streamlit as st


def ensure_session_id() -> str:
    """
    Ensures this browser session has a unique session_id,
    generating one on first visit and reusing it afterward.
    Used to scope each user's appliances and saved records
    so different browser sessions never see each other's data.
    """

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    return st.session_state.session_id


def render_sidebar() -> None:
    """
    Renders the shared sidebar block: a header and one bordered
    card per page, each with a bold title and a one-line
    description. Call once near the top of every page script
    (including Landing_Page.py).
    """

    ensure_session_id()

    with st.sidebar:

        st.header("Navigation")

        st.caption("Use the sidebar pages to access:")

        with st.container(border=True):
            st.markdown("**Home**")
            st.caption("Upload bills and manage appliance information.")

        with st.container(border=True):
            st.markdown("**Analysis**")
            st.caption("View electricity consumption analysis.")

        with st.container(border=True):
            st.markdown("**Suggestions**")
            st.caption("Review energy-saving recommendations.")

        with st.container(border=True):
            st.markdown("**History**")
            st.caption("Access previously saved analyses.")

        st.info(
            "Start by opening the Home page and uploading your electricity bill."
        )