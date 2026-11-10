# -*- coding: utf-8 -*-
"""Haïti : situation générale et raisons du maintien sur la liste grise du GAFI.
Utilisé par la page publique Juridictions, l'espace abonné et les exports (fiche juridiction)."""
import streamlit as st

from core import ui
from core.data import load
from core.links import url

TITRE = "Situation du pays et liste grise du GAFI"

SYNTHESE = [
    ("Un contexte qui freine la mise en œuvre",
     "Haïti traverse une crise sécuritaire, politique et économique prolongée : violences des gangs qui s'étendent aux zones rurales, "
     "près de 1,5 million de personnes déplacées, élections reportées et transition sans cesse prolongée, septième année de contraction "
     "de l'économie et inflation proche de 28 %. Les administrations, les tribunaux et les superviseurs fonctionnent avec des moyens "
     "réduits, ce qui ralentit l'application des textes adoptés."),
    ("Un cadre juridique rénové, mais encore peu appliqué",
     "Le pays s'est doté d'un nouveau cadre : décret du 30 avril 2023, réorganisation de l'UCREF (novembre 2023), évaluation nationale "
     "des risques (décembre 2025), circulaire BRH 129-1 et lignes directrices sur le gel des fonds (février 2026), pôles judiciaires "
     "spécialisés (mai 2026). Le GAFI juge désormais moins les textes que leur efficacité : supervision réelle, enquêtes, condamnations "
     "et confiscations."),
    ("Pourquoi Haïti reste sur la liste grise",
     "Haïti est sous surveillance renforcée depuis son engagement de juin 2021. Tous les délais de son plan d'action sont expirés. "
     "Six exigences restent ouvertes : supervision des professions non financières à risque (immobilier et jeux n'ont pas d'autorité "
     "désignée), transparence des bénéficiaires effectifs (pas de registre complet), enquêtes et poursuites pour blanchiment, recouvrement "
     "des avoirs criminels, régime de sanctions financières ciblées et surveillance des OBNL. En octobre 2026, Haïti a choisi de différer "
     "son rapport au GAFI."),
    ("Ce que cela implique pour les établissements",
     "Haïti figure aussi sur la liste européenne des pays tiers à haut risque : les banques correspondantes et les partenaires étrangers "
     "appliquent une vigilance renforcée aux flux haïtiens (risque de « de-risking »). Pour les institutions haïtiennes, un dispositif "
     "documenté et démontrable — cartographie, KYC/KYB, filtrage, déclarations à l'UCREF, contrôle interne — est la meilleure protection "
     "pour préserver leurs relations de correspondance et leurs corridors de transfert."),
]

STATUT_TONE = {"Réalisé": "green", "En cours": "amber"}


def render(compact: bool = False):
    """Affiche la synthèse, les indicateurs clés et le plan d'action du GAFI."""
    st.markdown(f"#### {TITRE}")
    for t, txt in SYNTHESE:
        st.markdown(f"**{t}**  \n{txt}")
    if compact:
        st.markdown(ui.links_html([(n, url(n)) for n in ["GAFI — listes noire et grise", "GAFIC", "ENR Haïti (décembre 2025)"]]),
                    unsafe_allow_html=True)
        return
    st.markdown("##### Indicateurs clés")
    ui.df_table(load("haiti/haiti_contexte_pays.csv"),
                {"dimension": "Dimension", "indicateur": "Indicateur", "valeur": "Situation", "periode": "Période", "source": "Source", "lien": "Lien"})
    st.markdown("##### Plan d'action du GAFI : état des exigences")
    plan = load("haiti/haiti_plan_action_gafi.csv").copy()
    ui.df_table(plan, {"n": "N°", "exigence_gafi": "Exigence du GAFI", "statut": "Statut", "avancees": "Avancées",
                       "difficultes": "Difficultés", "lien": "Source"})
    st.caption("Exigences reprises des déclarations publiques du GAFI (février et juin 2026). Statuts et analyses : Comply World Consulting, "
               "à partir de l'ENR, de la BRH, de l'UNODC et de l'ONU.")


def export_sections() -> list:
    """Sections prêtes pour les exports PDF/Word."""
    ctx = load("haiti/haiti_contexte_pays.csv")
    plan = load("haiti/haiti_plan_action_gafi.csv")
    secs = [(TITRE, " ".join(f"{t}. {txt}" for t, txt in SYNTHESE[:1]))]
    secs += [(t, txt) for t, txt in SYNTHESE[1:]]
    secs.append(("Haïti — indicateurs clés", ctx[["dimension", "indicateur", "valeur", "periode", "source", "lien"]]
                 .rename(columns={"dimension": "Dimension", "indicateur": "Indicateur", "valeur": "Situation", "periode": "Période",
                                  "source": "Source", "lien": "Lien"})))
    secs.append(("Plan d'action du GAFI — état des exigences", plan.rename(
        columns={"n": "N°", "exigence_gafi": "Exigence du GAFI", "statut": "Statut", "avancees": "Avancées", "difficultes": "Difficultés", "lien": "Source"})))
    return secs
