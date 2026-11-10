# -*- coding: utf-8 -*-
"""Paramètres de marque et chemins — Comply World Consulting."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RUNTIME = DATA / "runtime"          # données d'exécution (comptes, messages) — non versionnées
RUNTIME.mkdir(parents=True, exist_ok=True)

BRAND = "Comply World Consulting"
BRAND_SHORT = "Comply World"
PRODUCT = "Comply World Compliance Hub"
VERSION = "1.3.0"
VERSION_DATE = "Novembre 2026"
AUTHOR = "Mackenson CINEUS"
TAGLINE = "Conformité LCB-FT, sanctions et contrôle interne — Europe · Haïti · Amériques"

# Coordonnées affichées sur le site (laisser vide pour masquer)
CONTACT_EMAIL = ""
CONTACT_PHONE = ""
CONTACT_CITY = "Paris · Port-au-Prince"
LINKEDIN_URL = ""

DISCLAIMER = (
    "Outil d'aide à la décision — ne se substitue pas à l'analyse humaine ni aux textes officiels "
    "(Code monétaire et financier, AMLR, décret haïtien du 30 avril 2023, textes nationaux des Amériques, "
    "listes officielles de gel). Données indicatives à vérifier auprès des sources officielles."
)

FOOTER_LINE = f"{PRODUCT} · version {VERSION} ({VERSION_DATE}) · Conçu et développé par {AUTHOR}"

JURIDICTIONS = ["France / UE", "Haïti", "États-Unis", "Canada", "Mexique", "République dominicaine"]
ZONES = {
    "Europe": ["France / UE"],
    "Haïti": ["Haïti"],
    "Amériques": ["États-Unis", "Canada", "Mexique", "République dominicaine"],
}

# Offres d'abonnement (activées manuellement par l'administrateur)
PLANS = {
    "Essentiel": ["veille", "referentiel", "pays"],
    "Professionnel": ["veille", "referentiel", "pays", "parcours", "controles", "haiti"],
    "Intégral": ["veille", "referentiel", "pays", "parcours", "controles", "haiti", "exports"],
}
SERVICES_LABELS = {
    "parcours": "Parcours de mise en conformité",
    "controles": "Dispositif de contrôle",
    "haiti": "Cartographie Haïti (ENR 2025)",
    "referentiel": "Référentiel réglementaire",
    "pays": "Pays et corridors à risque",
    "veille": "Actualités réglementaires",
    "exports": "Exports PDF / Word / Excel",
}

# Palette (bleu nuit + cuivre) — distincte des sites de référence
COLORS = dict(
    navy="#0F1E3D", navy2="#1B2E57", copper="#B8743A", copper_light="#E9C9A6",
    ink="#1C2333", muted="#5B6478", line="#E3E6EE", bg="#F7F8FB", white="#FFFFFF",
    green="#2E7D5B", amber="#C58A1B", red="#B23A3A",
)
