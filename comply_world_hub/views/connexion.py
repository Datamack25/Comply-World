# -*- coding: utf-8 -*-
"""Connexion des abonnés, demande d'abonnement et création du premier administrateur."""
import streamlit as st

from core import ui, auth
from core.config import PLANS, SERVICES_LABELS


def page():
    ui.page_head("Espace client", "Accès abonnés", "Parcours de conformité, dispositifs de contrôle, référentiels et actualités réglementaires réservés aux abonnés.")
    ui.home_button("cx")

    if not auth.has_admin():
        st.warning("Première mise en service : créez le compte administrateur de la plateforme.")
        with st.form("first_admin"):
            a, b = st.columns(2)
            login = a.text_input("Identifiant administrateur")
            name = b.text_input("Nom affiché", value="Administrateur")
            p1 = a.text_input("Mot de passe (8 caractères minimum)", type="password")
            p2 = b.text_input("Confirmation", type="password")
            if st.form_submit_button("Créer l'administrateur", type="primary"):
                if p1 != p2:
                    st.error("Les mots de passe ne correspondent pas.")
                else:
                    ok, msg = auth.create_user(login, p1, name, "", role="admin", plan="Intégral", status="actif")
                    (st.success if ok else st.error)(msg + (" Vous pouvez vous connecter." if ok else ""))
        return

    c1, c2 = st.columns([1, 1.15], gap="large")
    with c1:
        st.markdown("### Se connecter")
        with st.form("login"):
            login = st.text_input("Identifiant")
            pwd = st.text_input("Mot de passe", type="password")
            go = st.form_submit_button("Connexion", type="primary", width="stretch")
        if go:
            user, err = auth.authenticate(login, pwd)
            if user:
                st.session_state.user = user
                st.session_state.page = "admin" if user.get("role") == "admin" else "espace"
                st.rerun()
            else:
                st.error(err)
    with c2:
        st.markdown("### Demander un abonnement")
        st.caption("Votre accès est activé par notre équipe après validation de votre demande.")
        with st.form("signup", clear_on_submit=True):
            a, b = st.columns(2)
            name = a.text_input("Nom et prénom")
            org = b.text_input("Organisation")
            login = a.text_input("Identifiant souhaité (e-mail conseillé)")
            plan = b.selectbox("Offre souhaitée", list(PLANS))
            p1 = a.text_input("Mot de passe", type="password")
            p2 = b.text_input("Confirmation", type="password")
            sent = st.form_submit_button("Envoyer la demande")
        if sent:
            if p1 != p2:
                st.error("Les mots de passe ne correspondent pas.")
            else:
                ok, msg = auth.create_user(login, p1, name, org, plan=plan, status="en attente")
                (st.success if ok else st.error)("Demande enregistrée. Vous serez informé de l'activation de votre accès." if ok else msg)
        with st.expander("Contenu des offres"):
            for p, services in PLANS.items():
                st.markdown(f"**{p}** — " + " · ".join(SERVICES_LABELS[s] for s in services))
