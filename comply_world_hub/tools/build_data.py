# -*- coding: utf-8 -*-
"""
Génère les référentiels CSV de la plateforme Comply World Consulting.

Usage :  python tools/build_data.py
Les CSV sont écrits dans data/. Ils peuvent ensuite être modifiés à la main
ou remplacés depuis l'espace administrateur (onglet « Référentiels »).

Sources principales (à la date du 10 novembre 2026) :
- Haïti : Décret du 30 avril 2023 sanctionnant le BC/FT/FP (Le Moniteur, Spécial n°12 du 4 mai 2023) ;
  Décret portant réorganisation de l'UCREF (Le Moniteur, Spécial n°30 du 21 novembre 2023) ;
  Loi du 7 octobre 1982 sur les sociétés financières de développement ;
  Évaluation nationale des risques BC/FT (CNLBA, décembre 2025).
- UE / France : AMLR (UE) 2024/1624, AMLD6 (UE) 2024/1640, Règl. AMLA (UE) 2024/1620, TFR (UE) 2023/1113,
  CMF art. L561-1 et s., Arrêté du 6 janvier 2021, Règl. délégué (UE) 2016/1675 modifié (version du 29/01/2026).
- GAFI : décisions de la plénière du 28-30 octobre 2026.
- Amériques : BSA / 31 CFR ch. X (US), LRPCFAT/PCMLTFA + lois C-12 et C-15 (CA), LFPIORPI réformée (MX),
  Ley 155-17 (RD).
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MAJ = "2026-11-10"


def save(df: pd.DataFrame, rel: str):
    p = DATA / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False, encoding="utf-8-sig")
    print(f"  {rel:<55} {len(df):>4} lignes")


# =====================================================================================
# 1. HAÏTI
# =====================================================================================
haiti_cadre = [
    ("HT-01", "Décret du 30 avril 2023 sanctionnant le blanchiment de capitaux, le financement du terrorisme et le financement de la prolifération des armes de destruction massive",
     "2023-04-30", "Le Moniteur, Spécial n°12 du 4 mai 2023", "Texte cadre LBC/FT/FP : champ des assujettis (IF et EPNFD), vigilance, DOS, gel, sanctions, coopération",
     "En vigueur", "Abroge les lois du 21 février 2001, du 11 novembre 2013 et du 28 septembre 2016 (art. 188). BE : > 10 % du capital ou des droits de vote. Conservation : 5 ans. DOS sans délai à l'UCREF, quel que soit le montant.",
     "https://www.brh.ht"),
    ("HT-02", "Décret portant réorganisation de l'Unité centrale de renseignements financiers (UCREF)",
     "2023-11-21", "Le Moniteur, Spécial n°30 du 21 novembre 2023", "Organisation, missions et fonctionnement de la cellule de renseignement financier",
     "En vigueur", "Réorganise l'UCREF (remplace le cadre de la loi du 8 mai 2017). Annonce de la création du BUGASC (gestion des avoirs saisis et confisqués).",
     "https://www.ucref.gouv.ht"),
    ("HT-03", "Évaluation nationale des risques de BC/FT de la République d'Haïti (ENR)",
     "2025-12-01", "CNLBA — outil Banque mondiale", "Première ENR : menaces, vulnérabilités nationales et sectorielles, inclusion financière, FT, criminalité organisée",
     "Publiée", "Risque global de BC élevé (menace élevée, vulnérabilité moyennement élevée). Jeux de hasard et immobilier : vulnérabilité 0,86. Plan d'action en 16 axes (a à p). Mise à jour au moins tous les 5 ans (décret 2023).",
     "https://www.brh.ht/wp-content/uploads/Rapport_ENR.pdf"),
    ("HT-04", "Loi du 14 mai 2012 sur les banques et autres institutions financières",
     "2012-05-14", "Le Moniteur", "Agrément, gouvernance et supervision des banques par la BRH", "En vigueur", "Base de la supervision prudentielle et LBC/FT des banques.", "https://www.brh.ht"),
    ("HT-05", "Loi du 7 octobre 1982 modifiant le Décret du 10 octobre 1979 sur les sociétés financières de développement",
     "1982-10-07", "Le Moniteur n°70 du 7 octobre 1982", "Statut des sociétés financières de développement (SFD)", "En vigueur",
     "Les SFD sont des institutions financières assujetties (art. 4 du décret 2023). ENR 2025 : vulnérabilité moyennement faible (0,20), 2 institutions dont 1 publique.", "https://www.brh.ht"),
    ("HT-06", "Loi du 26 juin 2002 sur les coopératives d'épargne et de crédit (CEC)", "2002-06-26", "Le Moniteur",
     "Constitution, contrôle et surveillance des CEC et fédérations", "En vigueur", "ENR 2025 : vulnérabilité moyennement élevée (0,6) — dispositif de conformité inégal.", "https://www.brh.ht"),
    ("HT-07", "Décret du 5 juin 2020 sur l'organisation et le fonctionnement des institutions de microfinance", "2020-06-05", "Le Moniteur",
     "Cadre des IMF non mutualistes", "En vigueur", "ENR 2025 : vulnérabilité moyenne (0,4) — forte dépendance aux espèces.", "https://www.brh.ht"),
    ("HT-08", "Décret du 6 juillet 1989 sur les maisons de transfert (modifié le 5 juin 2020)", "1989-07-06", "Le Moniteur",
     "Entreprises de transfert de devises entre le marché international et national", "En vigueur", "ENR 2025 : vulnérabilité moyennement élevée (0,6) — ~3 milliards USD/an de flux transfrontaliers.", "https://www.brh.ht"),
    ("HT-09", "Décret du 25 novembre 2020 sur les intermédiaires de change", "2020-11-25", "Le Moniteur", "Bureaux et intermédiaires de change",
     "En vigueur", "ENR 2025 : vulnérabilité moyennement faible (0,3).", "https://www.brh.ht"),
    ("HT-10", "Décret du 9 avril 2020 portant réglementation des opérations de crédit-bail", "2020-04-09", "Le Moniteur", "Sociétés de crédit-bail", "En vigueur",
     "Institutions financières assujetties (art. 4 du décret 2023).", "https://www.brh.ht"),
    ("HT-11", "Décret du 20 mars 1981 modifiant la loi du 13 juillet 1956 sur les compagnies d'assurance", "1981-03-20", "Le Moniteur", "Compagnies, agents et courtiers d'assurance",
     "En vigueur — modernisation recommandée", "Supervision : MEF via l'Unité de contrôle et de supervision des assurances (UCSA). ENR 2025 : vulnérabilité moyenne (0,50).", ""),
    ("HT-12", "Décret du 9 juin 1989 sur la borlette", "1989-06-09", "Le Moniteur", "Jeux de hasard (borlettes)", "En vigueur — modernisation recommandée",
     "ENR 2025 : jeux de hasard vulnérabilité 0,86 (élevé) ; casinos sans encadrement légal clair.", ""),
    ("HT-13", "Loi du 3 avril 2018 portant réforme du statut de commerçant et organisant le registre de commerce", "2018-04-03", "Le Moniteur", "Registre de commerce",
     "En vigueur", "ENR 2025 : registre incomplet et non à jour ; pas de registre complet des bénéficiaires effectifs (axe l).", ""),
    ("HT-14", "Loi du 30 avril 2014 sur la lutte contre la traite des personnes", "2014-04-30", "Le Moniteur", "Infraction sous-jacente", "En vigueur", "Menace « élevée » et croissante (ENR 2025).", ""),
    ("HT-15", "Loi du 22 août 2017 sur l'enlèvement, la séquestration et la prise d'otages", "2017-08-22", "Le Moniteur", "Infraction sous-jacente", "En vigueur", "Menace « très élevée » et croissante (ENR 2025).", ""),
    ("HT-16", "Décrets du 19 décembre 2022 portant Code fiscal et Code des douanes", "2022-12-19", "Le Moniteur", "Infractions fiscales et douanières", "En vigueur",
     "Infractions fiscales : menace « très élevée » ; contrebande : « très élevée » (ENR 2025).", ""),
]
save(pd.DataFrame(haiti_cadre, columns=["id", "texte", "date", "publication", "objet", "statut", "points_cles", "lien"]), "haiti/haiti_cadre_juridique.csv")

# Entités assujetties — art. 4 (IF) et art. 5 (EPNFD) du décret 2023 + notations ENR 2025
haiti_entites = [
    ("Banque", "Institution financière", "Art. 4", "BRH", "Toute relation d'affaires", 0.43, "Moyennement faible à moyen",
     "Virements internationaux (0,63), dépôts de personnes morales (0,57), crédit grandes entreprises (0,57) : produits les plus vulnérables"),
    ("Société de promotion des investissements / titres", "Institution financière", "Art. 4", "BRH", "Toute relation d'affaires", 0.36, "Moyennement faible",
     "Secteur titres régulé et supervisé par la BRH"),
    ("Société de cartes de crédit", "Institution financière", "Art. 4", "BRH", "Toute relation d'affaires", None, "Non noté séparément", "Contrôle des porteurs et des marchands"),
    ("Société financière de développement (SFD)", "Institution financière", "Art. 4 ; Loi du 7 octobre 1982", "BRH", "Toute relation d'affaires", 0.20, "Moyennement faible",
     "2 institutions dont 1 publique ; activité centrée sur le crédit"),
    ("Société de crédit-bail", "Institution financière", "Art. 4 ; Décret du 9 avril 2020", "BRH", "Toute relation d'affaires", None, "Non noté séparément", "Origine des fonds des preneurs et apports"),
    ("Institution de microfinance (IMF)", "Institution financière", "Art. 4 ; Décret du 5 juin 2020", "BRH", "Toute relation d'affaires", 0.40, "Moyen",
     "Forte dépendance aux espèces, clientèle potentiellement à risque"),
    ("Coopérative d'épargne et de crédit (CEC)", "Institution financière", "Art. 4 ; Loi du 26 juin 2002", "BRH", "Toute relation d'affaires", 0.60, "Moyennement élevé",
     "Poids croissant dans l'épargne ; dispositif de conformité inégal ; manque de formation"),
    ("Maison de transfert", "Institution financière", "Art. 4 ; Décret du 6 juillet 1989", "BRH", "Toute opération", 0.60, "Moyennement élevé",
     "~3 milliards USD/an de flux transfrontaliers ; forte dépendance aux espèces"),
    ("Intermédiaire / bureau de change", "Institution financière", "Art. 4 ; Décret du 25 novembre 2020", "BRH", "Toute opération", 0.30, "Moyennement faible",
     "Activité régulée, double KYC via les banques ; moyens humains et technologiques insuffisants"),
    ("Compagnie, agent ou courtier d'assurance", "Institution financière", "Art. 4", "MEF — UCSA", "Toute relation d'affaires", 0.50, "Moyen",
     "Supervision à professionnaliser ; préparer un éventuel retour de l'assurance vie (axe e)"),
    ("Casino, loterie, borlette, établissement de jeux", "EPNFD", "Art. 5", "Autorité à désigner (LEH / MEF)", "Opérations ≥ 50 000 HTG ; identification des joueurs ≥ 500 000 HTG", 0.86, "Élevé",
     "Volume important d'espèces ; casinos sans encadrement légal clair ; aucune DOS reçue"),
    ("Agent / société immobilière", "EPNFD", "Art. 5", "Aucune autorité désignée", "Opérations d'achat/vente et conseil", 0.86, "Élevé",
     "Aucune DOS jamais transmise à l'UCREF ; prédominance des espèces ; forte informalité"),
    ("Comptable", "EPNFD", "Art. 5", "OCPAH (organisme d'autorégulation)", "Activités listées à l'art. 5", 0.73, "Moyennement élevé", "Aucune procédure ni outil de conformité constatés"),
    ("Avocat / juriste indépendant", "EPNFD", "Art. 5", "Barreaux / FBH (organismes d'autorégulation)", "Activités listées à l'art. 5", 0.73, "Moyennement élevé",
     "Faible sensibilisation ; pas de supervision LBC/FT ciblée des barreaux"),
    ("Notaire", "EPNFD", "Art. 5", "SNJH / ASNOP (organismes d'autorégulation)", "Activités listées à l'art. 5", 0.72, "Moyennement élevé",
     "Meilleure compréhension des obligations, mais absence de directives et de cadre de supervision"),
    ("Négociant en métaux et pierres précieuses, antiquités, œuvres d'art", "EPNFD", "Art. 5", "Autorité à désigner", "Opérations en espèces ≥ 2 500 000 HTG", None, "Non évalué (ENR)",
     "Déclaration des transactions en espèces ≥ 2,5 M HTG (art. 17)"),
    ("Prestataire de services aux sociétés et fiducies", "EPNFD", "Art. 5", "Autorité à désigner", "Constitution, domiciliation, mandats", None, "Non évalué (ENR)", "Transparence des BE"),
    ("Prestataire de services d'actifs virtuels (PSAV)", "PSAV", "Art. 6 (définition)", "Régime réglementaire à préciser (BRH)", "Opérations ≥ 150 000 HTG", None, "Non évalué (ENR)",
     "Régime à préciser par voie réglementaire ; appliquer la règle de voyage (R.16 GAFI)"),
    ("Organisme à but non lucratif (OBNL / ONG)", "OBNL", "Art. 71-72", "MJSP (approche fondée sur les risques)", "OBNL à risque identifiés par le MJSP", None, "Voir ENR ch. 5 (FT)",
     "Identification des OBNL exposés au FT et mesures ciblées"),
]
save(pd.DataFrame(haiti_entites, columns=["type_entite", "famille", "base_legale", "autorite_controle", "seuil_declencheur", "vulnerabilite_enr", "niveau_enr", "points_attention"]),
     "haiti/haiti_entites_assujetties.csv")

haiti_seuils = [
    ("Bénéficiaire effectif", "> 10 % du capital ou des droits de vote (ou contrôle par tout autre moyen)", "Art. 6", "IF et EPNFD"),
    ("Assujettissement des établissements de jeux", "Opérations financières ≥ 50 000 HTG ou équivalent", "Art. 5", "Casinos, loteries, borlettes"),
    ("Identification des joueurs (jetons/plaques)", "≥ 500 000 HTG (ou seuil fixé par l'autorité de contrôle)", "Section 3 — EPNFD", "Casinos et établissements de jeux"),
    ("Négociants en métaux/pierres précieuses", "Opérations en espèces ≥ 2 500 000 HTG", "Art. 5 et 17", "Négociants"),
    ("Actifs virtuels", "Opérations ≥ 150 000 HTG régies par voie réglementaire", "Art. 6", "PSAV"),
    ("Interdiction des paiements en espèces", "> 400 000 HTG auprès des commerçants, industriels et prestataires — amende de 250 000 HTG par transaction", "Art. 73", "Tous"),
    ("Déclaration des transactions en espèces (DTE)", "Seuil fixé par la BRH ; opérations uniques ou liées", "Art. 16-18", "Institutions financières"),
    ("Déclaration transfrontalière d'espèces et INP", "Seuil fixé par le MEF — déclaration à l'AGD", "Art. 14-15", "Voyageurs"),
    ("Déclaration d'opération suspecte (DOS)", "Sans délai, quel que soit le montant, y compris les tentatives", "Art. 19-21", "IF et EPNFD"),
    ("Opposition de l'UCREF", "48 heures, puis gel possible pour une durée supplémentaire", "Art. 24", "IF et EPNFD"),
    ("Conservation des documents", "Au moins 5 ans après la clôture du compte ou la fin de la relation", "Art. 55", "IF et EPNFD"),
    ("Mise à jour de l'ENR", "Au moins tous les 5 ans", "Titre II ch. 1", "CNLBA"),
]
save(pd.DataFrame(haiti_seuils, columns=["obligation", "seuil_ou_regle", "reference", "assujettis"]), "haiti/haiti_seuils_obligations.csv")

haiti_menaces = [
    ("Criminalité organisée (gangs)", "Très élevé", "Croissante", "Enlèvements, extorsion, taxation illégale des flux, infiltration du secteur formel"),
    ("Trafic d'armes et de munitions", "Très élevé", "Croissante", "Expansion ; lien avec la criminalité organisée"),
    ("Enlèvements contre rançon", "Très élevé", "Croissante", "Paiements en espèces et via transferts"),
    ("Corruption et détournement de fonds publics", "Très élevé", "Stable et persistante", "PPE nationales ; marchés publics"),
    ("Contrebande et trafic transfrontalier", "Très élevé", "Active et persistante", "Frontière dominicaine, ports"),
    ("Infractions fiscales", "Très élevé", "Stable et persistante", "Économie informelle (~35 % du PIB)"),
    ("Trafic de stupéfiants", "Élevé", "Stable et persistante", "Transit régional"),
    ("Blanchiment de capitaux", "Élevé", "Stable et persistante", "Fractionnement, sociétés écrans, immobilier, flux transfrontaliers"),
    ("Traite des personnes / trafic de migrants", "Élevé", "Croissante", "Réseaux maritimes"),
]
save(pd.DataFrame(haiti_menaces, columns=["menace", "niveau_global", "tendance", "typologies"]), "haiti/haiti_menaces_enr.csv")

haiti_secteurs = [
    ("Banque", 0.43, "Moyennement faible à moyen"), ("Titres", 0.36, "Moyennement faible"),
    ("Autres institutions financières (AIF)", 0.45, "Moyen"), ("Assurances", 0.50, "Moyen"),
    ("Maisons de transfert", 0.60, "Moyennement élevé"), ("Caisses d'épargne et de crédit", 0.60, "Moyennement élevé"),
    ("Institutions de microfinance", 0.40, "Moyen"), ("Bureaux de change", 0.30, "Moyennement faible"),
    ("Sociétés financières de développement", 0.20, "Moyennement faible"),
    ("Jeux de hasard", 0.86, "Élevé"), ("Immobilier", 0.86, "Élevé"), ("Comptables", 0.73, "Moyennement élevé"),
    ("Avocats", 0.73, "Moyennement élevé"), ("Notaires", 0.72, "Moyennement élevé"),
]
save(pd.DataFrame(haiti_secteurs, columns=["secteur", "vulnerabilite", "niveau"]), "haiti/haiti_vulnerabilites_sectorielles_enr.csv")

haiti_produits = [
    ("Virements internationaux", 0.63, 0.42, "Faible réduction"), ("Dépôts personnes morales", 0.57, 0.38, "Moyenne réduction"),
    ("Crédit grandes entreprises", 0.57, 0.45, "Faible réduction"), ("Comptes courants", 0.54, 0.37, "Moyenne réduction"),
    ("Crédit PME", 0.52, 0.41, "Faible réduction"),
]
save(pd.DataFrame(haiti_produits, columns=["produit", "vulnerabilite_inherente", "vulnerabilite_finale", "effet_controle"]), "haiti/haiti_produits_bancaires_enr.csv")

haiti_actions = [
    ("a", "Adopter une politique nationale et une stratégie coordonnée LBC/FT/FP avec mécanisme de suivi", "Autorités"),
    ("b", "Former et professionnaliser les autorités d'enquête et de poursuite", "Autorités"),
    ("c", "Mettre en place le BUGASC (cadre organique et budgétaire)", "Autorités"),
    ("d", "Moderniser le cadre juridique des EPNFD et désigner leurs autorités de supervision", "Autorités / EPNFD"),
    ("e", "Renforcer la conformité LBC/FT/FP du secteur des assurances", "Assurances / UCSA"),
    ("f", "Moderniser le contrôle douanier", "AGD"),
    ("g", "Renforcer la surveillance maritime intégrée", "Autorités"),
    ("h", "Moderniser l'UCREF, adhésion au Groupe Egmont, outils technologiques", "UCREF"),
    ("i", "Former les enquêteurs (UCREF, BAFE, ULCC) et protéger les enquêteurs", "Autorités"),
    ("j", "Institutionnaliser un système de retour d'information", "UCREF / superviseurs"),
    ("k", "Formaliser l'économie ; stratégie d'intégrité fiscale et financière", "MEF / DGI"),
    ("l", "Créer un registre complet et à jour des bénéficiaires effectifs", "MCI / MEF"),
    ("m", "Renforcer le cadre de conformité de certaines institutions financières", "Assujettis"),
    ("n", "Former et professionnaliser le personnel des IF et des EPNFD", "Assujettis"),
    ("o", "Réévaluer les paramètres et scénarios de surveillance des transactions, ajuster les seuils", "Assujettis"),
    ("p", "Tenir des statistiques de manière systématique", "Tous"),
]
save(pd.DataFrame(haiti_actions, columns=["axe", "action", "porteur"]), "haiti/haiti_actions_prioritaires_enr.csv")

# =====================================================================================
# 2. RÉFÉRENCES PAR JURIDICTION ET PAR THÈME
# =====================================================================================
J_FR, J_HT, J_US, J_CA, J_MX, J_DO = "France / UE", "Haïti", "États-Unis", "Canada", "Mexique", "République dominicaine"

REFS = {
    J_FR: dict(
        gouvernance="CMF L561-32 et R561-38 ; Arrêté du 6 janvier 2021 ; AMLR (UE) 2024/1624 art. 11 à compter du 10/07/2027",
        cadre="CMF L561-1 et s. ; AMLR (UE) 2024/1624 ; AMLD6 (UE) 2024/1640 ; Règl. AMLA (UE) 2024/1620 ; TFR (UE) 2023/1113",
        classification="CMF L561-4-1 ; Arrêté du 6 janvier 2021 ; AMLR art. 10 ; analyse nationale des risques (COLB)",
        procedures="CMF L561-32 ; Arrêté du 6 janvier 2021 ; AMLR art. 9",
        gel="CMF L562-1 et s. ; règlements UE de mesures restrictives ; registre national des gels (DG Trésor)",
        kyc="CMF L561-5, L561-5-1, L561-6 et R561-5 et s. ; AMLR art. 19 à 22 et 26 ; RTS AMLA CDD (projet final 30/09/2026)",
        be="CMF L561-2-2, R561-1 à R561-3 (> 25 %) ; RBE ; AMLR art. 51 et s. (≥ 25 %)",
        ppe="CMF L561-10 et R561-18 ; AMLR art. 42 à 46",
        pays="CMF L561-10 ; Règl. délégué (UE) 2016/1675 modifié (version du 29/01/2026) ; listes GAFI ; AMLR art. 29",
        surveillance="CMF L561-6 et L561-10-2 ; Arrêté du 6 janvier 2021",
        declaration="CMF L561-15 et s. — déclaration de soupçon à Tracfin (ERMES) ; AMLR art. 69",
        declaration_auto="CMF L561-15-1 — communications systématiques d'informations (COSI) à Tracfin selon les catégories prévues",
        conservation="CMF L561-12 (5 ans) ; AMLR art. 77",
        formation="CMF L561-32 ; Arrêté du 6 janvier 2021 ; AMLR art. 12",
        controle="Arrêté du 3 novembre 2014 (contrôle interne) ; Arrêté du 6 janvier 2021",
        audit="Arrêté du 3 novembre 2014 (contrôle périodique) ; AMLR art. 9 (fonction d'audit indépendante)",
        reporting="Questionnaire LCB-FT annuel (ACPR) ; rapport de contrôle interne ; Arrêté du 6 janvier 2021",
        crf="Tracfin", fiabilite="Source officielle"),
    J_HT: dict(
        gouvernance="Décret du 30 avril 2023, art. 13 et 31 c) — responsable de la conformité au niveau de l'administration centrale",
        cadre="Décret du 30 avril 2023 (Le Moniteur, Spécial n°12 du 4 mai 2023) ; Décret de réorganisation de l'UCREF (Spécial n°30 du 21/11/2023) ; Loi du 14 mai 2012 ; circulaire BRH 129-1 du 6/02/2026 (mesures préventives LBC/FT/FP)",
        classification="Décret 2023, art. 12 (classification documentée et tenue à jour) et art. 33 (nouveaux produits et technologies) ; ENR Haïti déc. 2025",
        procedures="Décret 2023, art. 13 (politiques, procédures et contrôles approuvés par la haute direction) et art. 31",
        gel="Décret 2023, art. 97 à 112 — gel des fonds (SFC du Conseil de sécurité) ; lignes directrices BRH du 16/02/2026",
        kyc="Décret 2023, art. 25 à 40 — identification, vérification, objet et nature de la relation",
        be="Décret 2023, art. 6 (BE > 10 %) et art. 41-42",
        ppe="Décret 2023, art. 6 (PPE étrangères, nationales, OI) et art. 63 à 66 (vigilance renforcée)",
        pays="Décret 2023, Titre II ch. 4 — mesures renforcées exigibles pour les pays appliquant insuffisamment les normes ; listes GAFI",
        surveillance="Décret 2023, art. 22 (examen renforcé des opérations complexes ou inhabituelles) ; ENR 2025 axe o)",
        declaration="Décret 2023, art. 19 à 24 — DOS à l'UCREF sans délai, quel que soit le montant ; opposition de 48 h",
        declaration_auto="Décret 2023, art. 16 à 18 — déclaration des transactions ≥ seuils fixés par la circulaire BRH 95-5 (16/04/2025)",
        conservation="Décret 2023, art. 55 — au moins 5 ans",
        formation="Décret 2023, art. 31 d) — formation continue des employés",
        controle="Décret 2023, art. 31 e) et art. 13 ; circulaire BRH 89-2 (normes minimales de contrôle interne)",
        audit="Décret 2023, art. 13 b) — fonction d'audit indépendante",
        reporting="Décret 2023, Titre II ch. 4 — pouvoirs des autorités de contrôle (BRH, UCSA/MEF, organismes d'autorégulation)",
        crf="UCREF", fiabilite="Texte officiel (Le Moniteur)"),
    J_US: dict(
        gouvernance="31 U.S.C. 5318(h) ; 31 CFR 1020.210 (banques) / 1022.210 (MSB) — BSA/AML Officer désigné",
        cadre="Bank Secrecy Act ; AML Act of 2020 ; USA PATRIOT Act ; règles FinCEN (31 CFR ch. X)",
        classification="FFIEC BSA/AML Examination Manual — évaluation des risques ; priorités nationales AML/CFT de FinCEN",
        procedures="31 CFR 1020.210 — programme écrit approuvé par le board",
        gel="OFAC — 31 CFR ch. V ; liste SDN ; déclaration des biens bloqués sous 10 jours ouvrables (31 CFR 501.603)",
        kyc="CIP — 31 CFR 1020.220 ; CDD Rule — 31 CFR 1010.230",
        be="CDD Rule 31 CFR 1010.230 (≥ 25 % + une personne exerçant le contrôle) ; CTA : BOI limité aux sociétés étrangères depuis mars 2025",
        ppe="31 CFR 1010.620 (private banking — senior foreign political figures) ; FFIEC Manual",
        pays="Section 311 USA PATRIOT Act ; avis FinCEN sur les juridictions GAFI",
        surveillance="FFIEC Manual — suspicious activity monitoring",
        declaration="SAR — 31 CFR 1020.320 : dépôt dans les 30 jours calendaires suivant la détection",
        declaration_auto="CTR — opérations en espèces > 10 000 USD (31 CFR 1010.311) ; CMIR ; FBAR",
        conservation="31 CFR 1010.430 — 5 ans",
        formation="31 CFR 1020.210 — formation du personnel (pilier)",
        controle="Contrôles internes (pilier) — 31 CFR 1020.210",
        audit="Independent testing (pilier) — 31 CFR 1020.210",
        reporting="Examens OCC / Fed / FDIC / NCUA / régulateurs d'État ; reporting au board",
        crf="FinCEN", fiabilite="Source officielle"),
    J_CA: dict(
        gouvernance="LRPCFAT/PCMLTFA art. 9.6 ; Règlement art. 156(1)a) — agent de conformité",
        cadre="LRPCFAT/PCMLTFA et règlements ; lois C-12 et C-15 (sanction royale le 26 mars 2026)",
        classification="Règlement art. 156(1)c) — évaluation documentée des risques",
        procedures="Règlement art. 156(1)b) — politiques et procédures écrites approuvées par un cadre supérieur",
        gel="Code criminel art. 83.08 et s. ; Loi sur les mesures économiques spéciales ; Loi Sergueï Magnitski",
        kyc="Règlement — vérification de l'identité selon les méthodes CANAFE/FINTRAC",
        be="Règlement art. 138 (≥ 25 %) ; signalement des divergences BE (C-15)",
        ppe="LRPCFAT art. 9.3 — NPE étrangers et nationaux, dirigeants d'OI",
        pays="Directives ministérielles (partie 1.1 LRPCFAT) ; avis GAFI",
        surveillance="Règlement art. 123.1 — contrôle continu des relations d'affaires",
        declaration="Déclaration d'opération douteuse à CANAFE dès que possible (LRPCFAT art. 7)",
        declaration_auto="Déclarations ≥ 10 000 CAD : espèces (DOIE), télévirements internationaux (DTE), actifs virtuels (DOMV) — règle des 24 h",
        conservation="Règlement art. 148 — 5 ans",
        formation="Règlement art. 156(1)d)-e) — programme de formation écrit et continu",
        controle="Programme de conformité « raisonnablement conçu, fondé sur les risques et efficace » (C-12)",
        audit="Règlement art. 156(3) — examen d'efficacité au moins tous les 2 ans",
        reporting="Inscription obligatoire auprès de CANAFE (C-12) ; pénalités jusqu'à 20 M CAD ou 3 % du revenu mondial",
        crf="CANAFE / FINTRAC", fiabilite="Source officielle"),
    J_MX: dict(
        gouvernance="Disposiciones de carácter general (DCG) CNBV — Oficial de Cumplimiento et Comité de Comunicación y Control ; LFPIORPI — représentant de conformité",
        cadre="LFPIORPI réformée (2025) ; Reglas generales du 7 août 2026 (en vigueur au 30 nov. 2026) ; art. 115 Ley de Instituciones de Crédito ; DCG CNBV",
        classification="Enfoque basado en riesgo (DCG) ; évaluation des risques LFPIORPI exigible au 1er mars 2027",
        procedures="Documento de políticas / Manual de cumplimiento (DCG CNBV)",
        gel="Lista de Personas Bloqueadas (UIF) ; listes du Conseil de sécurité",
        kyc="DCG CNBV — identificación y conocimiento del cliente ; LFPIORPI art. 18",
        be="Beneficiario controlador ≥ 25 % (réforme 2025 — exigible au 1er mars 2027 pour les actividades vulnerables)",
        ppe="Lista de PEP (SHCP) ; DCG — mesures renforcées",
        pays="Listes GAFI ; communications de l'UIF",
        surveillance="Monitoreo automatizado — exigible au 1er juin 2027 (actividades vulnerables)",
        declaration="Reportes de operaciones inusuales / internas preocupantes à l'UIF (délais fixés par les DCG — à confirmer)",
        declaration_auto="Reportes de operaciones relevantes (entités financières) ; avisos au SAT (actividades vulnerables) — seuils à confirmer",
        conservation="10 ans (réforme LFPIORPI 2025) — à confirmer selon le régime",
        formation="Capacitación anual (DCG ; LFPIORPI — 1re période 2027)",
        controle="Área de cumplimiento ; Comité de Comunicación y Control",
        audit="Auditoría anual (DCG) ; 1re période d'audit LFPIORPI en 2028",
        reporting="Supervision CNBV / SAT ; informe al Consejo",
        crf="UIF", fiabilite="À confirmer (texte espagnol)"),
    J_DO: dict(
        gouvernance="Ley 155-17 — Oficial de cumplimiento ; règlements SB / SIMV ; DGII pour les sujetos obligados no financieros",
        cadre="Ley 155-17 contra el lavado de activos y el financiamiento del terrorismo ; Decreto 408-17 (règlement d'application) ; normes de la SB",
        classification="Ley 155-17 — évaluation des risques (approche fondée sur les risques)",
        procedures="Manual de prevención (Ley 155-17 ; instructions SB)",
        gel="Ley 155-17 et Decreto 407-17 — sanctions financières ciblées (ONU)",
        kyc="Ley 155-17 — debida diligencia del cliente",
        be="Ley 155-17 — beneficiario final (seuil à confirmer)",
        ppe="Ley 155-17 — PEP : vigilance renforcée",
        pays="Listes GAFI / GAFILAT",
        surveillance="Monitoreo de transacciones (normes SB)",
        declaration="Reporte de operación sospechosa (ROS) à l'UAF — délai légal à confirmer",
        declaration_auto="Reporte de transacciones en efectivo (RTE) — seuil à confirmer",
        conservation="10 ans (Ley 155-17 — à confirmer)",
        formation="Programa de capacitación (Ley 155-17)",
        controle="Contrôle interne et oficial de cumplimiento",
        audit="Auditoría externa independiente (Ley 155-17)",
        reporting="Supervision SB / SIMV / DGII ; CONCLAFIT",
        crf="UAF", fiabilite="À confirmer (texte espagnol)"),
}

ref_rows = []
for j, d in REFS.items():
    for k, v in d.items():
        if k in ("crf", "fiabilite"):
            continue
        ref_rows.append((j, k, v, d["fiabilite"]))
save(pd.DataFrame(ref_rows, columns=["juridiction", "theme", "reference", "fiabilite"]), "referentiels/references_par_theme.csv")

# =====================================================================================
# 3. PARCOURS DE MISE EN CONFORMITÉ
# =====================================================================================
# Étapes génériques (communes à toutes les entités) — la référence est injectée par juridiction
GENERIC = [
    # phase_no, phase, etape, description, livrable, theme, delai_jours, responsable, priorite
    (1, "Cadrage et gouvernance", "Nommer le responsable conformité LCB-FT et son suppléant",
     "Désigner un responsable disposant de l'indépendance, de l'accès à la direction et des moyens nécessaires ; formaliser sa fiche de fonction.",
     "Décision de nomination + fiche de fonction", "gouvernance", 15, "Direction générale", "Critique"),
    (1, "Cadrage et gouvernance", "Établir l'inventaire réglementaire applicable",
     "Recenser les textes, instructions du superviseur et lignes directrices de la CRF applicables à l'activité.",
     "Registre réglementaire", "cadre", 20, "Conformité", "Haute"),
    (1, "Cadrage et gouvernance", "Faire valider la politique LCB-FT et l'appétence au risque",
     "Présenter à l'organe de direction la politique, les rôles (1re, 2e et 3e lignes) et les limites d'appétence au risque.",
     "Politique LCB-FT signée", "gouvernance", 30, "Direction / Conseil", "Critique"),
    (2, "Évaluation des risques", "Élaborer la classification des risques BC-FT",
     "Cartographier les risques par client, produit, canal, zone géographique ; intégrer l'évaluation nationale des risques et les typologies de la CRF.",
     "Cartographie des risques (Excel)", "classification", 45, "Conformité", "Critique"),
    (2, "Évaluation des risques", "Définir la méthode de scoring client",
     "Fixer les critères, pondérations et seuils de classement (faible / standard / élevé) et les mesures de vigilance associées.",
     "Grille de scoring documentée", "classification", 45, "Conformité", "Haute"),
    (2, "Évaluation des risques", "Évaluer les risques des nouveaux produits et technologies",
     "Instaurer un avis conformité préalable à tout lancement de produit, canal ou technologie.",
     "Procédure « nouveau produit »", "classification", 60, "Conformité / Métiers", "Moyenne"),
    (3, "Corpus procédural", "Rédiger les procédures LCB-FT",
     "Procédures opérationnelles : entrée en relation, vigilance constante, examen renforcé, déclaration, conservation.",
     "Manuel de procédures", "procedures", 60, "Conformité", "Critique"),
    (3, "Corpus procédural", "Formaliser la procédure de gel des avoirs",
     "Filtrage, traitement des homonymies, gel immédiat, information de l'autorité compétente, déblocage.",
     "Procédure sanctions et gel", "gel", 45, "Conformité", "Critique"),
    (3, "Corpus procédural", "Encadrer le recrutement et l'honorabilité du personnel",
     "Critères de sélection exigeants pour les postes exposés, contrôle d'honorabilité.",
     "Procédure RH", "procedures", 60, "RH / Conformité", "Moyenne"),
    (4, "Vigilance clientèle", "Identifier et vérifier l'identité des clients",
     "Collecte et vérification sur documents ou sources fiables et indépendantes, avant l'entrée en relation.",
     "Check-lists KYC personnes physiques / morales", "kyc", 60, "1re ligne", "Critique"),
    (4, "Vigilance clientèle", "Identifier les bénéficiaires effectifs",
     "Remonter la chaîne de détention jusqu'aux personnes physiques ; documenter le contrôle effectif.",
     "Formulaire BE + organigramme de détention", "be", 60, "1re ligne / Conformité", "Critique"),
    (4, "Vigilance clientèle", "Recueillir l'objet de la relation et l'origine des fonds",
     "Profil attendu, origine des fonds et du patrimoine pour les risques élevés.",
     "Questionnaire de connaissance client", "kyc", 60, "1re ligne", "Haute"),
    (4, "Vigilance clientèle", "Détecter les PPE et appliquer la vigilance renforcée",
     "Filtrage PPE, autorisation de la direction, origine du patrimoine, suivi renforcé.",
     "Procédure PPE + registre PPE", "ppe", 60, "Conformité", "Critique"),
    (4, "Vigilance clientèle", "Traiter les pays tiers à haut risque",
     "Appliquer les mesures renforcées aux relations liées aux pays des listes GAFI et, le cas échéant, UE.",
     "Liste pays à risque paramétrée", "pays", 45, "Conformité", "Haute"),
    (4, "Vigilance clientèle", "Remédier le stock de dossiers clients",
     "Plan de mise à niveau priorisé par niveau de risque, avec échéancier et suivi mensuel.",
     "Plan de remédiation KYC", "kyc", 180, "1re ligne / Conformité", "Haute"),
    (5, "Surveillance et déclarations", "Paramétrer le filtrage sanctions",
     "Filtrage à l'entrée en relation, en continu et sur les flux ; mise à jour quotidienne des listes.",
     "Outil de filtrage paramétré + PV de tests", "gel", 60, "Conformité / IT", "Critique"),
    (5, "Surveillance et déclarations", "Déployer les scénarios de surveillance des opérations",
     "Scénarios alignés sur la cartographie (fractionnement, espèces, flux transfrontaliers, comptes de passage) ; seuils calibrés.",
     "Catalogue de scénarios", "surveillance", 90, "Conformité / IT", "Critique"),
    (5, "Surveillance et déclarations", "Organiser la déclaration de soupçon à la CRF",
     "Circuit d'analyse des alertes, décision, déclaration, information complémentaire, confidentialité.",
     "Procédure de déclaration + modèles", "declaration", 45, "Déclarant / Conformité", "Critique"),
    (5, "Surveillance et déclarations", "Mettre en place les déclarations automatiques",
     "Identification systématique des opérations soumises à déclaration de seuil et transmission dans les délais.",
     "Rapports automatiques", "declaration_auto", 60, "Conformité / IT", "Haute"),
    (6, "Conservation, formation et contrôle", "Organiser la conservation des documents",
     "Archivage des pièces KYC et des opérations, restitution rapide sur demande des autorités.",
     "Politique d'archivage", "conservation", 60, "Conformité / IT", "Haute"),
    (6, "Conservation, formation et contrôle", "Déployer le plan de formation",
     "Formation initiale et annuelle adaptée aux métiers ; suivi des présences et des évaluations.",
     "Plan de formation + attestations", "formation", 90, "Conformité / RH", "Haute"),
    (6, "Conservation, formation et contrôle", "Mettre en œuvre le plan de contrôle permanent",
     "Contrôles de 1er et 2e niveau (voir dispositif de contrôle généré), avec indicateurs et plans d'action.",
     "Plan de contrôle + fiches de contrôle", "controle", 90, "Conformité", "Critique"),
    (6, "Conservation, formation et contrôle", "Programmer le contrôle périodique / audit indépendant",
     "Mission d'audit indépendante testant l'efficacité du dispositif.",
     "Rapport d'audit + suivi des recommandations", "audit", 365, "Audit interne / externe", "Haute"),
    (6, "Conservation, formation et contrôle", "Rendre compte à la direction et au superviseur",
     "Rapport annuel LCB-FT, indicateurs clés, incidents, plan d'action.",
     "Rapport annuel LCB-FT", "reporting", 365, "Conformité", "Haute"),
]

# Étapes spécifiques par entité (juridiction, entité) -> liste d'étapes
S = {}
# ---------- France / UE
S[(J_FR, "Établissement de crédit")] = [
    (5, "Surveillance et déclarations", "Contrôler les informations accompagnant les virements", "Vérifier la complétude des données donneur d'ordre / bénéficiaire et traiter les virements incomplets.", "Procédure virements", "TFR (UE) 2023/1113", 60, "Opérations / Conformité", "Haute"),
    (4, "Vigilance clientèle", "Encadrer la correspondance bancaire", "Due diligence des banques correspondantes, interdiction des banques fictives.", "Questionnaires correspondants", "CMF L561-10-3", 90, "Conformité", "Haute"),
]
S[(J_FR, "Établissement de paiement / de monnaie électronique")] = [
    (3, "Corpus procédural", "Encadrer les agents et distributeurs", "Sélection, formation et contrôle des agents ; responsabilité de l'établissement pour leurs opérations.", "Programme de contrôle des agents", "CMF L523-1 et s. ; L525-8", 90, "Conformité", "Critique"),
    (5, "Surveillance et déclarations", "Contrôler les informations accompagnant les transferts de fonds", "Données du donneur d'ordre et du bénéficiaire.", "Procédure transferts", "TFR (UE) 2023/1113", 60, "Opérations", "Haute"),
    (1, "Cadrage et gouvernance", "Désigner un point de contact central (passeport entrant)", "Si l'établissement opère en France via des agents en libre établissement.", "Désignation PCC", "CMF L561-3 ; AMLR", 60, "Direction", "Moyenne"),
]
S[(J_FR, "Prestataire de services sur crypto-actifs (MiCA)")] = [
    (1, "Cadrage et gouvernance", "Sécuriser l'agrément CASP", "Agrément MiCA auprès de l'AMF (fin de la période transitoire française au 1er juillet 2026).", "Dossier d'agrément", "Règl. (UE) 2023/1114 (MiCA)", 120, "Direction", "Critique"),
    (5, "Surveillance et déclarations", "Appliquer la règle de voyage crypto", "Informations accompagnant chaque transfert de crypto-actifs ; vérifications renforcées pour les adresses auto-hébergées.", "Procédure travel rule", "TFR (UE) 2023/1113", 60, "Opérations / Conformité", "Critique"),
    (5, "Surveillance et déclarations", "Déployer l'analyse on-chain", "Scoring des adresses et des transactions, exposition aux mixeurs et aux entités sanctionnées.", "Outil d'analyse blockchain", "AMLR ; orientations AMLA", 60, "Conformité", "Haute"),
]
S[(J_FR, "Entreprise d'investissement / société de gestion")] = [
    (4, "Vigilance clientèle", "Encadrer la connaissance des souscripteurs via les distributeurs", "Répartition des obligations KYC dans la chaîne de distribution des fonds.", "Conventions de distribution", "CMF L561-7 ; RG AMF", 90, "Conformité", "Haute"),
]
S[(J_FR, "Entreprise ou intermédiaire d'assurance")] = [
    (4, "Vigilance clientèle", "Identifier le bénéficiaire du contrat au versement", "Vérification au plus tard au versement des prestations d'assurance vie.", "Procédure prestations", "CMF L561-5 ; AMLR", 60, "Gestion / Conformité", "Haute"),
]
S[(J_FR, "Agent immobilier")] = [
    (4, "Vigilance clientèle", "Identifier les deux parties à la transaction", "Vigilance sur l'acquéreur et le vendeur ; attention aux paiements en espèces et aux montages via sociétés.", "Fiche transaction", "CMF L561-2 8° ; lignes directrices DGCCRF", 45, "Négociateurs", "Critique"),
]
S[(J_FR, "Profession du chiffre ou du droit")] = [
    (5, "Surveillance et déclarations", "Respecter le circuit déclaratif propre à la profession", "Avocats : déclaration via le bâtonnier ; autres professions : directement à Tracfin.", "Procédure déclarative", "CMF L561-17", 30, "Professionnel", "Critique"),
    (6, "Conservation, formation et contrôle", "Préparer le contrôle de l'organisme d'autorégulation", "Dossier de preuve pour le contrôle de l'ordre professionnel.", "Dossier de contrôle", "CMF L561-36", 90, "Professionnel", "Moyenne"),
]
S[(J_FR, "Opérateur de jeux")] = [
    (4, "Vigilance clientèle", "Identifier les joueurs au-delà des seuils", "Identification des joueurs et enregistrement des gains et mises au-delà des seuils réglementaires.", "Registre des joueurs", "CMF L561-13 ; ANJ", 45, "Opérations", "Critique"),
]
# ---------- Haïti
S[(J_HT, "Banque")] = [
    (5, "Surveillance et déclarations", "Renforcer le contrôle des virements internationaux", "Produit le plus vulnérable (0,63) : filtrage automatisé systématique, contrôle des bénéficiaires ultimes et des tiers donneurs d'ordre.", "Scénarios virements + filtrage", "ENR 2025 §3.2.1 ; Décret 2023 art. 47 à 54", 60, "Conformité / Opérations", "Critique"),
    (4, "Vigilance clientèle", "Approfondir le KYB des comptes de personnes morales", "Vulnérabilité 0,57 : vérification de la structure de propriété et des BE, détection des sociétés écrans et des fausses factures.", "Check-list KYB renforcée", "ENR 2025 ; Décret 2023 art. 37-41", 90, "1re ligne / Conformité", "Critique"),
    (4, "Vigilance clientèle", "Intégrer la LBC/FT dans l'octroi de crédit", "Crédit grandes entreprises (0,57) et PME (0,52) : origine des fonds de remboursement, prêts interconnectés.", "Volet LCB-FT du dossier de crédit", "ENR 2025 §3.2.1", 90, "Crédit / Conformité", "Haute"),
    (4, "Vigilance clientèle", "Encadrer la correspondance bancaire", "Informations sur l'institution cliente, sa réputation, son dispositif LBC/FT ; autorisation de la haute direction.", "Questionnaires correspondants", "Décret 2023 — Section 5 (vigilance renforcée)", 90, "Conformité", "Haute"),
]
S[(J_HT, "Maison de transfert")] = [
    (5, "Surveillance et déclarations", "Surveiller les corridors et le fractionnement", "~3 milliards USD/an : scénarios par corridor (États-Unis, République dominicaine, Canada, France, Chili), fractionnement et bénéficiaires multiples.", "Scénarios corridors", "ENR 2025 §3.2.3 ; Décret 2023 art. 22", 60, "Conformité", "Critique"),
    (3, "Corpus procédural", "Contrôler le réseau d'agents et sous-agents", "Sélection, formation, contrôles sur place et suivi des volumes des agents.", "Programme de contrôle des agents", "Décret du 6 juillet 1989 modifié ; Décret 2023 art. 68-70 ; circulaire BRH 107-3 (30/08/2023)", 90, "Réseau / Conformité", "Critique"),
    (5, "Surveillance et déclarations", "Garantir les informations accompagnant les transferts", "Informations complètes donneur d'ordre / bénéficiaire ; suspension des transferts incomplets.", "Contrôle de complétude", "Décret 2023 art. 47 à 54", 45, "Opérations", "Haute"),
]
S[(J_HT, "Coopérative d'épargne et de crédit (CEC)")] = [
    (6, "Conservation, formation et contrôle", "Former les dirigeants élus et les agents", "Faible culture de conformité relevée par l'ENR : formation des conseils d'administration et des comités de crédit.", "Plan de formation dédié", "ENR 2025 §3.2.3 ; Décret 2023 art. 31 d)", 90, "Direction / Conformité", "Critique"),
]
S[(J_HT, "Institution de microfinance (IMF)")] = [
    (5, "Surveillance et déclarations", "Encadrer les remboursements en espèces", "Origine des fonds des remboursements anticipés et des montants inhabituels.", "Scénario remboursements", "ENR 2025 ; Décret 2023 art. 17", 60, "Conformité", "Haute"),
]
S[(J_HT, "Intermédiaire / bureau de change")] = [
    (5, "Surveillance et déclarations", "Tracer les opérations de change en espèces", "Enregistrement des opérations, identification au-delà des seuils et détection des opérations liées.", "Registre des opérations", "Décret du 25 novembre 2020 ; Décret 2023 art. 16-17", 45, "Opérations", "Haute"),
]
S[(J_HT, "Société financière de développement (SFD)")] = [
    (4, "Vigilance clientèle", "Vérifier l'origine des apports et des remboursements", "Activité centrée sur le crédit : contrôle des apports en capital et des remboursements anticipés.", "Procédure crédit-LCB-FT", "Loi du 7 octobre 1982 ; Décret 2023 art. 4", 60, "Crédit / Conformité", "Moyenne"),
]
S[(J_HT, "Compagnie, agent ou courtier d'assurance")] = [
    (4, "Vigilance clientèle", "Identifier le bénéficiaire des prestations", "Identification au plus tard lors du versement des prestations d'assurance vie.", "Procédure prestations", "Décret 2023 art. 67", 60, "Gestion / Conformité", "Haute"),
    (1, "Cadrage et gouvernance", "Préparer la supervision de l'UCSA", "Dossier de conformité à disposition du superviseur (MEF — UCSA).", "Dossier de supervision", "ENR 2025 axe e)", 90, "Direction", "Moyenne"),
]
S[(J_HT, "Casino, loterie, borlette, établissement de jeux")] = [
    (4, "Vigilance clientèle", "Identifier les joueurs au-delà des seuils", "Pièce officielle avec photo, copie conservée, pour les achats/échanges de jetons ≥ 500 000 HTG.", "Registre d'identification", "Décret 2023 — Section 3 (EPNFD)", 30, "Caisse", "Critique"),
    (6, "Conservation, formation et contrôle", "Tenir les registres chronologiques", "Registre des opérations des joueurs et des transferts entre établissements, conservés 5 ans ; comptabilité régulière.", "Registres", "Décret 2023 — Section 3 (EPNFD)", 30, "Direction", "Critique"),
    (5, "Surveillance et déclarations", "Détecter le recyclage d'espèces", "Achats de jetons sans jeu, encaissements de gains fractionnés, tickets gagnants rachetés.", "Scénarios jeux", "ENR 2025 §3.2.5.1", 60, "Conformité", "Critique"),
]
S[(J_HT, "Agent / société immobilière")] = [
    (4, "Vigilance clientèle", "Identifier acquéreurs, vendeurs et BE", "Vulnérabilité 0,86 : identification complète et origine des fonds ; refus des paiements en espèces > 400 000 HTG.", "Fiche transaction", "Décret 2023 art. 5 et 73", 30, "Agents", "Critique"),
    (5, "Surveillance et déclarations", "Créer le circuit de DOS", "Aucune DOS n'a jamais été transmise par le secteur : désigner un déclarant et former les équipes.", "Procédure DOS", "ENR 2025 §3.2.5.5 ; Décret 2023 art. 19", 30, "Direction", "Critique"),
]
for prof, ref in [("Notaire", "SNJH / ASNOP"), ("Avocat / juriste indépendant", "Barreaux / FBH"), ("Comptable", "OCPAH")]:
    S[(J_HT, prof)] = [
        (4, "Vigilance clientèle", "Identifier les opérations assujetties", "Achat/vente d'immeubles, gestion de fonds ou de comptes, constitution et gestion de sociétés, apports.", "Grille d'assujettissement", "Décret 2023 art. 5", 30, "Professionnel", "Critique"),
        (5, "Surveillance et déclarations", "Mettre en place la DOS", "Le secret professionnel n'est pas opposable à l'UCREF ; immunité de bonne foi.", "Procédure DOS", "Décret 2023 — Titre II ch. 4", 30, "Professionnel", "Critique"),
        (1, "Cadrage et gouvernance", f"Se coordonner avec l'organisme d'autorégulation ({ref})", "Lignes directrices, contrôles et retours d'information de l'organisme.", "Convention / correspondance", "ENR 2025 axe d)", 60, "Professionnel", "Moyenne"),
    ]
S[(J_HT, "Négociant en métaux et pierres précieuses, antiquités, œuvres d'art")] = [
    (5, "Surveillance et déclarations", "Déclarer les opérations en espèces ≥ 2,5 M HTG", "Identification du client et déclaration à l'UCREF.", "Registre + déclarations", "Décret 2023 art. 5 et 17", 30, "Direction", "Critique"),
]
S[(J_HT, "Prestataire de services d'actifs virtuels (PSAV)")] = [
    (5, "Surveillance et déclarations", "Appliquer la règle de voyage", "Informations donneur d'ordre / bénéficiaire sur les transferts d'actifs virtuels (R.16 GAFI).", "Procédure travel rule", "Décret 2023 art. 6 ; Recommandation 15 GAFI", 60, "Conformité", "Critique"),
    (1, "Cadrage et gouvernance", "Suivre le régime réglementaire", "Opérations ≥ 150 000 HTG régies par voie réglementaire : veille sur les textes BRH.", "Note de veille", "Décret 2023 art. 6", 30, "Direction", "Haute"),
]
S[(J_HT, "Organisme à but non lucratif (OBNL / ONG)")] = [
    (2, "Évaluation des risques", "Évaluer l'exposition au financement du terrorisme", "Bénéficiaires, zones d'intervention, partenaires d'exécution, flux en espèces.", "Évaluation FT", "Décret 2023 art. 71-72", 45, "Direction", "Haute"),
]
for e in ["Société de promotion des investissements / titres", "Société de cartes de crédit", "Société de crédit-bail", "Prestataire de services aux sociétés et fiducies"]:
    S.setdefault((J_HT, e), [])
# ---------- États-Unis
S[(J_US, "Banque")] = [
    (4, "Vigilance clientèle", "Diligence des comptes de correspondance étrangers", "Due diligence et EDD des comptes de correspondance ; interdiction des shell banks.", "Programme correspondants", "31 CFR 1010.610 / 1010.630", 90, "BSA Officer", "Haute"),
    (5, "Surveillance et déclarations", "Traiter les demandes 314(a) et partager via 314(b)", "Recherches sous 14 jours et partage d'informations entre institutions.", "Procédure 314", "31 CFR 1010.520 / 1010.540", 30, "BSA Officer", "Haute"),
]
S[(J_US, "Money Services Business (MSB)")] = [
    (1, "Cadrage et gouvernance", "Enregistrer le MSB auprès de FinCEN", "Enregistrement dans les 180 jours et renouvellement tous les 2 ans ; liste des agents ; licences d'État.", "Formulaire RMSB + liste d'agents", "31 CFR 1022.380", 30, "Direction", "Critique"),
    (5, "Surveillance et déclarations", "Appliquer la travel rule ≥ 3 000 USD", "Conservation et transmission des informations sur les transferts de fonds.", "Procédure funds transfer", "31 CFR 1010.410", 45, "Opérations", "Haute"),
]
S[(J_US, "Broker-dealer")] = [
    (3, "Corpus procédural", "Aligner le programme sur FINRA Rule 3310", "Programme AML écrit approuvé, test indépendant annuel.", "Programme AML", "FINRA Rule 3310 ; 31 CFR 1023.210", 60, "AML Officer", "Haute"),
]
S[(J_US, "Casino")] = [
    (5, "Surveillance et déclarations", "Déclarer les CTR-C", "Opérations en espèces > 10 000 USD par jour de jeu.", "Rapports CTR-C", "31 CFR 1021.311", 30, "Cage / Compliance", "Critique"),
]
# ---------- Canada
S[(J_CA, "Banque / entité financière")] = [
    (4, "Vigilance clientèle", "Encadrer les relations de correspondant bancaire", "Renseignements, approbation de la haute direction, interdiction des banques fictives.", "Programme correspondants", "LRPCFAT art. 9.4", 90, "Agent de conformité", "Haute"),
]
S[(J_CA, "Entreprise de services monétaires (ESM)")] = [
    (1, "Cadrage et gouvernance", "S'inscrire auprès de CANAFE", "Inscription et renouvellement ; déclaration des changements sous 30 jours (C-12).", "Inscription CANAFE", "LRPCFAT partie 1.1 ; C-12", 30, "Direction", "Critique"),
    (5, "Surveillance et déclarations", "Appliquer la règle de déplacement ≥ 1 000 CAD", "Informations accompagnant les télévirements et transferts d'actifs virtuels.", "Procédure travel rule", "Règlement — règle de déplacement", 45, "Opérations", "Haute"),
]
S[(J_CA, "Courtier ou agent immobilier")] = [
    (4, "Vigilance clientèle", "Vérifier l'identité des parties et tenir les relevés de réception de fonds", "Vérification de l'identité et relevés de réception de fonds ≥ 3 000 CAD.", "Relevés", "Règlement — secteur immobilier ; C-15", 30, "Courtier", "Critique"),
]
S[(J_CA, "Casino")] = [
    (5, "Surveillance et déclarations", "Déclarer les déboursements de casino ≥ 10 000 CAD", "Déclaration des déboursements et des opérations importantes en espèces.", "Déclarations DDC/DOIE", "Règlement — casinos", 30, "Cage / Conformité", "Critique"),
]
S[(J_CA, "Négociant en métaux et pierres précieuses")] = [
    (5, "Surveillance et déclarations", "Identifier et déclarer au-delà de 10 000 CAD", "Achats/ventes en espèces ≥ 10 000 CAD.", "Registre", "Règlement — NMPP", 30, "Direction", "Haute"),
]
# ---------- Mexique
S[(J_MX, "Institución financiera (banque, SOFOM, ITF)")] = [
    (5, "Surveillance et déclarations", "Organiser les trois familles de reportes", "Operaciones relevantes, inusuales et internas preocupantes ; Comité de Comunicación y Control.", "Procédure de reportes", "DCG CNBV — à confirmer", 60, "Oficial de Cumplimiento", "Critique"),
]
S[(J_MX, "Actividad vulnerable (immobilier, bijouterie, véhicules, dons…)")] = [
    (1, "Cadrage et gouvernance", "S'enregistrer sur le portail PLD du SAT", "Alta et désignation du représentant de conformité.", "Inscription SAT", "LFPIORPI", 30, "Direction", "Critique"),
    (5, "Surveillance et déclarations", "Déposer les avisos dans les délais", "Avisos mensuels au-delà des seuils de déclaration.", "Avisos", "LFPIORPI art. 17-23 — à confirmer", 30, "Représentant", "Critique"),
]
# ---------- République dominicaine
S[(J_DO, "Entidad de intermediación financiera")] = [
    (5, "Surveillance et déclarations", "Déclarer les transactions en espèces (RTE)", "Déclaration systématique des transactions en espèces au-delà du seuil réglementaire.", "Rapports RTE", "Ley 155-17 — à confirmer", 30, "Oficial de cumplimiento", "Critique"),
]
S[(J_DO, "Sujeto obligado no financiero (immobilier, casinos, notaires, joailliers…)")] = [
    (1, "Cadrage et gouvernance", "S'enregistrer auprès de la DGII", "Inscription comme sujeto obligado no financiero et désignation de l'oficial de cumplimiento.", "Inscription DGII", "Ley 155-17 — à confirmer", 30, "Direction", "Critique"),
]

rows = []
for (j, ent), specific in S.items():
    refs = REFS[j]
    for g in GENERIC:
        ph, phase, et, desc, liv, theme, d, resp, prio = g
        rows.append((j, ent, ph, phase, et, desc, liv, refs[theme], d, resp, prio, "Commune", refs["fiabilite"]))
    for sp in specific:
        ph, phase, et, desc, liv, ref, d, resp, prio = sp
        rows.append((j, ent, ph, phase, et, desc, liv, ref, d, resp, prio, "Spécifique à l'entité", refs["fiabilite"]))
parcours = pd.DataFrame(rows, columns=["juridiction", "type_entite", "phase_no", "phase", "etape", "description", "livrable", "reference",
                                       "delai_jours", "responsable", "priorite", "nature", "fiabilite_reference"])
parcours = parcours.sort_values(["juridiction", "type_entite", "phase_no", "delai_jours"], kind="stable")
save(parcours, "parcours/parcours_etapes.csv")

entites = pd.DataFrame([(j, e) for (j, e) in S.keys()], columns=["juridiction", "type_entite"])
save(entites, "parcours/entites_par_juridiction.csv")

# =====================================================================================
# 4. DISPOSITIF DE CONTRÔLE (plan de contrôle permanent)
# =====================================================================================
controles = [
    ("Gouvernance", "Revue annuelle de la politique LCB-FT par l'organe de direction", "N2", "Annuelle", "Revue documentaire", "PV de l'organe de direction", "gouvernance", "Politique revue < 12 mois"),
    ("Gouvernance", "Rapport du responsable conformité à la direction", "N2", "Semestrielle", "Revue documentaire", "Rapport + PV", "reporting", "Nombre de points d'alerte remontés"),
    ("Classification des risques", "Mise à jour de la classification des risques", "N2", "Annuelle et à chaque événement", "Revue + comparaison ENR / typologies CRF", "Cartographie datée et validée", "classification", "Date de dernière mise à jour"),
    ("Classification des risques", "Cohérence du scoring client avec la classification", "N2", "Trimestrielle", "Échantillon de 30 dossiers", "Fiche de contrôle", "classification", "% de dossiers mal classés"),
    ("Vigilance clientèle", "Complétude des dossiers à l'entrée en relation", "N1", "Quotidienne", "100 % des ouvertures", "Check-list signée", "kyc", "% de dossiers complets"),
    ("Vigilance clientèle", "Qualité des dossiers d'entrée en relation", "N2", "Mensuelle", "Échantillon aléatoire (≥ 5 %)", "Fiche de contrôle", "kyc", "Taux d'anomalies"),
    ("Vigilance clientèle", "Identification des bénéficiaires effectifs", "N2", "Trimestrielle", "Échantillon personnes morales à risque", "Fiche de contrôle + organigrammes", "be", "% BE identifiés et vérifiés"),
    ("Vigilance clientèle", "Mise à jour des dossiers selon le risque", "N2", "Mensuelle", "Suivi de l'échéancier de revue", "Tableau de bord", "kyc", "% de revues en retard"),
    ("Vigilance clientèle", "Validation des relations PPE par la direction", "N2", "Mensuelle", "100 % des PPE", "Autorisations signées", "ppe", "% PPE avec autorisation"),
    ("Vigilance clientèle", "Mesures renforcées pays à haut risque", "N2", "Trimestrielle", "Revue des relations liées aux pays listés", "Fiche de contrôle", "pays", "Nombre de relations concernées"),
    ("Sanctions et gel", "Filtrage à l'entrée en relation", "N1", "Temps réel", "Automatique", "Journal de filtrage", "gel", "Délai de traitement des alertes"),
    ("Sanctions et gel", "Filtrage des flux", "N1", "Temps réel", "Automatique", "Journal de filtrage", "gel", "% d'alertes traitées sous 24 h"),
    ("Sanctions et gel", "Mise à jour des listes de sanctions", "N2", "Quotidienne", "Contrôle de la date de chargement", "Capture du système", "gel", "Décalage entre publication et chargement"),
    ("Sanctions et gel", "Test de calibrage de l'outil de filtrage", "N2", "Semestrielle", "Jeu de tests (noms, variantes, translittérations)", "PV de tests", "gel", "Taux de détection"),
    ("Surveillance des opérations", "Traitement des alertes dans les délais", "N1/N2", "Hebdomadaire", "Revue du stock d'alertes", "Tableau de bord", "surveillance", "Âge moyen des alertes"),
    ("Surveillance des opérations", "Pertinence des scénarios et des seuils", "N2", "Annuelle", "Analyse rendement (alertes → DOS)", "Note de calibrage", "surveillance", "Taux de conversion alerte/DOS"),
    ("Surveillance des opérations", "Détection du fractionnement des espèces", "N2", "Mensuelle", "Requête sur opérations liées", "Fiche d'analyse", "surveillance", "Nombre de cas détectés"),
    ("Déclarations", "Délai entre détection et déclaration de soupçon", "N2", "Mensuelle", "100 % des DOS", "Registre des DOS", "declaration", "Délai moyen (jours)"),
    ("Déclarations", "Qualité des déclarations de soupçon", "N2", "Trimestrielle", "Revue qualitative", "Fiche de revue", "declaration", "Retours de la CRF"),
    ("Déclarations", "Exhaustivité des déclarations automatiques", "N2", "Mensuelle", "Rapprochement opérations / déclarations", "État de rapprochement", "declaration_auto", "Écarts constatés"),
    ("Conservation", "Capacité de restitution des documents", "N2", "Annuelle", "Test de restitution sur échantillon", "PV de test", "conservation", "Délai de restitution"),
    ("Formation", "Taux de formation du personnel exposé", "N2", "Trimestrielle", "Extraction RH", "Registre de formation", "formation", "% de personnel formé"),
    ("Formation", "Formation des nouveaux arrivants", "N1", "À l'arrivée", "100 % des recrutements", "Attestations", "formation", "% formés sous 3 mois"),
    ("Tiers et agents", "Contrôle des agents, distributeurs et tiers introducteurs", "N2", "Semestrielle", "Échantillon + visites", "Rapport de contrôle", "procedures", "Nombre d'agents en anomalie"),
    ("Audit", "Mission d'audit indépendante du dispositif LCB-FT", "N3", "Annuelle ou biennale", "Mission d'audit", "Rapport d'audit", "audit", "% de recommandations soldées"),
]
crow = []
for j, refs in REFS.items():
    for c in controles:
        dom, ctl, niv, freq, meth, preuve, theme, kri = c
        crow.append((j, dom, ctl, niv, freq, meth, preuve, refs[theme], kri))
save(pd.DataFrame(crow, columns=["juridiction", "domaine", "controle", "niveau", "frequence", "methode", "preuve", "reference", "indicateur"]),
     "parcours/dispositif_controles.csv")

# =====================================================================================
# 5. EUROPE / AMÉRIQUES — RÉFÉRENTIELS
# =====================================================================================
europe = [
    ("UE", "AMLR — Règlement (UE) 2024/1624", "2024-06-19", "Règlement unique LCB-FT (« single rulebook »)", "Applicable au 10 juillet 2027",
     "Plafond de 10 000 € pour les paiements en espèces ; BE ≥ 25 % ; revue KYC 1 an (risque élevé) / 5 ans (autres)", "https://eur-lex.europa.eu/eli/reg/2024/1624/oj"),
    ("UE", "AMLD6 — Directive (UE) 2024/1640", "2024-06-19", "Mécanismes nationaux : CRF, superviseurs, registres BE", "Transposition — l'essentiel au 10 juillet 2027",
     "Registres BE et registres de comptes bancaires interconnectés ; pouvoirs des CRF", "https://eur-lex.europa.eu/eli/dir/2024/1640/oj"),
    ("UE", "Règlement AMLA — (UE) 2024/1620", "2024-06-19", "Autorité européenne de lutte contre le blanchiment (Francfort)", "AMLA opérationnelle ; supervision directe à partir de 2028",
     "Projets finaux de RTS (CDD, seuils art. 19(9), groupes) transmis à la Commission le 1er octobre 2026", "https://www.amla.europa.eu"),
    ("UE", "TFR — Règlement (UE) 2023/1113", "2023-05-31", "Informations accompagnant les transferts de fonds et de crypto-actifs", "Applicable depuis le 30 décembre 2024",
     "Règle de voyage pour les crypto-actifs, sans seuil", "https://eur-lex.europa.eu/eli/reg/2023/1113/oj"),
    ("UE", "MiCA — Règlement (UE) 2023/1114", "2023-05-31", "Marchés de crypto-actifs — agrément des CASP", "Pleinement applicable ; période transitoire française close au 1er juillet 2026",
     "Agrément AMF pour les PSCA en France", "https://eur-lex.europa.eu/eli/reg/2023/1114/oj"),
    ("UE", "Liste UE des pays tiers à haut risque — Règl. délégué (UE) 2016/1675 modifié", "2026-01-29", "Pays soumis à vigilance renforcée", "Version en vigueur depuis le 29 janvier 2026",
     "Ajouts : Bolivie, Îles Vierges britanniques, Russie ; retraits : Burkina Faso, Mali, Mozambique, Nigeria, Afrique du Sud, Tanzanie", "https://eur-lex.europa.eu/eli/reg_del/2016/1675/oj"),
    ("France", "Code monétaire et financier — art. L561-1 et s.", "", "Dispositif national LCB-FT", "En vigueur (jusqu'à l'application de l'AMLR)",
     "Assujettis (L561-2), classification (L561-4-1), vigilance (L561-5 à L561-14-2), déclaration à Tracfin (L561-15)", "https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006072026/"),
    ("France", "Arrêté du 6 janvier 2021 relatif au dispositif et au contrôle interne LCB-FT et de gel des avoirs", "2021-01-06", "Organisation interne et contrôle", "En vigueur",
     "Gouvernance, classification, procédures, contrôle interne, gel", "https://www.legifrance.gouv.fr"),
    ("France", "Lignes directrices et positions de l'ACPR", "", "Interprétation sectorielle", "Mises à jour régulières", "Bénéficiaire effectif, PPE, tiers introducteurs, gel des avoirs", "https://acpr.banque-france.fr"),
    ("France", "Tracfin — déclaration de soupçon (ERMES)", "", "Cellule de renseignement financier", "En vigueur", "Priorités : FT, fraude fiscale et sociale, actifs numériques, immobilier, contournement des sanctions", "https://www.economie.gouv.fr/tracfin"),
    ("France", "Registre national des gels (DG Trésor)", "", "Mesures de gel nationales, UE et ONU", "Mise à jour continue", "Consultation obligatoire pour le filtrage", "https://gels-avoirs.dgtresor.gouv.fr"),
]
save(pd.DataFrame(europe, columns=["perimetre", "texte", "date", "objet", "statut", "points_cles", "lien"]), "europe/europe_cadre_reglementaire.csv")

ameriques = [
    ("États-Unis", "FinCEN (Treasury)", "FinCEN", "OCC, Fed, FDIC, NCUA, SEC, FINRA, régulateurs d'État", "Bank Secrecy Act ; AML Act 2020 ; USA PATRIOT Act",
     "Non listé", "Non listé", "Règle AML des conseillers en investissement reportée au 1er janvier 2028 ; rapport d'évaluation mutuelle GAFI attendu en décembre 2026", "https://www.fincen.gov"),
    ("Canada", "CANAFE / FINTRAC", "CANAFE", "CANAFE ; BSIF (prudentiel)", "LRPCFAT/PCMLTFA ; lois C-12 et C-15 (26 mars 2026)",
     "Non listé", "Non listé", "Pénalités jusqu'à 20 M CAD ou 3 % du revenu mondial ; inscription obligatoire ; projet de loi C-2 en discussion", "https://fintrac-canafe.canada.ca"),
    ("Mexique", "UIF (SHCP)", "UIF", "CNBV, SAT, CNSF", "LFPIORPI réformée (2025) ; Reglas generales 7 août 2026",
     "Non listé", "Non listé", "Règles en vigueur le 30 nov. 2026 ; BE ≥ 25 % au 1er mars 2027 ; rapport d'évaluation mutuelle GAFI attendu en décembre 2026", "https://www.uif.gob.mx"),
    ("République dominicaine", "UAF", "UAF", "SB, SIMV, DGII", "Ley 155-17", "Non listé", "Non listé", "Principal corridor terrestre avec Haïti — contrebande et flux en espèces", "https://www.uaf.gob.do"),
    ("Haïti", "UCREF", "UCREF", "BRH, MEF/UCSA, MJSP, organismes d'autorégulation", "Décret du 30 avril 2023",
     "Surveillance renforcée (liste grise)", "Oui", "ENR décembre 2025 : risque global élevé ; pas encore membre du Groupe Egmont (axe h)", "https://www.ucref.gouv.ht"),
    ("Brésil", "COAF", "COAF", "Banco Central do Brasil, CVM", "Lei 9.613/1998", "Non listé", "Non listé", "Corridor diaspora haïtienne", "https://www.gov.br/coaf"),
    ("Chili", "UAF Chile", "UAF", "CMF Chile", "Ley 19.913", "Non listé", "Non listé", "Corridor diaspora haïtienne", "https://www.uaf.cl"),
    ("Colombie", "UIAF", "UIAF", "Superintendencia Financiera", "SARLAFT", "Non listé", "Non listé", "", "https://www.uiaf.gov.co"),
    ("Panama", "UAF Panamá", "UAF", "SBP", "Ley 23 de 2015", "Non listé", "Non listé", "Sorti de la liste grise GAFI en 2023", "https://www.uaf.gob.pa"),
    ("Jamaïque", "Financial Investigations Division", "FID", "Bank of Jamaica, FSC", "Proceeds of Crime Act", "Non listé", "Non listé", "", "https://www.fid.gov.jm"),
    ("Bahamas", "Financial Intelligence Unit", "FIU", "Central Bank of The Bahamas, SCB", "Financial Transactions Reporting Act", "Non listé", "Non listé", "", ""),
    ("Bolivie", "UIF Bolivia", "UIF", "ASFI", "Ley 004 / normativa UIF", "Surveillance renforcée (liste grise)", "Oui", "Ajoutée à la liste UE en janvier 2026", "https://www.uif.gob.bo"),
    ("Venezuela", "UNIF", "UNIF", "SUDEBAN", "LOCDOFT", "Surveillance renforcée (liste grise)", "Oui", "Sanctions OFAC/UE sectorielles à vérifier", ""),
    ("Îles Vierges britanniques", "FIA", "FIA", "FSC BVI", "Proceeds of Criminal Conduct Act", "Surveillance renforcée (liste grise)", "Oui", "Ajoutées à la liste UE en janvier 2026", ""),
    ("Trinité-et-Tobago", "FIUTT", "FIUTT", "Central Bank of T&T", "Proceeds of Crime Act", "Non listé", "Oui", "Liste UE uniquement", "https://www.fiu.gov.tt"),
]
save(pd.DataFrame(ameriques, columns=["pays", "crf_nom", "crf", "superviseurs", "texte_principal", "statut_gafi_oct2026", "liste_ue_2026", "points_cles", "lien"]),
     "ameriques/ameriques_juridictions.csv")

# =====================================================================================
# 6. LISTES DE PAYS À RISQUE (GAFI oct. 2026 / UE janv. 2026)
# =====================================================================================
gafi_noire = {"Corée du Nord (RPDC)": "Contre-mesures", "Iran": "Contre-mesures", "Myanmar": "Vigilance renforcée (contre-mesures possibles si pas de progrès d'ici février 2027)"}
gafi_grise = ["Angola", "Bolivie", "Bosnie-Herzégovine", "Cameroun", "Haïti", "Irak", "Kenya", "Koweït", "Laos", "Liban", "Népal", "Papouasie-Nouvelle-Guinée",
              "Soudan du Sud", "Syrie", "Venezuela", "Viêt Nam", "Îles Vierges britanniques", "Yémen"]
ue = ["Afghanistan", "Algérie", "Angola", "Bolivie", "Îles Vierges britanniques", "Cameroun", "Côte d'Ivoire", "Corée du Nord (RPDC)", "République démocratique du Congo",
      "Haïti", "Iran", "Kenya", "Laos", "Liban", "Monaco", "Myanmar", "Namibie", "Népal", "Russie", "Soudan du Sud", "Syrie", "Trinité-et-Tobago", "Vanuatu",
      "Venezuela", "Viêt Nam", "Yémen"]
retires_oct = ["Bulgarie", "Côte d'Ivoire", "République démocratique du Congo", "Monaco"]
pays = sorted(set(list(gafi_noire) + gafi_grise + ue + retires_oct))
prow = []
for p in pays:
    g = "Liste noire — " + gafi_noire[p] if p in gafi_noire else ("Liste grise — surveillance renforcée" if p in gafi_grise else
                                                                  ("Retiré de la liste grise le 30/10/2026" if p in retires_oct else "Non listé"))
    u = "Oui" if p in ue else "Non"
    note = ""
    if p in retires_oct and u == "Oui":
        note = "Retiré par le GAFI mais toujours sur la liste UE à la date de mise à jour : appliquer la règle la plus stricte selon votre juridiction"
    prow.append((p, g, u, note, "GAFI 30/10/2026", "UE 29/01/2026"))
save(pd.DataFrame(prow, columns=["pays", "statut_gafi", "liste_ue_haut_risque", "note", "source_gafi", "source_ue"]), "referentiels/pays_a_risque.csv")

# =====================================================================================
# 7. LIENS OFFICIELS
# =====================================================================================
liens = [
    ("International", "GAFI / FATF", "Normes, listes noire et grise", "https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html"),
    ("International", "GAFIC / CFATF", "Organisme régional (Caraïbes) — Haïti", "https://www.cfatf-gafic.org"),
    ("International", "GAFILAT", "Organisme régional (Amérique latine)", "https://www.gafilat.org"),
    ("International", "Conseil de sécurité de l'ONU — liste consolidée", "Sanctions financières ciblées", "https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list"),
    ("International", "Groupe Egmont", "Réseau des CRF", "https://egmontgroup.org"),
    ("UE", "AMLA", "Autorité européenne LCB-FT", "https://www.amla.europa.eu"),
    ("UE", "EUR-Lex — AMLR (UE) 2024/1624", "Texte officiel", "https://eur-lex.europa.eu/eli/reg/2024/1624/oj"),
    ("UE", "EUR-Lex — AMLD6 (UE) 2024/1640", "Texte officiel", "https://eur-lex.europa.eu/eli/dir/2024/1640/oj"),
    ("UE", "EUR-Lex — Liste des pays tiers à haut risque", "Règl. délégué (UE) 2016/1675 consolidé", "https://eur-lex.europa.eu/eli/reg_del/2016/1675/oj"),
    ("UE", "EU Sanctions Map", "Mesures restrictives de l'UE", "https://www.sanctionsmap.eu"),
    ("France", "ACPR", "Superviseur banque / assurance", "https://acpr.banque-france.fr"),
    ("France", "AMF", "Superviseur marchés / PSCA", "https://www.amf-france.org"),
    ("France", "Tracfin", "Cellule de renseignement financier", "https://www.economie.gouv.fr/tracfin"),
    ("France", "Registre national des gels", "DG Trésor", "https://gels-avoirs.dgtresor.gouv.fr"),
    ("France", "Légifrance — Code monétaire et financier", "Texte officiel", "https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006072026/"),
    ("Haïti", "Banque de la République d'Haïti (BRH)", "Superviseur IF — circulaires", "https://www.brh.ht"),
    ("Haïti", "ENR Haïti (décembre 2025)", "Rapport complet", "https://www.brh.ht/wp-content/uploads/Rapport_ENR.pdf"),
    ("Haïti", "UCREF", "Cellule de renseignement financier", "https://www.ucref.gouv.ht"),
    ("Haïti", "Presses nationales d'Haïti — Le Moniteur", "Journal officiel", "https://www.pressesnationalesdhaiti.ht"),
    ("États-Unis", "FinCEN", "CRF et régulateur BSA", "https://www.fincen.gov"),
    ("États-Unis", "OFAC", "Sanctions — liste SDN", "https://ofac.treasury.gov"),
    ("États-Unis", "FFIEC BSA/AML Manual", "Manuel d'examen", "https://bsaaml.ffiec.gov/manual"),
    ("Canada", "CANAFE / FINTRAC", "CRF et superviseur", "https://fintrac-canafe.canada.ca"),
    ("Mexique", "UIF", "Cellule de renseignement financier", "https://www.uif.gob.mx"),
    ("Mexique", "Portal PLD SAT", "Actividades vulnerables", "https://sppld.sat.gob.mx"),
    ("République dominicaine", "UAF", "Cellule de renseignement financier", "https://www.uaf.gob.do"),
    ("République dominicaine", "Superintendencia de Bancos", "Superviseur", "https://www.sb.gob.do"),
]
save(pd.DataFrame(liens, columns=["juridiction", "organisme", "usage", "url"]), "referentiels/liens_officiels.csv")

# =====================================================================================
# 8. ÉCHÉANCIER RÉGLEMENTAIRE
# =====================================================================================
echeances = [
    ("2026-11-30", "Mexique", "Entrée en vigueur des Reglas generales LFPIORPI"),
    ("2026-12-02", "UE", "Fin des tables rondes AMLA sur la vigilance simplifiée — consultation à suivre"),
    ("2026-12-31", "International", "Publication attendue des rapports d'évaluation mutuelle GAFI du Mexique et des États-Unis"),
    ("2027-02-28", "International", "Plénière GAFI de février 2027 (revue de la liste grise, Myanmar)"),
    ("2027-03-01", "Mexique", "BE ≥ 25 %, évaluation des risques et politiques internes exigibles (LFPIORPI)"),
    ("2027-06-01", "Mexique", "Surveillance automatisée exigée (actividades vulnerables)"),
    ("2027-07-10", "UE", "Application de l'AMLR (UE) 2024/1624 et de l'essentiel de l'AMLD6"),
    ("2028-01-01", "États-Unis", "Entrée en vigueur reportée de la règle AML des conseillers en investissement"),
    ("2028-01-01", "UE", "Début de la supervision directe par l'AMLA (sélection des entités en 2027)"),
    ("2030-12-01", "Haïti", "Échéance de mise à jour de l'ENR (au plus tard 5 ans)"),
]
save(pd.DataFrame(echeances, columns=["date", "juridiction", "echeance"]), "referentiels/echeancier.csv")

# =====================================================================================
# 9. VEILLE : SOURCES ET ACTUALITÉS INITIALES
# =====================================================================================
def gnews(q, lang="fr"):
    from urllib.parse import quote_plus
    if lang == "fr":
        return f"https://news.google.com/rss/search?q={quote_plus(q)}&hl=fr&gl=FR&ceid=FR:fr"
    if lang == "es":
        return f"https://news.google.com/rss/search?q={quote_plus(q)}&hl=es-419&gl=MX&ceid=MX:es-419"
    return f"https://news.google.com/rss/search?q={quote_plus(q)}&hl=en-US&gl=US&ceid=US:en"

sources = [
    ("GAFI — listes noire et grise", "page", "https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html", "International", "Pays à risque", 1),
    ("AMLA — site officiel", "page", "https://www.amla.europa.eu", "UE", "Réglementation", 1),
    ("OFAC — Recent Actions", "page", "https://ofac.treasury.gov/recent-actions", "États-Unis", "Sanctions", 1),
    ("FinCEN — News", "page", "https://www.fincen.gov/news-room", "États-Unis", "Réglementation", 1),
    ("CANAFE — Nouveautés", "page", "https://fintrac-canafe.canada.ca/new-neuf/1-fra", "Canada", "Réglementation", 1),
    ("BRH — Chronologie des activités", "page", "https://www.brh.ht/category/chronologie-des-activites/", "Haïti", "Réglementation", 1),
    ("UCREF — site officiel", "page", "https://www.ucref.gouv.ht", "Haïti", "Réglementation", 1),
    ("Actualités — AMLA / AMLR", "rss", gnews("AMLA OR AMLR blanchiment"), "UE", "Réglementation", 1),
    ("Actualités — LCB-FT France (ACPR, Tracfin)", "rss", gnews("LCB-FT ACPR OR Tracfin"), "France", "Réglementation", 1),
    ("Actualités — GAFI liste grise", "rss", gnews("GAFI liste grise"), "International", "Pays à risque", 1),
    ("Actualités — Haïti blanchiment (UCREF, BRH)", "rss", gnews("Haïti UCREF OR BRH blanchiment"), "Haïti", "Réglementation", 1),
    ("Actualités — Haïti sanctions", "rss", gnews("Haiti sanctions OFAC OR \"UN Security Council\"", "en"), "Haïti", "Sanctions", 1),
    ("News — FinCEN AML rule", "rss", gnews("FinCEN AML rule", "en"), "États-Unis", "Réglementation", 1),
    ("News — FINTRAC PCMLTFA", "rss", gnews("FINTRAC PCMLTFA", "en"), "Canada", "Réglementation", 1),
    ("Noticias — UIF México LFPIORPI", "rss", gnews("LFPIORPI UIF lavado", "es"), "Mexique", "Réglementation", 1),
    ("Noticias — UAF República Dominicana", "rss", gnews("UAF República Dominicana lavado de activos", "es"), "République dominicaine", "Réglementation", 1),
    ("Actualités — sanctions UE", "rss", gnews("sanctions UE gel des avoirs"), "UE", "Sanctions", 1),
]
save(pd.DataFrame(sources, columns=["nom", "type", "url", "juridiction", "theme", "actif"]), "veille/veille_sources.csv")

actus = [
    ("2026-10-30", "International", "Pays à risque", "Plénière du GAFI : quatre sorties de la liste grise, Haïti reste sous surveillance renforcée",
     "Bulgarie, Côte d'Ivoire, RDC et Monaco retirés ; aucun ajout. Liste noire inchangée (RPDC, Iran : contre-mesures ; Myanmar : vigilance renforcée). 18 juridictions sous surveillance renforcée, dont Haïti, la Bolivie, le Venezuela et les Îles Vierges britanniques.",
     "ComplyAdvantage", "https://complyadvantage.com/insights/fatf-plenary-october-2026-four-grey-list-exits-a-virtual-asset-review-and-a-new-focus-on-scam-compounds/", "Initiale"),
    ("2026-10-01", "UE", "Réglementation", "AMLA : projets finaux de normes techniques transmis à la Commission",
     "Vigilance à l'égard de la clientèle (art. 28(1) AMLR), relations d'affaires et seuils (art. 19(9)), exigences de groupe (art. 16(4) et 17(3)). Les normes ne deviendront définitives qu'après adoption et publication au JOUE.",
     "Didit", "https://didit.me/blog/amla-final-cdd-standards-october-2026/", "Initiale"),
    ("2026-11-09", "UE", "Réglementation", "AMLA : tables rondes sur la vigilance simplifiée (9 novembre – 2 décembre 2026)",
     "Une consultation publique suivra. Plusieurs orientations AMLR sont attendues entre le T3 2026 et le T2 2027.",
     "Didit", "https://didit.me/blog/amla-final-cdd-standards-october-2026/", "Initiale"),
    ("2026-03-26", "Canada", "Réglementation", "Sanction royale des lois C-12 et C-15 modifiant la LRPCFAT",
     "Pénalités administratives jusqu'à 4 M CAD (personne) et 20 M CAD (entité) ou 3 % du revenu mondial ; accords et ordonnances de conformité ; inscription obligatoire auprès de CANAFE. Le projet de loi C-2 reste en discussion.",
     "DLA Piper", "https://www.dlapiper.com/en-us/insights/publications/2026/03/canada-aml-update-three-bills-make-major-amendments-to-the-pcmltfa", "Initiale"),
    ("2026-08-07", "Mexique", "Réglementation", "Publication des Reglas generales de la LFPIORPI",
     "En vigueur le 30 novembre 2026. BE ≥ 25 %, évaluation des risques et politiques internes au 1er mars 2027 ; surveillance automatisée au 1er juin 2027.",
     "Council on Foundations", "https://cof.org/news/2026-changes-mexicos-anti-money-laundering-law", "Initiale"),
    ("2026-02-05", "États-Unis", "Réglementation", "FinCEN reporte au 1er janvier 2028 la règle AML des conseillers en investissement",
     "Report de deux ans et réexamen annoncé du champ d'application.", "FinTech Global", "https://fintech.global/2026/02/05/fincen-delays-investment-adviser-aml-rule-to-2028/", "Initiale"),
    ("2026-01-29", "UE", "Pays à risque", "Entrée en vigueur de la nouvelle liste UE des pays tiers à haut risque",
     "Règlements délégués (UE) 2026/46 et 2026/83 : ajout de la Bolivie, des Îles Vierges britanniques et de la Russie ; retrait du Burkina Faso, du Mali, du Mozambique, du Nigeria, de l'Afrique du Sud et de la Tanzanie. Haïti reste listé.",
     "Bird & Bird", "https://cm.twobirds.com/en/insights/2026/eu-list-of-highrisk-countries-and-jurisdictions-for-money-laundering-and-terrorism-financing-amended", "Initiale"),
    ("2025-12-01", "Haïti", "Évaluation des risques", "Publication de l'Évaluation nationale des risques BC/FT d'Haïti",
     "Risque global de blanchiment élevé. Menaces très élevées : trafic d'armes, enlèvements, corruption, contrebande, infractions fiscales. EPNFD les plus vulnérables : jeux de hasard et immobilier (0,86). Plan d'action en 16 axes.",
     "CNLBA / BRH", "https://www.brh.ht/wp-content/uploads/Rapport_ENR.pdf", "Initiale"),
    ("2023-11-21", "Haïti", "Réglementation", "Décret portant réorganisation de l'UCREF",
     "Publié au Moniteur (Spécial n°30). Renforce le cadre de la cellule de renseignement financier.", "Le Moniteur", "https://www.ucref.gouv.ht", "Initiale"),
    ("2023-05-04", "Haïti", "Réglementation", "Publication du décret du 30 avril 2023 sanctionnant le BC/FT/FP",
     "Nouveau texte cadre abrogeant les lois de 2001, 2013 et 2016 ; extension aux PSAV ; BE au-delà de 10 % ; interdiction des paiements en espèces au-delà de 400 000 HTG.",
     "Le Moniteur", "https://www.brh.ht", "Initiale"),
]
save(pd.DataFrame(actus, columns=["date", "juridiction", "theme", "titre", "resume", "source", "lien", "origine"]), "veille/veille_actualites.csv")

print("Terminé.")
