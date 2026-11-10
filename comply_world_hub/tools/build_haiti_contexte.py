# -*- coding: utf-8 -*-
"""
Haïti : situation générale du pays et plan d'action du GAFI (liste grise).

Usage : python tools/build_haiti_contexte.py
Produit :
- data/haiti/haiti_contexte_pays.csv     (dimension, indicateur, valeur, periode, source, lien)
- data/haiti/haiti_plan_action_gafi.csv  (n, exigence_gafi, statut, avancees, difficultes, lien)
Sources : déclarations du GAFI (février, juin et octobre 2026), ONU Info (19/10/2026),
DG Trésor (8/07/2026), ENR Haïti (déc. 2025), UNODC (juin 2026), BRH.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ONU = "https://news.un.org/fr/story/2026/10/1159684"
TRESOR = "https://www.tresor.economie.gouv.fr/Pays/HT/indicateurs-et-conjoncture"
GAFI_JUIN = "https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/increased-monitoring-february-2026.html"
GAFI_OCT = "https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/increased-monitoring-october-2026.html"
ENR = "https://www.brh.ht/wp-content/uploads/Rapport_ENR.pdf"
UNODC = "https://www.unodc.org/unodc/en/frontpage/2026/June/haiti-opens-two-new-judicial-poles-to-fight-corruption--money-laundering--arms-trafficking-and-more.html"

ctx = [
    ("Sécurité", "Victimes des violences liées aux gangs", "1 123 tués et 440 blessés", "Juillet – début octobre 2026", "ONU Info", ONU),
    ("Sécurité", "Extension de la violence", "Les gangs gagnent les zones rurales (Artibonite, Léogane, Marigot…) ; prises d'otages et représailles", "Octobre 2026", "ONU Info", ONU),
    ("Sécurité", "Force de répression des gangs", "1 563 membres déployés sur 5 550 autorisés par le Conseil de sécurité", "12 octobre 2026", "ONU Info", ONU),
    ("Humanitaire", "Personnes déplacées", "Près de 1,5 million, dont plus de 740 000 enfants", "Octobre 2026", "ONU Info", ONU),
    ("Politique", "Élections", "Scrutins prévus le 13 décembre 2026 reportés sans nouvelle date ; aucune élection depuis 2016 ; transition prolongée", "Octobre 2026", "ONU Info", ONU),
    ("Économie", "Croissance du PIB", "-2,7 % en 2025, -1,7 % projeté en 2026 : septième année de contraction", "2025-2026", "DG Trésor (FMI)", TRESOR),
    ("Économie", "Inflation", "28,3 % en 2025", "2025", "DG Trésor (FMI)", TRESOR),
    ("Économie", "Transferts de la diaspora", "Environ 16 % du PIB ; la taxe américaine sur les transferts (1er janvier 2026) et la fin du TPS pourraient les réduire de 1,5 à 5 points de PIB", "2026", "DG Trésor (BID)", TRESOR),
    ("Économie", "Taux de change", "Environ 131 HTG pour 1 USD, relativement stable depuis fin 2023", "2026", "DG Trésor (BRH)", TRESOR),
    ("Secteur financier", "Dépendance aux espèces", "Forte, y compris dans l'immobilier, les jeux et la microfinance ; environ 3 milliards USD par an transitent par les maisons de transfert", "Décembre 2025", "ENR Haïti", ENR),
    ("Risque BC/FT", "Évaluation nationale des risques", "Risque global de blanchiment élevé (menace élevée, vulnérabilité moyennement élevée)", "Décembre 2025", "ENR Haïti", ENR),
    ("Justice", "Pôles judiciaires spécialisés", "Pôle crimes financiers et pôle crimes de masse inaugurés le 27 mai 2026", "Mai 2026", "UNODC", UNODC),
    ("GAFI", "Statut", "Sous surveillance renforcée depuis l'engagement de juin 2021 ; tous les délais du plan d'action sont expirés", "Octobre 2026", "GAFI", GAFI_OCT),
    ("GAFI", "Plénière d'octobre 2026", "Haïti a choisi de différer son rapport : le statut publié peut ne pas refléter les derniers progrès", "30 octobre 2026", "GAFI", GAFI_OCT),
]
pd.DataFrame(ctx, columns=["dimension", "indicateur", "valeur", "periode", "source", "lien"]).to_csv(
    ROOT / "data/haiti/haiti_contexte_pays.csv", index=False, encoding="utf-8-sig")

plan = [
    (1, "Achever l'évaluation nationale des risques BC/FT et en diffuser les résultats",
     "Réalisé", "ENR publiée en décembre 2025 ; l'exigence ne figure plus dans la déclaration de juin 2026",
     "Mise à jour à prévoir au moins tous les 5 ans", ENR),
    (2, "Appliquer une supervision LBC/FT fondée sur les risques aux EPNFD les plus exposées",
     "En cours", "Décret 2023 étendu aux EPNFD ; organismes d'autorégulation identifiés",
     "Aucune autorité désignée pour l'immobilier ni pour les jeux (vulnérabilité 0,86) ; aucune DOS reçue de l'immobilier ; organismes d'autorégulation peu outillés", ENR),
    (3, "Rendre accessibles en temps utile les informations de base et sur les bénéficiaires effectifs",
     "En cours", "Seuil BE de 10 % fixé par le décret 2023",
     "Registre de commerce incomplet et non à jour ; pas de registre complet des bénéficiaires effectifs (ENR, axe l)", ENR),
    (4, "Démontrer des enquêtes et poursuites pour blanchiment conformes au profil de risque",
     "En cours", "Pôle judiciaire crimes financiers (mai 2026) ; magistrats, UCREF, ULCC et BAFE formés par l'UNODC",
     "Insécurité qui entrave le fonctionnement des tribunaux ; capacités d'enquête limitées ; peu de condamnations", UNODC),
    (5, "Accroître l'identification, le traçage et le recouvrement des produits du crime",
     "En cours", "Cadre de confiscation prévu par le décret 2023",
     "Bureau de gestion des avoirs saisis et confisqués (BUGASC) encore à mettre en place (ENR, axe c)", ENR),
    (6, "Corriger les déficiences techniques du régime de sanctions financières ciblées",
     "En cours", "Art. 97 à 112 du décret 2023 ; lignes directrices de la BRH du 16 février 2026",
     "Mise en œuvre « sans délai » à démontrer, notamment hors du secteur bancaire", "https://www.brh.ht/notes-de-presse/?act=circulaires"),
    (7, "Surveiller les OBNL exposés au financement du terrorisme selon une approche par les risques",
     "En cours", "Compétence du MJSP prévue par le décret 2023 (art. 71-72)",
     "Identification des OBNL à risque et contrôles ciblés à déployer sans entraver l'aide humanitaire", ENR),
]
pd.DataFrame(plan, columns=["n", "exigence_gafi", "statut", "avancees", "difficultes", "lien"]).to_csv(
    ROOT / "data/haiti/haiti_plan_action_gafi.csv", index=False, encoding="utf-8-sig")
print("contexte :", len(ctx), "lignes ; plan d'action :", len(plan), "lignes")
