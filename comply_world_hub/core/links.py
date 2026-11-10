# -*- coding: utf-8 -*-
"""Liens officiels utilisés dans les pages, les fiches et les exports.

Quand l'adresse exacte d'un texte n'est pas stable (Légifrance, par exemple), on utilise
une recherche Légifrance qui renvoie toujours vers le texte officiel.
"""
from urllib.parse import quote_plus


def lf(q: str) -> str:
    """Recherche Légifrance."""
    return "https://www.legifrance.gouv.fr/search/all?query=" + quote_plus(q)


L = {
    # ---------------- International
    "GAFI": "https://www.fatf-gafi.org",
    "GAFI — Recommandations": "https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html",
    "GAFI — listes noire et grise": "https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html",
    "GAFIC": "https://www.cfatf-gafic.org",
    "GAFILAT": "https://www.gafilat.org",
    "Groupe Egmont": "https://egmontgroup.org",
    "ONU — liste consolidée": "https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list",
    "ONU — régime de sanctions Haïti (2653)": "https://main.un.org/securitycouncil/en/sanctions/2653",
    "UNODC": "https://www.unodc.org",
    # ---------------- Union européenne
    "AMLR (UE) 2024/1624": "https://eur-lex.europa.eu/eli/reg/2024/1624/oj",
    "AMLD6 (UE) 2024/1640": "https://eur-lex.europa.eu/eli/dir/2024/1640/oj",
    "Règlement AMLA (UE) 2024/1620": "https://eur-lex.europa.eu/eli/reg/2024/1620/oj",
    "TFR (UE) 2023/1113": "https://eur-lex.europa.eu/eli/reg/2023/1113/oj",
    "MiCA (UE) 2023/1114": "https://eur-lex.europa.eu/eli/reg/2023/1114/oj",
    "Règlement (UE) 2018/1672 — argent liquide": "https://eur-lex.europa.eu/eli/reg/2018/1672/oj",
    "Liste UE des pays tiers à haut risque": "https://eur-lex.europa.eu/eli/reg_del/2016/1675/oj",
    "AMLA": "https://www.amla.europa.eu",
    "EU Sanctions Map": "https://www.sanctionsmap.eu",
    # ---------------- France
    "CMF — L561-1 et s.": "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000006154830/",
    "CMF — L561-2 (assujettis)": lf("article L561-2 code monétaire et financier"),
    "CMF — L561-15 (déclaration de soupçon)": lf("article L561-15 code monétaire et financier"),
    "CMF — R561-1 (bénéficiaire effectif)": lf("article R561-1 code monétaire et financier"),
    "CMF — L112-6 (plafond espèces)": lf("article L112-6 code monétaire et financier"),
    "CMF — L562-1 (gel des avoirs)": lf("article L562-1 code monétaire et financier"),
    "Arrêté du 6 janvier 2021": lf("arrêté du 6 janvier 2021 dispositif contrôle interne blanchiment gel des avoirs"),
    "Arrêté du 3 novembre 2014": lf("arrêté du 3 novembre 2014 contrôle interne"),
    "Code pénal — art. 324-1": lf("article 324-1 code pénal"),
    "ACPR": "https://acpr.banque-france.fr",
    "ACPR — lignes directrices gel des avoirs": "https://acpr.banque-france.fr/system/files/2025-01/20210616_lignes_directrices_gel_des_avoirs.pdf",
    "AMF": "https://www.amf-france.org",
    "Tracfin": "https://www.economie.gouv.fr/tracfin",
    "Tracfin — quand et comment déclarer": "https://www.economie.gouv.fr/tracfin/vous-etes-professionnel-declarant/quand-et-comment-declarer-un-soupcon",
    "Tracfin — ERMES": "https://www.economie.gouv.fr/tracfin/vous-etes-professionnel-declarant/ermes-la-plateforme-de-declaration-en-ligne-de-tracfin",
    "Registre national des gels": "https://gels-avoirs.dgtresor.gouv.fr",
    "Registre des bénéficiaires effectifs (INPI)": "https://data.inpi.fr",
    # ---------------- Haïti
    "BRH": "https://www.brh.ht",
    "BRH — circulaires": "https://www.brh.ht/notes-de-presse/?act=circulaires",
    "BRH — normes prudentielles": "https://www.brh.ht/supervision-bancaire/normes-prudentielles/",
    "BRH — circulaire 129-1": "https://www.brh.ht/wp-content/uploads/Circulaire-CIR-.-BRH-IF-2026-129-1-Aux-Institutions-FinancieEres-6-feevrier-2026-Lutte-contre-le-blanchiment-de-capitaux._0001.pdf",
    "ENR Haïti (décembre 2025)": "https://www.brh.ht/wp-content/uploads/Rapport_ENR.pdf",
    "UCREF": "https://www.ucref.gouv.ht",
    "UCREF — événements": "https://ucref.gouv.ht/evenements.php",
    "Le Moniteur (Presses nationales)": "https://www.pressesnationalesdhaiti.ht",
    # ---------------- Amériques
    "FinCEN": "https://www.fincen.gov",
    "BSA E-Filing (FinCEN)": "https://bsaefiling.fincen.treas.gov",
    "31 CFR chapitre X": "https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X",
    "FFIEC BSA/AML Manual": "https://bsaaml.ffiec.gov/manual",
    "OFAC": "https://ofac.treasury.gov",
    "OFAC — recherche SDN": "https://sanctionssearch.ofac.treas.gov",
    "CANAFE / FINTRAC": "https://fintrac-canafe.canada.ca",
    "LRPCFAT (Justice Canada)": "https://laws-lois.justice.gc.ca/fra/lois/p-24.501/",
    "UIF Mexique": "https://www.uif.gob.mx",
    "Portail PLD du SAT": "https://sppld.sat.gob.mx",
    "UAF République dominicaine": "https://www.uaf.gob.do",
    "Superintendencia de Bancos (RD)": "https://www.sb.gob.do",
}


def url(name: str) -> str:
    return L.get(name, "")


# Mots-clés → liens (détection automatique dans les textes de référence)
_AUTO = [
    ("129-1", "BRH — circulaire 129-1"), ("circulaire BRH", "BRH — circulaires"), ("Circulaire BRH", "BRH — circulaires"),
    ("Circulaires BRH", "BRH — circulaires"), ("lignes directrices BRH", "BRH — circulaires"), ("BRH", "BRH"),
    ("ENR", "ENR Haïti (décembre 2025)"), ("UCREF", "UCREF"), ("Décret 2023", "Le Moniteur (Presses nationales)"),
    ("décret du 30 avril 2023", "Le Moniteur (Presses nationales)"), ("Décret du 30 avril 2023", "Le Moniteur (Presses nationales)"),
    ("2653", "ONU — régime de sanctions Haïti (2653)"), ("Conseil de sécurité", "ONU — liste consolidée"),
    ("GAFIC", "GAFIC"), ("GAFI", "GAFI — listes noire et grise"), ("OFAC", "OFAC"),
    ("L561-15", "CMF — L561-15 (déclaration de soupçon)"), ("L562-1", "CMF — L562-1 (gel des avoirs)"),
    ("L112-6", "CMF — L112-6 (plafond espèces)"), ("R561-1", "CMF — R561-1 (bénéficiaire effectif)"),
    ("registre des bénéficiaires effectifs", "Registre des bénéficiaires effectifs (INPI)"), ("CMF", "CMF — L561-1 et s."),
    ("6 janvier 2021", "Arrêté du 6 janvier 2021"), ("3 novembre 2014", "Arrêté du 3 novembre 2014"),
    ("AMLR", "AMLR (UE) 2024/1624"), ("AMLD6", "AMLD6 (UE) 2024/1640"), ("AMLA", "AMLA"), ("TFR", "TFR (UE) 2023/1113"),
    ("MiCA", "MiCA (UE) 2023/1114"), ("ERMES", "Tracfin — ERMES"), ("Tracfin", "Tracfin — quand et comment déclarer"),
    ("ACPR", "ACPR"), ("AMF", "AMF"), ("DG Trésor", "Registre national des gels"), ("mesures restrictives", "EU Sanctions Map"),
    ("Règlements UE", "EU Sanctions Map"), ("FinCEN", "FinCEN"), ("CANAFE", "CANAFE / FINTRAC"), ("UIF", "UIF Mexique"), ("UAF", "UAF République dominicaine"),
]
L["EUR-Lex"] = "https://eur-lex.europa.eu"
L["Légifrance"] = "https://www.legifrance.gouv.fr"
L["Directive (UE) 2024/1226"] = "https://eur-lex.europa.eu/eli/dir/2024/1226/oj"
_AUTO += [("JOUE", "EUR-Lex"), ("Légifrance", "Légifrance"), ("2024/1226", "Directive (UE) 2024/1226")]


def autolinks(text: str, maximum: int = 6) -> list[tuple[str, str]]:
    """Liens officiels correspondant aux références citées dans un texte."""
    out, seen = [], set()
    for kw, name in _AUTO:
        if kw in text and L.get(name) and L[name] not in seen:
            # « GAFI » ne doit pas re-déclencher si seul « GAFIC » est cité
            if kw == "GAFI" and "GAFI" not in text.replace("GAFIC", ""):
                continue
            if kw == "BRH" and any(n.startswith("BRH") for n, _ in out):
                continue
            seen.add(L[name]); out.append((name, L[name]))
        if len(out) >= maximum:
            break
    return out
