# -*- coding: utf-8 -*-
"""
Comply World Consulting — site du cabinet et espace abonné (Compliance Hub).
Lancement :  streamlit run app.py
"""
import streamlit as st

from core.config import BRAND, PRODUCT, VERSION
from core import ui, auth

st.set_page_config(page_title=f"{BRAND} — Conformité LCB-FT", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

from views import public, connexion, espace, admin  # noqa: E402

try:
    auth.bootstrap_admin_from_secrets(st.secrets)
except Exception:
    auth.bootstrap_admin_from_secrets(None)

st.session_state.setdefault("page", "accueil")
st.session_state.setdefault("user", None)

ui.inject_css()
user = st.session_state.user
ui.topnav(user)

page = st.session_state.page
PUBLIC = {"accueil": public.accueil, "cabinet": public.cabinet, "expertises": public.expertises,
          "juridictions": public.juridictions, "actualites": public.actualites_page, "contact": public.contact}

if page in PUBLIC:
    PUBLIC[page]()
elif page == "connexion":
    if user:
        st.session_state.page = "admin" if user.get("role") == "admin" else "espace"
        st.rerun()
    connexion.page()
elif page == "espace":
    if not user:
        st.session_state.page = "connexion"; st.rerun()
    espace.page(user)
elif page == "admin":
    if not user:
        st.session_state.page = "connexion"; st.rerun()
    admin.page(user)
else:
    public.accueil()

ui.footer()
