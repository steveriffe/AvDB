"""
Google OAuth 2.0 Authentication & Session Management Module
Handles Google Sign-In, token exchange, email allowlist verification, and sidebar user status.
"""
import urllib.parse
import requests
import streamlit as st
from app.config import settings

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_redirect_uri() -> str:
    """
    Returns the appropriate redirect URI for Google OAuth callback.
    Can be overridden via REDIRECT_URI_OVERRIDE env var or auto-detected.
    """
    if settings.redirect_uri_override:
        return settings.redirect_uri_override.rstrip("/") + "/"

    # Default fallback for production / local
    # In Streamlit Cloud / Cloud Run, default is http://localhost:8501 or https://avdb.riffe.co.uk/
    return "https://avdb.riffe.co.uk/"


def get_google_auth_url(redirect_uri: str) -> str:
    """
    Generates the Google OAuth 2.0 Login URL.
    """
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"


def exchange_code_for_user(code: str, redirect_uri: str) -> dict | None:
    """
    Exchanges authorization code for access token and retrieves Google user profile.
    """
    payload = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    try:
        token_resp = requests.post(GOOGLE_TOKEN_ENDPOINT, data=payload, timeout=10)
        token_resp.raise_for_status()
        tokens = token_resp.json()
        access_token = tokens.get("access_token")

        if not access_token:
            return None

        # Fetch profile
        headers = {"Authorization": f"Bearer {access_token}"}
        user_resp = requests.get(GOOGLE_USERINFO_ENDPOINT, headers=headers, timeout=10)
        user_resp.raise_for_status()
        return user_resp.json()
    except Exception as e:
        st.error(f"Authentication error during Google login: {e}")
        return None


def init_auth() -> dict | None:
    """
    Initializes session auth state and processes OAuth callback code if present.
    Returns current user info dictionary if logged in, else None.
    """
    if "user" not in st.session_state:
        st.session_state["user"] = None

    # Check query params for OAuth code
    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]
        # Clear code from URL immediately
        st.query_params.clear()
        
        redirect_uri = get_redirect_uri()
        user_info = exchange_code_for_user(code, redirect_uri)
        if user_info:
            st.session_state["user"] = user_info
            st.rerun()

    return st.session_state.get("user")


def is_authenticated() -> bool:
    """Returns True if the current user is logged in with a verified Google account."""
    user = st.session_state.get("user")
    if not user or not isinstance(user, dict):
        return False
    email = user.get("email", "").strip().lower()
    if not email:
        return False
    # If allowed_emails is * or empty, open access to all valid Google authenticated accounts
    if not settings.allowed_emails or "*" in settings.allowed_emails or "all" in settings.allowed_emails:
        return True
    return email in settings.allowed_emails


def logout():
    """Clears user session state and triggers rerun."""
    st.session_state["user"] = None
    st.query_params.clear()
    st.rerun()


def render_user_sidebar():
    """Renders signed-in user status pill and Logout button in Streamlit sidebar."""
    user = st.session_state.get("user")
    if user and isinstance(user, dict):
        email = user.get("email", "")
        name = user.get("name", email.split("@")[0])
        picture = user.get("picture", "")

        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 Account")
            col1, col2 = st.columns([1, 3])
            with col1:
                if picture:
                    st.image(picture, width=40)
                else:
                    st.markdown("👤")
            with col2:
                st.markdown(f"**{name}**")
                st.caption(email)

            if st.button("Sign Out", type="secondary", use_container_width=True):
                logout()


def require_auth() -> bool:
    """
    Guards subpages in Streamlit. If OAuth is configured and user is not authorized,
    stops execution and renders landing/unauthorized page.
    Returns True if execution can proceed.
    """
    if settings.local_dev_bypass_auth:
        if "user" not in st.session_state or not st.session_state["user"]:
            st.session_state["user"] = {
                "email": settings.allowed_emails[0] if settings.allowed_emails else "steve@riffe.co.uk",
                "name": "Steve (Local Dev)",
                "picture": ""
            }
        render_user_sidebar()
        return True

    if not settings.google_client_id:
        return True

    from app.components.landing import render_landing_page, render_unauthorized_page

    user_info = init_auth()
    if not user_info:
        st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)
        render_landing_page()
        st.stop()
        return False
    elif not is_authenticated():
        st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)
        render_unauthorized_page(user_info)
        st.stop()
        return False

    render_user_sidebar()
    return True

