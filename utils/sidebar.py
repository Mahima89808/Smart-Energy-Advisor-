import uuid

import streamlit as st
from streamlit_cookies_controller import CookieController

_cookie_controller = None


def _get_cookie_controller() -> CookieController:
    """
    Reuses a single CookieController instance per session instead
    of creating a new one on every rerun.
    """
    global _cookie_controller
    if _cookie_controller is None:
        _cookie_controller = CookieController()
    return _cookie_controller

def ensure_session_id() -> str:
    """
    Ensures this browser has a unique session_id that survives
    both page refreshes and page-to-page navigation, by storing
    it in a browser cookie (st.session_state and st.query_params
    both get cleared in these situations, cookies don't).
    """

    if "session_id" in st.session_state:
        return st.session_state.session_id

    controller = _get_cookie_controller()
    existing_session_id = controller.get("session_id")

    if existing_session_id:
        st.session_state.session_id = existing_session_id
        return existing_session_id

    new_session_id = str(uuid.uuid4())
    st.session_state.session_id = new_session_id
    controller.set("session_id", new_session_id)

    return new_session_id


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