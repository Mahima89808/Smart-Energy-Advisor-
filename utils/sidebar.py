"""
Shared Sidebar Navigation
Smart Energy Advisor

Responsibility:
- Render a consistent navigation block in every page's sidebar,
  matching the bordered-card style used on the landing page.

Streamlit's multipage sidebar only persists custom content on the
page where st.sidebar is actually used in that page's own script —
it does not carry over automatically to other pages. This function
is called once near the top of every page so the sidebar looks the
same everywhere, not just on the landing page.

No:
- Business logic
- API calls
- Database logic
"""

import streamlit as st


def render_sidebar() -> None:
    """
    Renders the shared sidebar block: a header and one bordered
    card per page, each with a bold title and a one-line
    description. Call once near the top of every page script
    (including Landing_Page.py).
    """

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