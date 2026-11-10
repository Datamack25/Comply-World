# -*- coding: utf-8 -*-
"""Espace administrateur : veille (mise à jour), abonnés, messages, référentiels."""
import io
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from core import ui, auth, veille
from core.config import PLANS, SERVICES_LABELS, JURIDICTIONS
from core.data import REFERENTIELS, load, save, contacts


def page(user):
    if user.get("role") != "admin":
        st.error("Accès réservé à l'administrateur.")
        return
    ui.page_head("Administration", "Pilotage de la plateforme", "Actualités réglementaires, abonnés, messages et référentiels.")
    c1, c2, _ = st.columns([1.3, 1.5, 4])
    c1.button("← Retour à l'accueil", on_click=ui.go, args=("accueil",), key="adm_home")
    c2.button("Ouvrir l'espace abonné", on_click=ui.go, args=("espace",), key="adm_space")
    t1, t2, t3, t4 = st.tabs(["🔄 Actualités réglementaires", "👥 Abonnés", "✉️ Messages", "🗂️ Référentiels"])
    with t1:
        _veille()
    with t2:
        _abonnes()
    with t3:
        _messages()
    with t4:
        _referentiels()


def _veille():
    st.markdown("#### Mise à jour des actualités réglementaires")
    st.caption(f"Dernière mise à jour : {veille.derniere_maj()}. La collecte interroge les flux d'actualités et vérifie si les pages officielles "
               "suivies (GAFI, AMLA, OFAC, FinCEN, CANAFE, BRH, UCREF) ont changé.")
    if st.button("🔄 Mettre à jour les actualités réglementaires", type="primary", key="veille_go"):
        with st.spinner("Collecte en cours…"):
            res = veille.mettre_a_jour()
        st.success(f"{res['nouveautes']} nouvelle(s) actualité(s) ajoutée(s).")
        st.dataframe(res["rapport"], hide_index=True, width="stretch")
        if res["entree"]["erreurs"]:
            st.warning("Certaines sources n'ont pas répondu (réseau ou site indisponible). Elles seront réinterrogées à la prochaine mise à jour.")
    with st.expander("➕ Ajouter une actualité manuellement"):
        with st.form("add_news", clear_on_submit=True):
            a, b, c = st.columns(3)
            d = a.date_input("Date", value=date.today(), format="DD/MM/YYYY")
            j = b.selectbox("Juridiction", ["International", "UE"] + JURIDICTIONS)
            th = c.selectbox("Thème", ["Réglementation", "Sanctions", "Pays à risque", "Évaluation des risques", "Supervision", "Typologies"])
            titre = st.text_input("Titre")
            resume = st.text_area("Résumé / analyse")
            a, b = st.columns(2)
            src = a.text_input("Source")
            lien = b.text_input("Lien")
            if st.form_submit_button("Publier", type="primary") and titre:
                veille.ajouter_manuellement(d, j, th, titre, resume, src, lien)
                st.success("Actualité publiée.")
    with st.expander("⚙️ Sources suivies"):
        src = load("veille/veille_sources.csv")
        ed = st.data_editor(src, num_rows="dynamic", width="stretch", key="src_ed",
                            column_config={"type": st.column_config.SelectboxColumn(options=["rss", "page"]),
                                           "actif": st.column_config.CheckboxColumn()})
        if st.button("Enregistrer les sources", key="src_save"):
            ed["actif"] = ed["actif"].astype(int)
            save("veille/veille_sources.csv", ed)
            st.success("Sources enregistrées.")
    with st.expander("🧹 Gérer les actualités publiées"):
        a = load("veille/veille_actualites.csv")
        ed = st.data_editor(a, num_rows="dynamic", width="stretch", key="act_ed")
        if st.button("Enregistrer les actualités", key="act_save"):
            save("veille/veille_actualites.csv", ed)
            st.success("Actualités enregistrées.")


def _abonnes():
    users = auth.list_users()
    if users:
        rows = [dict(identifiant=k, nom=v.get("name"), organisation=v.get("org"), role=v.get("role"), offre=v.get("plan"),
                     statut=v.get("status"), expiration=v.get("expiry"), derniere_connexion=v.get("last_login"), cree_le=v.get("created"))
                for k, v in users.items()]
        df = pd.DataFrame(rows)
        attente = int((df.statut == "en attente").sum())
        if attente:
            st.warning(f"{attente} demande(s) d'abonnement en attente d'activation.")
        st.dataframe(df, hide_index=True, width="stretch")
    st.markdown("#### Modifier un compte")
    if users:
        login = st.selectbox("Compte", list(users), key="u_sel")
        u = users[login]
        with st.form("edit_user"):
            a, b, c = st.columns(3)
            status = a.selectbox("Statut", ["actif", "en attente", "suspendu"], index=["actif", "en attente", "suspendu"].index(u.get("status", "en attente")))
            plan = b.selectbox("Offre", list(PLANS), index=list(PLANS).index(u.get("plan", "Essentiel")) if u.get("plan") in PLANS else 0)
            exp_default = date.fromisoformat(u["expiry"]) if u.get("expiry") else date.today() + timedelta(days=365)
            expiry = c.date_input("Expiration", value=exp_default, format="DD/MM/YYYY")
            services = st.multiselect("Services ouverts (ajustement fin)", list(SERVICES_LABELS), default=u.get("services", PLANS.get(plan, [])),
                                      format_func=lambda s: SERVICES_LABELS[s])
            pwd = st.text_input("Nouveau mot de passe (laisser vide pour conserver)", type="password")
            a, b = st.columns(2)
            save_btn = a.form_submit_button("Enregistrer", type="primary")
            reset_srv = b.form_submit_button("Appliquer les services de l'offre")
        if save_btn:
            auth.update_user(login, status=status, plan=plan, expiry=expiry.isoformat(), services=services, password=pwd)
            st.success("Compte mis à jour."); st.rerun()
        if reset_srv:
            auth.update_user(login, plan=plan)
            st.success("Services alignés sur l'offre."); st.rerun()
        if u.get("role") != "admin" and st.button(f"Supprimer le compte {login}", key="u_del"):
            auth.delete_user(login); st.rerun()
    st.markdown("#### Créer un abonné")
    with st.form("new_user", clear_on_submit=True):
        a, b, c = st.columns(3)
        login = a.text_input("Identifiant")
        name = b.text_input("Nom")
        org = c.text_input("Organisation")
        pwd = a.text_input("Mot de passe provisoire", type="password")
        plan = b.selectbox("Offre", list(PLANS))
        role = c.selectbox("Rôle", ["client", "admin"])
        if st.form_submit_button("Créer", type="primary"):
            ok, msg = auth.create_user(login, pwd, name, org, role=role, plan=plan, status="actif",
                                       expiry=(date.today() + timedelta(days=365)).isoformat())
            (st.success if ok else st.error)(msg)


def _messages():
    df = contacts()
    if df.empty:
        st.info("Aucun message reçu.")
        return
    st.dataframe(df.sort_values("date", ascending=False), hide_index=True, width="stretch")
    st.download_button("Exporter (CSV)", df.to_csv(index=False).encode("utf-8-sig"), "messages_contact.csv", "text/csv")


def _referentiels():
    st.caption("Chaque référentiel est un fichier CSV : téléchargez-le, modifiez-le (ou éditez-le ici), puis enregistrez. "
               "Les colonnes doivent être conservées.")
    key = st.selectbox("Référentiel", list(REFERENTIELS), key="ref_sel")
    rel = REFERENTIELS[key]
    df = load(rel)
    st.download_button("⬇️ Télécharger le CSV", df.to_csv(index=False).encode("utf-8-sig"), rel.split("/")[-1], "text/csv")
    up = st.file_uploader("Remplacer par un fichier CSV", type="csv", key=f"up_{rel}")
    if up is not None:
        try:
            new = pd.read_csv(io.BytesIO(up.getvalue()), encoding="utf-8-sig", sep=None, engine="python")
            missing = set(df.columns) - set(new.columns)
            if missing:
                st.error(f"Colonnes manquantes : {', '.join(sorted(missing))}")
            elif st.button("Confirmer le remplacement", type="primary", key="up_ok"):
                save(rel, new[df.columns.tolist() + [c for c in new.columns if c not in df.columns]])
                st.success("Référentiel remplacé.")
        except Exception as e:
            st.error(f"Lecture impossible : {e}")
    ed = st.data_editor(df, num_rows="dynamic", width="stretch", height=420, key=f"ed_{rel}")
    if st.button("Enregistrer les modifications", key="ref_save"):
        save(rel, ed)
        st.success("Référentiel enregistré.")
