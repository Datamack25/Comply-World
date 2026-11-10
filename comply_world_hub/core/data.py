# -*- coding: utf-8 -*-
"""Chargement des référentiels CSV (avec cache) et petites persistances."""
import csv
from datetime import datetime

import pandas as pd
import streamlit as st

from .config import DATA, RUNTIME

# Référentiels modifiables depuis l'administration : clé -> chemin relatif
REFERENTIELS = {
    "Haïti — cadre juridique": "haiti/haiti_cadre_juridique.csv",
    "Haïti — entités assujetties": "haiti/haiti_entites_assujetties.csv",
    "Haïti — seuils et obligations": "haiti/haiti_seuils_obligations.csv",
    "Haïti — menaces (ENR)": "haiti/haiti_menaces_enr.csv",
    "Haïti — vulnérabilités sectorielles (ENR)": "haiti/haiti_vulnerabilites_sectorielles_enr.csv",
    "Haïti — produits bancaires (ENR)": "haiti/haiti_produits_bancaires_enr.csv",
    "Haïti — actions prioritaires (ENR)": "haiti/haiti_actions_prioritaires_enr.csv",
    "Haïti — circulaires BRH": "haiti/haiti_circulaires_brh.csv",
    "Haïti — acteurs institutionnels": "haiti/haiti_acteurs_institutionnels.csv",
    "Haïti — sanctions pénales (décret 2023)": "haiti/haiti_sanctions_penales.csv",
    "Dispositif légal — criminalité financière": "referentiels/dispositif_legal_criminalite_financiere.csv",
    "Fiches juridictions": "referentiels/fiches_juridictions.csv",
    "Haïti — situation du pays": "haiti/haiti_contexte_pays.csv",
    "Haïti — plan d'action GAFI": "haiti/haiti_plan_action_gafi.csv",
    "Circuits de déclaration de soupçon": "referentiels/circuit_declaration.csv",
    "Europe — cadre réglementaire": "europe/europe_cadre_reglementaire.csv",
    "Amériques — juridictions": "ameriques/ameriques_juridictions.csv",
    "Parcours — étapes": "parcours/parcours_etapes.csv",
    "Parcours — entités par juridiction": "parcours/entites_par_juridiction.csv",
    "Dispositif de contrôle": "parcours/dispositif_controles.csv",
    "Références par thème": "referentiels/references_par_theme.csv",
    "Pays à risque": "referentiels/pays_a_risque.csv",
    "Liens officiels": "referentiels/liens_officiels.csv",
    "Échéancier": "referentiels/echeancier.csv",
    "Veille — sources": "veille/veille_sources.csv",
    "Veille — actualités": "veille/veille_actualites.csv",
}


@st.cache_data(show_spinner=False)
def load(rel: str) -> pd.DataFrame:
    p = DATA / rel
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p, encoding="utf-8-sig")


def save(rel: str, df: pd.DataFrame):
    p = DATA / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False, encoding="utf-8-sig")
    load.clear()


def ref(juridiction: str, theme: str) -> str:
    df = load("referentiels/references_par_theme.csv")
    r = df[(df.juridiction == juridiction) & (df.theme == theme)]
    return r.reference.iloc[0] if len(r) else ""


def actualites(n: int | None = None) -> pd.DataFrame:
    df = load("veille/veille_actualites.csv").copy()
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date", ascending=False)
    return df.head(n) if n else df


# ---------------------------------------------------------------- messages de contact
CONTACTS = RUNTIME / "contacts.csv"


def save_contact(name, email, org, subject, message):
    new = not CONTACTS.exists()
    with CONTACTS.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "nom", "email", "organisation", "objet", "message", "statut"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), name, email, org, subject, message, "Nouveau"])


def contacts() -> pd.DataFrame:
    if not CONTACTS.exists():
        return pd.DataFrame(columns=["date", "nom", "email", "organisation", "objet", "message", "statut"])
    return pd.read_csv(CONTACTS)
