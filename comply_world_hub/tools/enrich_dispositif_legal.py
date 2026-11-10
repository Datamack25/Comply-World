# -*- coding: utf-8 -*-
"""
Enrichissement (10/11/2026) : dispositif légal de lutte contre la criminalité financière
(Haïti, France, Union européenne), circulaires BRH, acteurs institutionnels haïtiens,
sanctions pénales du décret du 30 avril 2023 et actualités (UNODC, UCREF, BRH).

Usage : python tools/enrich_dispositif_legal.py   (idempotent : réécrit les fichiers créés,
ajoute les actualités manquantes sans doublon)
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def save(df, rel):
    p = DATA / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False, encoding="utf-8-sig")
    print(f"  {rel:<52} {len(df):>4} lignes")


OFF, CONF, SCAN = "Texte officiel", "À confirmer", "Contenu à analyser (PDF scanné)"
BRH_CIRC = "https://www.brh.ht/notes-de-presse/?act=circulaires"

# =====================================================================================
# 1. CIRCULAIRES BRH (liste publiée sur brh.ht, consultée le 10/11/2026)
# =====================================================================================
circ = [
    ("129-1", "2026-02-06", "Institutions financières", "Mesures préventives contre le blanchiment de capitaux, le financement du terrorisme et de la prolifération",
     "LBC/FT/FP", "En vigueur", SCAN,
     "https://www.brh.ht/wp-content/uploads/Circulaire-CIR-.-BRH-IF-2026-129-1-Aux-Institutions-FinancieEres-6-feevrier-2026-Lutte-contre-le-blanchiment-de-capitaux._0001.pdf"),
    ("Lignes directrices SFC", "2026-02-16", "Institutions financières", "Sanctions financières ciblées liées au terrorisme et à la prolifération des armes de destruction massive",
     "Sanctions / gel", "En vigueur", CONF, BRH_CIRC),
    ("131", "2026-02-06", "Institutions financières", "Protection des consommateurs de produits et services financiers", "Protection de la clientèle", "En vigueur", CONF, BRH_CIRC),
    ("BRH/IMF/2026/1", "2026-02-16", "Institutions de microfinance", "Gestion du risque de crédit", "Prudentiel", "En vigueur", CONF, BRH_CIRC),
    ("BRH/IMF/2026/2", "2026-02-16", "Institutions de microfinance", "Gestion de la liquidité", "Prudentiel", "En vigueur", CONF, BRH_CIRC),
    ("BRH/IMF/2026/3", "2026-02-16", "Institutions de microfinance", "Capital réglementaire minimum", "Prudentiel", "En vigueur", CONF, BRH_CIRC),
    ("10", "2026-04-16", "Coopératives d'épargne et de crédit", "Règles de gouvernance des CEC", "Gouvernance", "En vigueur", CONF, BRH_CIRC),
    ("95-5", "2025-04-16", "Institutions financières", "Conditions et seuils de transmission des déclarations de transactions", "LBC/FT — déclarations", "En vigueur", CONF, BRH_CIRC),
    ("95-4", "2023-11-27", "Institutions financières", "Transmission des déclarations de transactions et seuils", "LBC/FT — déclarations", "Remplacée par 95-5 (à confirmer)", CONF, BRH_CIRC),
    ("99-4", "2023-11-16", "Banques", "Mesures préventives LBC/FT", "LBC/FT", "À articuler avec la 129-1", CONF, BRH_CIRC),
    ("100-4", "2023-11-16", "Banques", "Mesures de mise en œuvre des programmes LBC/FT", "LBC/FT — programme", "À articuler avec la 129-1", CONF, BRH_CIRC),
    ("107-3", "2023-08-30", "Maisons de transfert", "Directives LBC/FT proportionnées aux maisons de transfert", "LBC/FT", "En vigueur", CONF, BRH_CIRC),
    ("89-2 (et addendum du 27/03/2024)", "2020-10-12", "Institutions financières", "Normes minimales de contrôle interne", "Contrôle interne", "En vigueur", CONF, BRH_CIRC),
    ("121", "2021-12-07", "Prestataires de services de paiement électronique", "Prestataires de services de paiement électronique (avis du 21/08/2024)", "Paiements", "En vigueur", CONF, BRH_CIRC),
    ("118", "2021-05-12", "Institutions financières", "Déclarations des opérations de transfert et de change", "Déclarations", "En vigueur", CONF, BRH_CIRC),
    ("119", "2021-05-12", "Institutions financières", "Opérations de change", "Change", "En vigueur", CONF, BRH_CIRC),
    ("114-2", "2020-09-21", "Institutions financières", "Transferts sans contrepartie", "Transferts", "En vigueur", CONF, BRH_CIRC),
    ("128", "", "Bureaux de change", "Circulaire aux bureaux de change", "Change", "En vigueur", CONF, "https://www.brh.ht/wp-content/uploads/Circulaire-128.pdf"),
]
save(pd.DataFrame(circ, columns=["numero", "date", "destinataires", "objet", "domaine", "statut", "fiabilite", "lien"]), "haiti/haiti_circulaires_brh.csv")

# =====================================================================================
# 2. ACTEURS INSTITUTIONNELS HAÏTIENS
# =====================================================================================
acteurs = [
    ("CNLBA", "Comité national de lutte contre le blanchiment des avoirs", "Coordination", "Politique nationale LBC/FT/FP, ENR (déc. 2025), suivi du plan d'action", ""),
    ("UCREF", "Unité centrale de renseignements financiers", "Cellule de renseignement financier", "Réception et analyse des DOS, opposition (48 h), diffusion aux autorités ; MOU avec l'UAF dominicaine (2023) et deux CRF des Îles Caïmans (2024)", "https://www.ucref.gouv.ht"),
    ("BRH", "Banque de la République d'Haïti", "Autorité de contrôle", "Supervision LBC/FT des banques, maisons de transfert, CEC, IMF, bureaux de change, SFD ; circulaires (dont 129-1 du 6/02/2026)", "https://www.brh.ht"),
    ("UCSA (MEF)", "Unité de contrôle et de supervision des assurances", "Autorité de contrôle", "Supervision des compagnies, agents et courtiers d'assurance", ""),
    ("MJSP", "Ministère de la Justice et de la Sécurité publique", "Autorité de contrôle / tutelle", "Approche fondée sur les risques pour les OBNL ; tutelle de la justice pénale", ""),
    ("Organismes d'autorégulation", "SNJH / ASNOP, barreaux / FBH, OCPAH", "Autorégulation", "Encadrement LBC/FT des notaires, avocats et comptables", ""),
    ("ULCC", "Unité de lutte contre la corruption", "Anticorruption", "Prévention et enquêtes de corruption, déclaration de patrimoine, stratégie nationale ; appui UNODC", ""),
    ("BAFE", "Bureau des affaires financières et économiques (PNH)", "Police judiciaire", "Enquêtes sur la criminalité financière et le blanchiment", ""),
    ("Pôles judiciaires spécialisés", "Pôle crimes financiers et pôle crimes de masse", "Justice", "Inaugurés le 27 mai 2026 avec l'appui de l'UNODC et du HCDH : corruption et blanchiment ; trafic d'armes, d'organes et violences sexuelles", "https://www.unodc.org/unodc/en/frontpage/2026/June/haiti-opens-two-new-judicial-poles-to-fight-corruption--money-laundering--arms-trafficking-and-more.html"),
    ("BUGASC", "Bureau de gestion des avoirs saisis et confisqués", "Recouvrement des avoirs", "Prévu par le cadre 2023 — mise en place recommandée par l'ENR (axe c)", ""),
    ("AGD", "Administration générale des douanes", "Douane", "Déclaration transfrontalière d'espèces et d'instruments négociables ; contrebande", ""),
    ("DGI", "Direction générale des impôts", "Fiscalité", "Infractions fiscales (menace très élevée selon l'ENR)", ""),
    ("IGF", "Inspection générale des finances", "Contrôle des finances publiques", "Contrôle de la dépense publique ; formée par l'UNODC", ""),
    ("CNMP", "Commission nationale des marchés publics", "Marchés publics", "Prévention de la corruption dans la commande publique", ""),
    ("LEH", "Loterie de l'État haïtien", "Jeux", "Secteur des jeux (vulnérabilité ENR 0,86) — interlocuteur de l'UCREF", ""),
]
save(pd.DataFrame(acteurs, columns=["sigle", "nom", "role", "missions", "lien"]), "haiti/haiti_acteurs_institutionnels.csv")

# =====================================================================================
# 3. SANCTIONS PÉNALES — DÉCRET DU 30 AVRIL 2023
# =====================================================================================
sanc = [
    ("Blanchiment de capitaux (personne physique)", "7 à 10 ans d'emprisonnement ou amende de 500 000 à 100 000 000 HTG, selon la gravité", "Titre IV, section 2", "Tentative, complicité et entente punies des mêmes peines"),
    ("Blanchiment de capitaux (personne morale)", "Amende égale au quintuple de celle des personnes physiques ; interdiction d'activité, fermeture (définitive ou 5 ans max.), dissolution, publication", "Titre IV, section 2", "Sans préjudice des peines contre les auteurs"),
    ("Infractions connexes des assujettis", "10 à 15 ans de réclusion et amende de 2 000 000 à 100 000 000 HTG", "Titre IV, section 2",
     "Révélation de la DOS au client (tipping-off), destruction de registres, fausse identité, documents tronqués, absence de DOS, blanchiment en bande organisée"),
    ("Financement du terrorisme / de la prolifération", "15 à 20 ans de réclusion ; mêmes peines complémentaires pour les personnes morales", "Titre IV, section 3", "Tentative et complicité punies des mêmes peines"),
    ("Absence de sursis", "Aucune peine pour BC ou FT ne peut être assortie du sursis", "Titre IV", ""),
    ("Repentir", "Réduction de peine si l'auteur aide à prévenir, identifier les auteurs, obtenir des preuves ou priver les organisations de leurs ressources", "Titre IV", ""),
    ("Paiement en espèces interdit", "Amende de 250 000 HTG par transaction au-delà de 400 000 HTG", "Art. 73", "Commerçants, industriels, prestataires"),
    ("Manquements aux obligations de gel", "Sanctions prévues pour violation des art. 98 et 102", "Titre IV", "Gel des fonds — SFC du Conseil de sécurité"),
]
save(pd.DataFrame(sanc, columns=["infraction", "peine", "reference", "precisions"]), "haiti/haiti_sanctions_penales.csv")

# =====================================================================================
# 4. DISPOSITIF LÉGAL CONSOLIDÉ (Haïti / France / UE)
# =====================================================================================
P_PREV, P_REP, P_SFC, P_INST, P_CORR, P_COOP = ("Prévention (assujettis)", "Répression pénale", "Sanctions financières et gel",
                                               "Institutions et supervision", "Corruption et intégrité", "Coopération et recouvrement")
D = []
def add(j, pilier, intitule, reference, contenu, seuil, lien="", fiab=OFF, date=""):
    D.append((j, pilier, intitule, reference, contenu, seuil, date, fiab, lien))

# ---------------- HAÏTI
H = "Haïti"
add(H, P_PREV, "Décret du 30 avril 2023 sanctionnant le BC/FT/FP", "Le Moniteur, Spécial n°12 du 4 mai 2023",
    "Assujettis (IF art. 4, EPNFD art. 5, PSAV art. 6), classification des risques (art. 12), programme (art. 13 et 31), vigilance (art. 25-42), PPE (art. 63-66), virements (art. 47-54), conservation 5 ans (art. 55)",
    "BE > 10 % ; jeux ≥ 50 000 HTG ; métaux précieux ≥ 2 500 000 HTG ; PSAV ≥ 150 000 HTG", "https://www.brh.ht", date="2023-04-30")
add(H, P_PREV, "Déclarations à l'UCREF", "Décret 2023, art. 16 à 24", "DOS sans délai, quel que soit le montant ; déclaration des transactions en espèces ; opposition de l'UCREF",
    "Opposition 48 h ; seuils DTE fixés par la BRH (circ. 95-5)", date="2023-04-30")
add(H, P_PREV, "Circulaire BRH 129-1 aux institutions financières", "BRH, 6 février 2026",
    "Mesures préventives contre le blanchiment de capitaux, le financement du terrorisme et de la prolifération", "Contenu détaillé à analyser", "https://www.brh.ht/wp-content/uploads/Circulaire-CIR-.-BRH-IF-2026-129-1-Aux-Institutions-FinancieEres-6-feevrier-2026-Lutte-contre-le-blanchiment-de-capitaux._0001.pdf", SCAN, "2026-02-06")
add(H, P_PREV, "Circulaire BRH 95-5", "BRH, 16 avril 2025", "Conditions et seuils de transmission des déclarations de transactions", "Seuils fixés par la circulaire", BRH_CIRC, CONF, "2025-04-16")
add(H, P_PREV, "Circulaires BRH 99-4 et 100-4 (banques), 107-3 (maisons de transfert), 89-2 (contrôle interne)", "BRH, 2020-2023",
    "Mesures préventives, programmes LBC/FT, directives proportionnées aux maisons de transfert, normes minimales de contrôle interne", "", BRH_CIRC, CONF)
add(H, P_PREV, "Interdiction des paiements en espèces", "Décret 2023, art. 73", "Paiements aux commerçants, industriels et prestataires", "> 400 000 HTG — amende 250 000 HTG par transaction", date="2023-04-30")
add(H, P_REP, "Blanchiment de capitaux", "Décret 2023, Titre IV section 2", "Personnes physiques et morales ; tentative et complicité", "7-10 ans ou 500 000 à 100 M HTG ; personnes morales : quintuple + interdictions", date="2023-04-30")
add(H, P_REP, "Infractions connexes des assujettis", "Décret 2023, Titre IV section 2", "Tipping-off, destruction de registres, absence de DOS, fausse identité, bande organisée", "10-15 ans de réclusion et 2 M à 100 M HTG", date="2023-04-30")
add(H, P_REP, "Financement du terrorisme et de la prolifération", "Décret 2023, Titre IV section 3", "Actes de FT/FP, tentative, complicité", "15-20 ans de réclusion ; pas de sursis", date="2023-04-30")
add(H, P_REP, "Infractions sous-jacentes", "Lois du 30/04/2014 (traite), du 22/08/2017 (enlèvement), Codes fiscal et des douanes (19/12/2022)", "Menaces très élevées selon l'ENR 2025 : armes, enlèvements, corruption, contrebande, fraude fiscale", "")
add(H, P_SFC, "Gel des fonds — sanctions financières ciblées", "Décret 2023, art. 97 à 112 ; lignes directrices BRH du 16/02/2026", "Mise en œuvre sans délai des listes du Conseil de sécurité (terrorisme, prolifération, régime Haïti 2653)", "Gel immédiat, déclaration à l'autorité", BRH_CIRC, date="2026-02-16")
add(H, P_INST, "UCREF — cellule de renseignement financier", "Décret de réorganisation (Le Moniteur, Spécial n°30 du 21/11/2023)", "Analyse des DOS, coopération avec les CRF étrangères (MOU UAF 2023, Îles Caïmans 2024)", "", "https://www.ucref.gouv.ht", date="2023-11-21")
add(H, P_INST, "BRH, UCSA/MEF, MJSP et organismes d'autorégulation", "Décret 2023, Titre II ch. 4", "Supervision fondée sur les risques ; pouvoirs de contrôle et de sanction", "")
add(H, P_INST, "Pôles judiciaires spécialisés", "Inauguration le 27 mai 2026", "Pôle crimes financiers (corruption, blanchiment) et pôle crimes de masse ; magistrats formés par l'UNODC", "",
    "https://www.unodc.org/unodc/en/frontpage/2026/June/haiti-opens-two-new-judicial-poles-to-fight-corruption--money-laundering--arms-trafficking-and-more.html", date="2026-05-27")
add(H, P_INST, "Évaluation nationale des risques", "CNLBA, décembre 2025", "Risque global de BC élevé ; plan d'action en 16 axes", "Mise à jour au moins tous les 5 ans", "https://www.brh.ht/wp-content/uploads/Rapport_ENR.pdf", date="2025-12-01")
add(H, P_CORR, "Loi portant prévention et répression de la corruption", "Loi de 2014", "Incriminations de corruption, enrichissement illicite, détournement", "", fiab=CONF)
add(H, P_CORR, "Unité de lutte contre la corruption (ULCC)", "Décret de création de 2004 ; stratégie nationale", "Prévention, enquêtes, déclaration de patrimoine des agents publics", "",
    "https://www.unodc.org/cld/uploads/res/treaties/strategies/haiti/hti0001s_html/Strategie-nationale-de-lutte-contre-la-corruption.pdf", CONF)
add(H, P_CORR, "Appui de l'UNODC aux institutions anticorruption", "Communiqués UNODC 2026", "Formation de l'ULCC, de l'UCREF, de la CNMP, du BAFE et de l'IGF ; guide d'enquête anticorruption en français et en créole ; plus de 170 ordinateurs ; outil logiciel annoncé le 1er octobre 2026", "",
    "https://www.unodc.org/ropan/en/Noticias/2026_1octubre_haiti_corruption_software.html", CONF, "2026-10-01")
add(H, P_COOP, "Entraide judiciaire et extradition", "Décret 2023, Titre V", "Coopération internationale, demandes d'entraide, confiscation", "")
add(H, P_COOP, "Gestion des avoirs saisis et confisqués (BUGASC)", "Cadre 2023 ; ENR axe c)", "Structure à mettre en place (cadre organique et budgétaire)", "")
add(H, P_COOP, "GAFIC et liste grise du GAFI", "Plénière GAFI du 30/10/2026", "Haïti reste sous surveillance renforcée ; adhésion au Groupe Egmont recherchée (ENR axe h)", "", "https://www.cfatf-gafic.org", date="2026-10-30")

# ---------------- FRANCE
F = "France"
add(F, P_PREV, "Code monétaire et financier — art. L561-1 et s.", "CMF", "Assujettis (L561-2), classification (L561-4-1), vigilance (L561-5 à L561-14-2), DS à Tracfin (L561-15), conservation 5 ans (L561-12)", "BE > 25 %", "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000006154830/")
add(F, P_PREV, "Arrêté du 6 janvier 2021", "JORF", "Dispositif et contrôle interne LCB-FT et gel des avoirs", "", "https://www.legifrance.gouv.fr", date="2021-01-06")
add(F, P_PREV, "Plafond des paiements en espèces", "CMF L112-6 et D112-3", "Paiements en espèces entre professionnels et particuliers", "1 000 € (résidents) ; 15 000 € (non-résidents, dépenses personnelles)")
add(F, P_PREV, "Déclaration transfrontalière d'argent liquide", "Code des douanes art. 464 ; Règl. (UE) 2018/1672", "Entrée ou sortie de l'UE", "≥ 10 000 €")
add(F, P_PREV, "Registre des bénéficiaires effectifs", "CMF L561-45-1 et s.", "Déclaration des BE au greffe ; accès restreint depuis 2024", "")
add(F, P_REP, "Blanchiment simple", "Code pénal art. 324-1", "Faciliter la justification mensongère de l'origine des biens ou concourir à leur placement, dissimulation ou conversion", "5 ans et 375 000 € (amende portée au double du produit possible)")
add(F, P_REP, "Blanchiment aggravé", "Code pénal art. 324-2", "Habituel, facilité professionnelle, bande organisée", "10 ans et 750 000 €")
add(F, P_REP, "Présomption d'origine illicite", "Code pénal art. 324-1-1", "Renversement de la charge de la preuve lorsque l'opération n'a d'autre justification que de dissimuler l'origine des fonds", "")
add(F, P_REP, "Financement du terrorisme", "Code pénal art. 421-2-2", "Fournir, réunir ou gérer des fonds en vue d'un acte terroriste", "10 ans et 225 000 €")
add(F, P_REP, "Fraude fiscale", "CGI art. 1741", "Soustraction frauduleuse à l'impôt", "5 ans et 500 000 € (7 ans et 3 M€ si aggravée)")
add(F, P_REP, "Blanchiment douanier", "Code des douanes art. 415", "Opérations financières portant sur des fonds provenant d'un délit douanier ou de stupéfiants", "2 à 10 ans")
add(F, P_REP, "Loi « narcotrafic » du 13 juin 2025", "Loi n° 2025-532", "Parquet national anticriminalité organisée (PNACO), renforcement des outils contre le blanchiment lié au narcotrafic", "", "https://www.legifrance.gouv.fr", CONF, "2025-06-13")
add(F, P_SFC, "Gel des avoirs", "CMF L562-1 et s.", "Mesures nationales, UE et ONU ; obligation de gel et de déclaration à la DG Trésor", "", "https://gels-avoirs.dgtresor.gouv.fr")
add(F, P_INST, "Tracfin", "CMF L561-23", "Cellule de renseignement financier", "", "https://www.economie.gouv.fr/tracfin")
add(F, P_INST, "ACPR et AMF", "CMF L561-36", "Supervision LCB-FT des secteurs banque, assurance, paiement, marchés et PSCA", "Commission des sanctions ACPR : jusqu'à 100 M€ ou 10 % du chiffre d'affaires", "https://acpr.banque-france.fr")
add(F, P_INST, "DGCCRF, ANJ et organismes d'autorégulation", "CMF L561-36", "Agents immobiliers, jeux, professions du chiffre et du droit (ordres, H2A, CNB, CSN)", "")
add(F, P_INST, "Parquet national financier (PNF)", "Loi du 6 décembre 2013", "Poursuite des atteintes à la probité et des fraudes complexes", "")
add(F, P_INST, "COLB", "Conseil d'orientation de la lutte contre le blanchiment", "Coordination nationale et analyse nationale des risques", "")
add(F, P_CORR, "Loi Sapin II", "Loi n° 2016-1691 du 9 décembre 2016", "Programme anticorruption (art. 17) pour les sociétés ≥ 500 salariés et CA > 100 M€ ; AFA ; CJIP", "Sanctions AFA : jusqu'à 1 M€ (personnes morales)")
add(F, P_CORR, "Corruption d'agent public", "Code pénal art. 432-11 et 433-1", "Corruption passive et active", "10 ans et 1 M€ (ou double du produit)")
add(F, P_COOP, "AGRASC", "Code de procédure pénale art. 706-159", "Gestion et recouvrement des avoirs saisis et confisqués", "")

# ---------------- UNION EUROPÉENNE
U = "Union européenne"
add(U, P_PREV, "AMLR — Règlement (UE) 2024/1624", "JOUE 19/06/2024", "Règlement unique : vigilance, BE, PPE, déclarations, conservation", "Plafond espèces 10 000 € ; BE ≥ 25 % ; application au 10/07/2027", "https://eur-lex.europa.eu/eli/reg/2024/1624/oj", date="2024-06-19")
add(U, P_PREV, "AMLD6 — Directive (UE) 2024/1640", "JOUE 19/06/2024", "CRF, superviseurs, registres BE et registres de comptes", "Transposition essentiellement au 10/07/2027", "https://eur-lex.europa.eu/eli/dir/2024/1640/oj", date="2024-06-19")
add(U, P_PREV, "AMLD4/AMLD5 — Directive (UE) 2015/849 modifiée", "", "Cadre applicable jusqu'à l'entrée en application de l'AMLR", "")
add(U, P_PREV, "TFR — Règlement (UE) 2023/1113", "", "Informations accompagnant les transferts de fonds et de crypto-actifs", "Crypto-actifs : sans seuil", "https://eur-lex.europa.eu/eli/reg/2023/1113/oj")
add(U, P_PREV, "Contrôles de l'argent liquide — Règlement (UE) 2018/1672", "", "Déclaration aux frontières extérieures de l'UE", "≥ 10 000 €")
add(U, P_PREV, "Liste UE des pays tiers à haut risque", "Règl. délégué (UE) 2016/1675 modifié", "Vigilance renforcée obligatoire", "Version en vigueur au 29/01/2026", "https://eur-lex.europa.eu/eli/reg_del/2016/1675/oj", date="2026-01-29")
add(U, P_REP, "Directive (UE) 2018/1673 — droit pénal du blanchiment", "", "Harmonisation des infractions sous-jacentes et des peines", "Peine maximale d'au moins 4 ans")
add(U, P_REP, "Directive (UE) 2024/1226 — violation des mesures restrictives", "", "Incrimination du contournement des sanctions de l'UE", "Transposition au 20/05/2025")
add(U, P_REP, "Directive (UE) 2017/1371 (PIF)", "", "Fraude portant atteinte aux intérêts financiers de l'Union", "")
add(U, P_SFC, "Règlements UE de mesures restrictives", "Art. 215 TFUE ; règl. 2580/2001, 881/2002, 269/2014, 833/2014…", "Gel des avoirs et interdictions sectorielles", "", "https://www.sanctionsmap.eu")
add(U, P_INST, "AMLA — Règlement (UE) 2024/1620", "Francfort", "Normes techniques, convergence des superviseurs, supervision directe dès 2028", "Projets finaux de RTS transmis le 01/10/2026", "https://www.amla.europa.eu", date="2026-10-01")
add(U, P_INST, "Parquet européen (EPPO) — Règlement (UE) 2017/1939", "", "Poursuite des fraudes aux intérêts financiers de l'UE, dont le blanchiment associé", "")
add(U, P_COOP, "Directive (UE) 2024/1260 — recouvrement et confiscation des avoirs", "", "Bureaux de recouvrement, confiscation élargie, gestion des avoirs", "Transposition au 23/11/2027")
add(U, P_COOP, "Europol, Eurojust, OLAF", "", "Coopération policière, judiciaire et antifraude", "")

disp = pd.DataFrame(D, columns=["juridiction", "pilier", "intitule", "reference", "contenu", "seuil_ou_sanction", "date", "fiabilite", "lien"])
save(disp, "referentiels/dispositif_legal_criminalite_financiere.csv")

# =====================================================================================
# 5. HAÏTI — cadre juridique : ajouts
# =====================================================================================
cj = pd.read_csv(DATA / "haiti/haiti_cadre_juridique.csv", encoding="utf-8-sig")
add_cj = [
    ("HT-17", "Circulaire BRH 129-1 aux institutions financières — mesures préventives LBC/FT/FP", "2026-02-06", "BRH", "Mesures préventives des institutions financières",
     "En vigueur", "Texte publié en PDF scanné : contenu détaillé à analyser et à intégrer aux parcours.", "https://www.brh.ht/wp-content/uploads/Circulaire-CIR-.-BRH-IF-2026-129-1-Aux-Institutions-FinancieEres-6-feevrier-2026-Lutte-contre-le-blanchiment-de-capitaux._0001.pdf"),
    ("HT-18", "Lignes directrices BRH sur les sanctions financières ciblées (terrorisme et prolifération)", "2026-02-16", "BRH", "Mise en œuvre du gel des fonds", "En vigueur", "Complète les art. 97 à 112 du décret 2023.", BRH_CIRC),
    ("HT-19", "Circulaire BRH 95-5 — conditions et seuils de déclaration des transactions", "2025-04-16", "BRH", "Déclarations de transactions", "En vigueur", "Fixe les seuils visés aux art. 16 à 18 du décret 2023.", BRH_CIRC),
    ("HT-20", "Loi portant prévention et répression de la corruption", "2014", "Le Moniteur", "Corruption, enrichissement illicite", "En vigueur (date exacte à confirmer)", "Infraction sous-jacente — corruption : menace très élevée (ENR 2025).", ""),
]
cj = cj[~cj.id.isin([r[0] for r in add_cj])]
cj = pd.concat([cj, pd.DataFrame(add_cj, columns=cj.columns)], ignore_index=True)
save(cj, "haiti/haiti_cadre_juridique.csv")

# =====================================================================================
# 6. ACTUALITÉS — ajouts sans doublon
# =====================================================================================
act = pd.read_csv(DATA / "veille/veille_actualites.csv", encoding="utf-8-sig")
new = [
    ("2026-10-01", "Haïti", "Corruption", "UNODC : outil logiciel au service de la lutte contre la corruption en Haïti",
     "Communiqué du bureau régional de l'UNODC (Panama) du 1er octobre 2026, dans le cadre de l'appui aux institutions anticorruption haïtiennes (ULCC, UCREF, pôles judiciaires). Détails à consulter sur la source.",
     "UNODC", "https://www.unodc.org/ropan/en/Noticias/2026_1octubre_haiti_corruption_software.html", "Saisie consultant"),
    ("2026-05-27", "Haïti", "Justice", "Inauguration de deux pôles judiciaires spécialisés",
     "Un pôle crimes financiers (corruption, blanchiment) et un pôle crimes de masse (armes, organes, violences sexuelles), avec l'appui de l'UNODC et du HCDH. Formation des magistrats et des agents de l'ULCC, de l'UCREF, de la CNMP, du BAFE et de l'IGF ; plus de 170 ordinateurs fournis.",
     "UNODC", "https://www.unodc.org/unodc/en/frontpage/2026/June/haiti-opens-two-new-judicial-poles-to-fight-corruption--money-laundering--arms-trafficking-and-more.html", "Saisie consultant"),
    ("2026-02-16", "Haïti", "Sanctions", "BRH : lignes directrices sur les sanctions financières ciblées",
     "Lignes directrices relatives au gel des fonds liés au terrorisme et à la prolifération, publiées avec trois circulaires prudentielles pour les IMF.", "BRH", BRH_CIRC, "Saisie consultant"),
    ("2026-02-06", "Haïti", "Réglementation", "BRH : circulaire 129-1 sur les mesures préventives LBC/FT/FP",
     "Nouvelle circulaire adressée aux institutions financières, accompagnée de la circulaire 131 sur la protection des consommateurs. Analyse détaillée à intégrer aux procédures.",
     "BRH", "https://www.brh.ht/wp-content/uploads/Circulaire-CIR-.-BRH-IF-2026-129-1-Aux-Institutions-FinancieEres-6-feevrier-2026-Lutte-contre-le-blanchiment-de-capitaux._0001.pdf", "Saisie consultant"),
    ("2025-05-09", "Haïti", "Événement", "UCREF : 12e Salon du droit consacré au crime financier",
     "Programme scientifique coordonné par l'UCREF : « De la prévention à la répression du crime financier : une approche globale et intégrée ».", "UCREF", "https://ucref.gouv.ht/evenements.php", "Saisie consultant"),
    ("2025-04-16", "Haïti", "Réglementation", "BRH : circulaire 95-5 sur les seuils de déclaration des transactions",
     "Conditions et seuils de transmission des déclarations de transactions par les institutions financières.", "BRH", BRH_CIRC, "Saisie consultant"),
    ("2024-06-01", "Haïti", "Coopération", "UCREF : deux protocoles d'accord signés aux Îles Caïmans",
     "Renforcement des échanges d'informations avec les CRF de la Caraïbe. (Année 2024 ; date précise non publiée par l'UCREF.)", "UCREF", "https://ucref.gouv.ht/evenements.php", "Saisie consultant"),
    ("2023-06-01", "Haïti", "Coopération", "UCREF : protocole d'accord avec l'UAF de la République dominicaine",
     "Coopération bilatérale entre les deux cellules de renseignement financier voisines. (Année 2023 ; date précise non publiée par l'UCREF.)", "UCREF", "https://ucref.gouv.ht/evenements.php", "Saisie consultant"),
]
known = set(act.titre.str.lower())
rows = [r for r in new if r[3].lower() not in known]
act = pd.concat([pd.DataFrame(rows, columns=act.columns), act], ignore_index=True)
save(act, "veille/veille_actualites.csv")

# Sources suivies : page événements UCREF + actualités UNODC Haïti
src = pd.read_csv(DATA / "veille/veille_sources.csv", encoding="utf-8-sig")
add_src = [("UCREF — Événements", "page", "https://ucref.gouv.ht/evenements.php", "Haïti", "Réglementation", 1),
           ("BRH — Circulaires", "page", BRH_CIRC, "Haïti", "Réglementation", 1),
           ("Actualités — UNODC Haïti corruption", "rss", "https://news.google.com/rss/search?q=UNODC+Ha%C3%AFti+corruption&hl=fr&gl=FR&ceid=FR:fr", "Haïti", "Corruption", 1)]
src = pd.concat([src, pd.DataFrame([r for r in add_src if r[2] not in set(src.url)], columns=src.columns)], ignore_index=True)
save(src, "veille/veille_sources.csv")
print("Terminé.")
