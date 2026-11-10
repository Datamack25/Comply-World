# -*- coding: utf-8 -*-
"""Pages publiques du site : accueil, cabinet, expertises, juridictions, actualités, contact."""
import html
import re

import streamlit as st

from core import ui
from core.config import BRAND, CONTACT_EMAIL
from core.data import load, actualites, save_contact
from views.expertises_content import DETAILS
from core.links import url
from views import haiti_contexte

EXPERTISES = [
    ("🧭", "Diagnostic et cartographie des risques",
     "Évaluation de votre exposition au blanchiment et au financement du terrorisme par client, produit, canal et zone géographique, "
     "alignée sur les évaluations nationales des risques et les typologies des cellules de renseignement financier."),
    ("🗺️", "Parcours de mise en conformité",
     "Feuille de route priorisée, étape par étape, avec livrables, responsables et échéances, adaptée à votre statut et à votre juridiction."),
    ("🛡️", "Dispositif de contrôle interne",
     "Plan de contrôle permanent de 1er et 2e niveau, fiches de contrôle, indicateurs de pilotage et préparation des missions d'audit."),
    ("🔎", "KYC / KYB et remédiation",
     "Revue des dossiers clients, identification des bénéficiaires effectifs, procédures d'entrée en relation et plans de remédiation du stock."),
    ("⚖️", "Sanctions et gel des avoirs",
     "Paramétrage et calibrage du filtrage, procédures de gel, traitement des homonymies : ONU, Union européenne, OFAC et registres nationaux."),
    ("📨", "Déclarations de soupçon",
     "Organisation du circuit d'alerte et de déclaration auprès de Tracfin, de l'UCREF, de FinCEN ou de CANAFE, et qualité des déclarations."),
    ("🎓", "Formation et sensibilisation",
     "Programmes adaptés aux dirigeants, aux équipes opérationnelles et aux réseaux d'agents, avec évaluation et attestations."),
    ("📡", "Veille réglementaire",
     "Suivi des évolutions du GAFI, de l'AMLA, de l'ACPR, de la BRH et de l'UCREF et des régulateurs des Amériques, avec analyse d'impact."),
    ("🏛️", "Agrément et relation superviseur",
     "Préparation des dossiers d'agrément et des contrôles sur place : ACPR, AMF, BRH, organismes d'autorégulation."),
]


def _hero():
    left, right = st.columns([1.75, 1], gap="large")
    with left:
        st.markdown(f"""
<div class="cw-hero">
  <div class="kicker">Cabinet spécialisé en</div>
  <h1>Conformité financière, <em>LCB&#8209;FT</em> et sanctions internationales</h1>
  <p>{html.escape(BRAND)} accompagne les établissements financiers et les professions assujetties dans la construction,
  la mise à niveau et le pilotage de leur dispositif de conformité : évaluation des risques, procédures, contrôle interne et formation.</p>
</div>""", unsafe_allow_html=True)
        c1, c2, _ = st.columns([1, 1.15, 1.2])
        c1.button("Nos expertises", type="primary", on_click=ui.go, args=("expertises",), width="stretch", key="hero_exp")
        c2.button("Nous contacter", on_click=ui.go, args=("contact",), width="stretch", key="hero_ct")
    with right:
        _news_box(4)
        st.button("Toutes les actualités réglementaires →", type="tertiary", on_click=ui.go, args=("actualites",), key="hero_news")


def _news_box(n=4):
    items = []
    for _, r in actualites(n).iterrows():
        d = r["date"].strftime("%d/%m/%Y") if hasattr(r["date"], "strftime") else str(r["date"])
        lien = str(r.get("lien", "") or "")
        t = html.escape(str(r["titre"]))
        t = f'<a href="{html.escape(lien)}" target="_blank">{t}</a>' if lien.startswith("http") else t
        items.append(f'<div class="it"><div class="d">{html.escape(d)} · {html.escape(str(r["juridiction"]))}</div><div class="t">{t}</div></div>')
    st.markdown(f'<div class="cw-newsbox"><h4>Actualités réglementaires</h4>{"".join(items)}</div>', unsafe_allow_html=True)


ORGANISMES = {
    "_": ["GAFI — Recommandations", "GAFI — listes noire et grise", "GAFIC", "AMLA", "Tracfin", "UCREF", "BRH — circulaires", "ACPR"],
    "Diagnostic et cartographie des risques": ["ENR Haïti (décembre 2025)", "GAFI — Recommandations", "CMF — L561-1 et s.", "AMLR (UE) 2024/1624", "AMLA", "BRH — circulaire 129-1"],
    "Parcours de mise en conformité": ["CMF — L561-1 et s.", "Arrêté du 6 janvier 2021", "AMLR (UE) 2024/1624", "BRH — circulaire 129-1", "BRH — circulaires", "UCREF"],
    "Dispositif de contrôle interne": ["Arrêté du 3 novembre 2014", "Arrêté du 6 janvier 2021", "AMLR (UE) 2024/1624", "BRH — circulaires", "BRH — normes prudentielles", "ACPR"],
    "KYC / KYB et remédiation": ["CMF — R561-1 (bénéficiaire effectif)", "Registre des bénéficiaires effectifs (INPI)", "AMLR (UE) 2024/1624", "BRH — circulaire 129-1", "GAFI — Recommandations"],
    "Sanctions et gel des avoirs": ["ONU — liste consolidée", "ONU — régime de sanctions Haïti (2653)", "EU Sanctions Map", "Registre national des gels",
                                    "ACPR — lignes directrices gel des avoirs", "OFAC — recherche SDN", "BRH — circulaires"],
    "Déclarations de soupçon": ["Tracfin — quand et comment déclarer", "Tracfin — ERMES", "CMF — L561-15 (déclaration de soupçon)", "UCREF", "FinCEN", "CANAFE / FINTRAC", "Groupe Egmont"],
    "Formation et sensibilisation": ["GAFI — Recommandations", "Arrêté du 6 janvier 2021", "UCREF", "ACPR"],
    "Veille réglementaire": ["GAFI", "GAFIC", "AMLA", "EUR-Lex", "Légifrance", "ACPR", "AMF", "Tracfin", "BRH — circulaires", "UCREF — événements"],
    "Agrément et relation superviseur": ["ACPR", "AMF", "BRH", "BRH — normes prudentielles"],
}


def _open_expertise(titre: str):
    st.session_state.expertise_once = titre  # consommé à l'affichage : la navigation normale revient à la liste
    ui.go("expertises")


def _expertises_grid(n=None, key="g"):
    # Bouton « En savoir plus » stylé comme un lien cuivre, collé sous chaque carte
    st.markdown("""<style>
    [class*="st-key-more_"] button {{ color:#B8743A !important; font-size:.76rem; letter-spacing:1px; text-transform:uppercase; font-weight:600;
        padding:0; margin-top:-6px; cursor:pointer; }}
    [class*="st-key-more_"] button:hover p {{ text-decoration:underline; text-underline-offset:5px; }}
    [class*="st-key-more_"] button p {{ color:#B8743A !important; }}
    </style>""".replace("{{", "{").replace("}}", "}"), unsafe_allow_html=True)
    items = EXPERTISES if n is None else EXPERTISES[:n]
    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for j, (col, (ico, t, d)) in enumerate(zip(cols, items[i:i + 3])):
            with col:
                ui.card(ico, t, d)
                st.button("+ En savoir plus", key=f"more_{key}_{i + j}", type="tertiary", on_click=_open_expertise, args=(t,))
        st.write("")


def _news_list(n=4):
    df = actualites(n)
    for _, r in df.iterrows():
        d = r["date"].strftime("%d/%m/%Y") if hasattr(r["date"], "strftime") else str(r["date"])
        lien = str(r.get("lien", "") or "")
        link = f' · <a href="{html.escape(lien)}" target="_blank">Source</a>' if lien.startswith("http") else ""
        st.markdown(f"""<div class="cw-news"><div class="meta">{html.escape(d)} · {html.escape(str(r['juridiction']))} · {html.escape(str(r['theme']))}</div>
        <div class="t">{html.escape(str(r['titre']))}</div><div class="r">{html.escape(str(r['resume']))[:330]}{link}</div></div>""", unsafe_allow_html=True)


# ============================================================================ ACCUEIL
def accueil():
    _hero()
    ui.section("Nos expertises", "Un accompagnement sur mesure",
               "Chaque établissement a son modèle d'affaires et son superviseur. Nous construisons avec vous un dispositif "
               "proportionné à vos risques, documenté et prêt pour le contrôle.")
    _expertises_grid(6, key="acc")
    st.button("Voir toutes nos expertises →", type="tertiary", on_click=ui.go, args=("expertises",), key="acc_more_exp")

    ui.section("Notre méthode", "Du diagnostic au contrôle", "")
    cols = st.columns(4)
    steps = [("01", "Diagnostic", "Entretiens, revue documentaire et tests sur dossiers pour mesurer l'écart avec les exigences."),
             ("02", "Plan d'action", "Parcours de mise en conformité priorisé, daté et validé par la direction."),
             ("03", "Déploiement", "Procédures, outils, formation des équipes et accompagnement de la remédiation."),
             ("04", "Contrôle et suivi", "Plan de contrôle permanent, indicateurs et préparation des inspections.")]
    for col, (n, t, d) in zip(cols, steps):
        col.markdown(f'<div class="cw-step"><div class="num">{n}</div><h5>{t}</h5><p>{d}</p></div>', unsafe_allow_html=True)

    st.markdown("""<div class="cw-band"><h3>Un dispositif à mettre en conformité ?</h3>
    <p>Parlons de votre activité et de votre calendrier réglementaire.</p></div>""", unsafe_allow_html=True)
    b1, _ = st.columns([1.2, 5])
    b1.button("Nous contacter", type="primary", on_click=ui.go, args=("contact",), width="stretch", key="acc_contact")


# ============================================================================ LE CABINET
def cabinet():
    ui.page_head("Le cabinet", "Présentation", "Un cabinet de conseil indépendant dédié à la conformité financière.")
    ui.home_button("cab")
    ui.section("Qui sommes-nous", "Ne faire que la conformité, et la faire bien",
               f"{BRAND} est un cabinet de conseil spécialisé en lutte contre le blanchiment de capitaux et le financement du terrorisme (LCB-FT), "
               "en sanctions internationales et en contrôle interne. Nos consultants ont exercé au sein d'établissements bancaires et de fintechs de paiement, "
               "sur des fonctions d'analyse LCB-FT, de KYC et de conformité.")
    st.markdown("""Nous intervenons en priorité sur les **corridors Europe – Caraïbes – Amériques**, là où les flux de la diaspora,
les transferts d'argent et les relations de correspondance bancaire exigent une maîtrise simultanée de plusieurs régimes juridiques.""")
    ui.section("Nos valeurs", "Ce qui guide nos missions")
    cols = st.columns(4)
    vals = [("🎯", "Approche par les risques", "Des mesures proportionnées à votre exposition réelle, pas des procédures génériques."),
            ("📐", "Rigueur", "Chaque recommandation est rattachée à un texte, une référence et une preuve attendue."),
            ("🤝", "Proximité", "Des livrables directement utilisables par vos équipes opérationnelles."),
            ("🧭", "Indépendance", "Un regard extérieur, sans conflit d'intérêts avec les éditeurs de solutions.")]
    for col, (i, t, d) in zip(cols, vals):
        with col:
            ui.card(i, t, d)
    ui.section("Nos clients", "Pour qui travaillons-nous ?")
    c1, c2 = st.columns(2)
    c1.markdown("""- Banques et établissements de crédit
- Établissements de paiement et de monnaie électronique
- Maisons de transfert et intermédiaires de change
- Coopératives d'épargne et de crédit, institutions de microfinance""")
    c2.markdown("""- Prestataires de services sur crypto-actifs
- Compagnies et intermédiaires d'assurance
- Professions non financières : notaires, avocats, comptables, agents immobiliers, opérateurs de jeux
- Organismes à but non lucratif""")


# ============================================================================ EXPERTISES
def expertises():
    ui.page_head("Nos expertises", "Un accompagnement sur mesure", "Du diagnostic initial au pilotage permanent de votre dispositif.")
    sel = st.session_state.pop("expertise_once", None)
    if sel in DETAILS:
        _detail_expertise(sel)
        return
    ui.home_button("exp")
    st.write("")
    _expertises_grid(key="exp")
    ui.section("Livrables", "Ce que vous obtenez")
    c1, c2 = st.columns(2)
    c1.markdown("""- Cartographie des risques BC-FT (Excel)
- Parcours de mise en conformité daté, par phase
- Manuel de procédures LCB-FT et gel des avoirs
- Grille de scoring client""")
    c2.markdown("""- Plan de contrôle permanent et fiches de contrôle
- Supports de formation et attestations
- Notes d'actualité réglementaire et analyses d'impact
- Rapport annuel LCB-FT pour la direction""")


def _detail_expertise(titre: str):
    import pandas as pd
    ico, _, desc = next(e for e in EXPERTISES if e[1] == titre)
    d = DETAILS[titre]
    b1, b2, _ = st.columns([1.3, 1.5, 4])
    b1.button("← Retour à l'accueil", key="det_home", on_click=ui.go, args=("accueil",))
    b2.button("← Toutes nos expertises", key="det_back", on_click=ui.go, args=("expertises",))
    ui.section("Expertise", f"{ico} {titre}", desc)

    st.markdown("#### Notre méthode")
    cols = st.columns(len(d["approche"]))
    for col, (t, txt) in zip(cols, d["approche"]):
        col.markdown(f'<div class="cw-card"><h4>{html.escape(t)}</h4><p>{html.escape(txt)}</p></div>', unsafe_allow_html=True)

    st.markdown("#### Cadre de référence")
    cols = st.columns(len(d["cadre"]), gap="large")
    for col, (j, items) in zip(cols, d["cadre"].items()):
        with col:
            st.markdown(f"**{j}**")
            ui.ref_list(items)

    if d["exemples"]:
        st.markdown("#### Exemples")
        tabs = st.tabs([e[0] for e in d["exemples"]])
        for tab, (_, intro, cols_, rows) in zip(tabs, d["exemples"]):
            with tab:
                st.caption(intro)
                ui.html_table(cols_, rows)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("#### Ce que nous faisons")
        st.markdown("\n".join(f"- {a}" for a in d["actions"]))
    with c2:
        st.markdown("#### Livrables")
        st.markdown("\n".join(f"- {l}" for l in d["livrables"]))
    org = ORGANISMES.get(titre, ORGANISMES["_"])
    st.markdown("#### Organismes et textes de référence")
    st.markdown(ui.links_html([(n, url(n)) for n in org]), unsafe_allow_html=True)
    st.caption("Les exemples présentés sont illustratifs : chaque mission est adaptée à l'activité, à la taille et au superviseur de l'établissement.")
    st.markdown(f"""<div class="cw-band"><h3>Parlons de votre besoin</h3>
    <p>{html.escape(titre)} : nous construisons une intervention adaptée à votre activité et à votre superviseur.</p></div>""", unsafe_allow_html=True)
    st.button("Nous contacter", type="primary", key="det_contact", on_click=ui.go, args=("contact",))


# ============================================================================ JURIDICTIONS
def juridictions():
    ui.page_head("Juridictions", "Cadres réglementaires couverts", "Les textes de référence et les dernières évolutions, avec les liens officiels.")
    ui.home_button("jur")
    t1, t2, t3, t4 = st.tabs(["Europe", "Haïti", "Amériques", "Pays à risque (GAFI / UE)"])
    with t1:
        ui.df_table(load("europe/europe_cadre_reglementaire.csv"),
                    {"perimetre": "Périmètre", "texte": "Texte", "statut": "Statut", "points_cles": "Points clés", "lien": "Lien"})
        st.markdown(ui.links_html([(n, url(n)) for n in ["AMLA", "EUR-Lex", "Légifrance", "ACPR", "AMF", "Tracfin", "Registre national des gels"]]),
                    unsafe_allow_html=True)
    with t2:
        haiti_contexte.render()
        st.markdown("#### Textes de référence")
        st.markdown("**Texte cadre : décret du 30 avril 2023** (Le Moniteur, Spécial n°12 du 4 mai 2023). "
                    "**Évaluation nationale des risques** publiée en décembre 2025 : risque global de blanchiment **élevé**. "
                    "Haïti figure sur la liste grise du GAFI et sur la liste UE des pays tiers à haut risque.")
        ui.df_table(load("haiti/haiti_cadre_juridique.csv"), {"texte": "Texte", "date": "Date", "publication": "Publication", "statut": "Statut", "lien": "Lien"})
        st.markdown(ui.links_html([(n, url(n)) for n in ["BRH", "BRH — circulaires", "UCREF", "ENR Haïti (décembre 2025)", "GAFIC",
                                                          "ONU — régime de sanctions Haïti (2653)"]]), unsafe_allow_html=True)
        st.caption("Le détail des obligations, seuils et vulnérabilités sectorielles est disponible dans l'espace abonné.")
    with t3:
        ui.df_table(load("ameriques/ameriques_juridictions.csv"),
                    {"pays": "Pays", "crf": "CRF", "superviseurs": "Superviseurs", "texte_principal": "Texte principal",
                     "statut_gafi_oct2026": "GAFI (oct. 2026)", "liste_ue_2026": "Liste UE", "lien": "Lien"})
        st.markdown(ui.links_html([(n, url(n)) for n in ["FinCEN", "OFAC", "CANAFE / FINTRAC", "UIF Mexique", "UAF République dominicaine", "GAFILAT"]]),
                    unsafe_allow_html=True)
    with t4:
        st.caption("Statuts au 30 octobre 2026 (GAFI) et au 29 janvier 2026 (liste UE).")
        ui.df_table(load("referentiels/pays_a_risque.csv"), {"pays": "Pays", "statut_gafi": "Statut GAFI", "liste_ue_haut_risque": "Liste UE"})
        st.markdown(ui.links_html([(n, url(n)) for n in ["GAFI — listes noire et grise", "Liste UE des pays tiers à haut risque"]]), unsafe_allow_html=True)


# ============================================================================ ACTUALITÉS
def actualites_page():
    ui.page_head("Actualités", "Actualités réglementaires", "Les dernières évolutions réglementaires en matière de conformité financière.")
    ui.home_button("act")
    _news_list(8)
    st.caption("Les abonnés accèdent à l'ensemble des actualités réglementaires, filtrables par juridiction et par thème.")


# ============================================================================ CONTACT
def contact():
    ui.page_head("Contact", "Nous contacter", "Une question, une mission, une demande d'accès ? Nous revenons vers vous rapidement.")
    ui.home_button("ct")
    c1, c2 = st.columns([1.6, 1])
    with c1:
        with st.form("contact_form", clear_on_submit=True):
            a, b = st.columns(2)
            nom = a.text_input("Nom et prénom *")
            email = b.text_input("Adresse e-mail *")
            org = a.text_input("Organisation")
            objet = b.selectbox("Objet", ["Demande de mission", "Demande d'abonnement", "Formation", "Actualités réglementaires", "Autre"])
            msg = st.text_area("Message *", height=150)
            ok = st.checkbox("J'accepte que mes données soient utilisées pour traiter ma demande.")
            sent = st.form_submit_button("Envoyer", type="primary")
        if sent:
            if not (nom and email and msg and ok):
                st.error("Merci de renseigner les champs obligatoires et d'accepter le traitement de vos données.")
            elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                st.error("Adresse e-mail invalide.")
            else:
                save_contact(nom, email, org, objet, msg)
                st.success("Merci, votre message a bien été transmis.")
    with c2:
        st.markdown("#### Coordonnées")
        st.markdown(("✉️ " + CONTACT_EMAIL + "  \n") if CONTACT_EMAIL else "")
        st.markdown("📍 Paris · Port-au-Prince  \n🌐 Interventions en Europe, en Haïti et dans les Amériques")
        st.markdown("#### Espace abonné")
        st.write("Les abonnés accèdent aux parcours de mise en conformité, aux dispositifs de contrôle, aux référentiels et aux actualités réglementaires.")
        st.button("👤 Se connecter", on_click=ui.go, args=("connexion",), key="ct_login", type="primary")
