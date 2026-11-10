# -*- coding: utf-8 -*-
"""
Fiches juridictions (dispositif de mise en conformité) et circuits de déclaration de soupçon.

Usage : python tools/build_fiches.py
Produit :
- data/referentiels/fiches_juridictions.csv  (juridiction, rubrique, ordre, element, detail, lien, fiabilite)
- data/referentiels/circuit_declaration.csv  (juridiction, etape_no, etape, acteur, detail)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd  # noqa: E402
from core.links import L  # noqa: E402

R1, R2, R3, R4, R5, R6, R7, R8 = ("1. Cadre légal LCB-FT", "2. Entités assujetties", "3. Autorités de contrôle",
                                  "4. Déclaration de soupçon : à qui et comment", "5. Seuils et limites de transaction",
                                  "6. Bénéficiaire effectif, KYC et KYB", "7. Sanctions financières et gel des avoirs",
                                  "8. Organismes de référence")
OFF, CONF = "Source officielle", "À confirmer"
rows = []


def add(j, rub, el, det, lien="", fiab=OFF):
    rows.append(dict(juridiction=j, rubrique=rub, element=el, detail=det, lien=L.get(lien, lien), fiabilite=fiab))


# =============================================================================== FRANCE / UE
J = "France / UE"
add(J, R1, "Code monétaire et financier, art. L561-1 et s.", "Socle des obligations préventives jusqu'à l'application de l'AMLR", "CMF — L561-1 et s.")
add(J, R1, "Arrêté du 6 janvier 2021", "Dispositif et contrôle interne LCB-FT et gel des avoirs", "Arrêté du 6 janvier 2021")
add(J, R1, "AMLR — Règlement (UE) 2024/1624", "Règlement unique applicable au 10 juillet 2027", "AMLR (UE) 2024/1624")
add(J, R1, "AMLD6 — Directive (UE) 2024/1640", "CRF, superviseurs, registres", "AMLD6 (UE) 2024/1640")
add(J, R1, "Règlement AMLA (UE) 2024/1620", "Autorité européenne ; supervision directe dès 2028", "Règlement AMLA (UE) 2024/1620")
add(J, R1, "TFR — Règlement (UE) 2023/1113", "Informations accompagnant les transferts de fonds et de crypto-actifs", "TFR (UE) 2023/1113")
add(J, R2, "Secteur financier", "Établissements de crédit, de paiement et de monnaie électronique ; entreprises d'assurance et intermédiaires ; entreprises d'investissement et sociétés de gestion ; changeurs manuels ; prestataires de services sur crypto-actifs", "CMF — L561-2 (assujettis)")
add(J, R2, "Professions non financières", "Notaires, avocats, commissaires de justice, experts-comptables, commissaires aux comptes ; agents immobiliers ; casinos et opérateurs de jeux ; marchands d'art et de biens de grande valeur ; domiciliataires ; administrateurs et mandataires judiciaires", "CMF — L561-2 (assujettis)")
add(J, R3, "ACPR", "Banques, établissements de paiement et de monnaie électronique, assurances", "ACPR")
add(J, R3, "AMF", "Entreprises d'investissement (marchés), sociétés de gestion, prestataires sur crypto-actifs", "AMF")
add(J, R3, "DGCCRF, ANJ, ordres professionnels", "Agents immobiliers et domiciliataires ; jeux ; professions du chiffre et du droit (CNB, CSN, H2A, CNOEC)")
add(J, R4, "Cellule de renseignement financier", "Tracfin (ministère de l'Économie)", "Tracfin")
add(J, R4, "Canal", "Télédéclaration sur ERMES, par le déclarant et le correspondant Tracfin désignés", "Tracfin — ERMES")
add(J, R4, "Quoi déclarer", "Sommes ou opérations dont on sait, soupçonne ou a de bonnes raisons de soupçonner qu'elles proviennent d'une infraction punie de plus d'un an d'emprisonnement ou participent au financement du terrorisme (CMF L561-15)", "CMF — L561-15 (déclaration de soupçon)")
add(J, R4, "Quand", "En principe avant l'exécution de l'opération ; à défaut, sans délai après", "Tracfin — quand et comment déclarer")
add(J, R4, "Opposition et confidentialité", "Tracfin peut s'opposer à l'exécution (10 jours ouvrables) ; interdiction de révéler l'existence de la déclaration (L561-18)")
add(J, R4, "Cas particulier", "Avocats : déclaration au bâtonnier, qui transmet à Tracfin (L561-17)")
add(J, R5, "Paiements en espèces", "1 000 € pour les résidents ; 15 000 € pour les non-résidents (dépenses personnelles)", "CMF — L112-6 (plafond espèces)")
add(J, R5, "Argent liquide aux frontières de l'UE", "Déclaration obligatoire à partir de 10 000 €", "Règlement (UE) 2018/1672 — argent liquide")
add(J, R5, "Opérations occasionnelles", "Vigilance au-delà de 15 000 € (seuils réduits pour certains secteurs)")
add(J, R5, "Plafond européen", "10 000 € pour les paiements en espèces à compter du 10 juillet 2027 (AMLR)", "AMLR (UE) 2024/1624")
add(J, R6, "Bénéficiaire effectif", "Personne physique détenant plus de 25 % du capital ou des droits de vote, ou exerçant un contrôle (R561-1)", "CMF — R561-1 (bénéficiaire effectif)")
add(J, R6, "Registre des bénéficiaires effectifs", "Consultation obligatoire ; signalement des divergences", "Registre des bénéficiaires effectifs (INPI)")
add(J, R6, "KYC", "Identification et vérification avant l'entrée en relation ; vérification à distance selon R561-5-1 ; objet et nature de la relation")
add(J, R6, "KYB", "Kbis, statuts, liste des dirigeants et mandataires, organigramme de détention jusqu'aux personnes physiques")
add(J, R6, "PPE et revue", "Vigilance renforcée des PPE (L561-10) ; AMLR : revue annuelle (risque élevé) et quinquennale (autres)")
add(J, R7, "Gel des avoirs", "Gel sans délai et déclaration à la DG Trésor (CMF L562-1 et s.)", "CMF — L562-1 (gel des avoirs)")
add(J, R7, "Registre national des gels", "Mesures nationales, UE et ONU", "Registre national des gels")
add(J, R7, "Lignes directrices ACPR – DG Trésor", "Mise en œuvre du gel des avoirs", "ACPR — lignes directrices gel des avoirs")
add(J, R7, "Mesures restrictives de l'UE", "Carte des sanctions de l'Union", "EU Sanctions Map")
add(J, R8, "GAFI", "Normes internationales (40 recommandations)", "GAFI — Recommandations")
add(J, R8, "AMLA", "Normes techniques européennes", "AMLA")
add(J, R8, "Groupe Egmont", "Réseau des cellules de renseignement financier", "Groupe Egmont")

# =============================================================================== HAÏTI
J = "Haïti"
add(J, R1, "Décret du 30 avril 2023", "Texte cadre BC/FT/FP (Le Moniteur, Spécial n°12 du 4 mai 2023)", "Le Moniteur (Presses nationales)")
add(J, R1, "Décret de réorganisation de l'UCREF", "Le Moniteur, Spécial n°30 du 21 novembre 2023", "UCREF")
add(J, R1, "Circulaire BRH 129-1 (6 février 2026)", "Mesures préventives des institutions financières", "BRH — circulaire 129-1")
add(J, R1, "Autres circulaires BRH", "95-5 (seuils de déclaration), 99-4 et 100-4 (banques), 107-3 (maisons de transfert), 89-2 (contrôle interne)", "BRH — circulaires")
add(J, R1, "Évaluation nationale des risques", "CNLBA, décembre 2025 : risque global élevé", "ENR Haïti (décembre 2025)")
add(J, R2, "Institutions financières (art. 4)", "Banques, sociétés de promotion des investissements, cartes de crédit, SFD, crédit-bail, IMF, CEC, maisons de transfert, intermédiaires de change, assurances")
add(J, R2, "EPNFD (art. 5)", "Casinos, loteries, borlettes ; agents immobiliers ; notaires, avocats, comptables ; négociants en métaux et pierres précieuses ; prestataires de services aux sociétés et fiducies")
add(J, R2, "Autres", "Prestataires de services d'actifs virtuels (art. 6) ; OBNL à risque (art. 71-72)")
add(J, R3, "BRH", "Institutions financières, maisons de transfert, CEC, IMF, bureaux de change", "BRH")
add(J, R3, "UCSA (MEF)", "Compagnies, agents et courtiers d'assurance")
add(J, R3, "MJSP", "Organismes à but non lucratif")
add(J, R3, "Organismes d'autorégulation", "Notaires (SNJH / ASNOP), avocats (barreaux / FBH), comptables (OCPAH)")
add(J, R3, "À désigner", "Immobilier et jeux de hasard : autorité de supervision à désigner (ENR, axe d)")
add(J, R4, "Cellule de renseignement financier", "UCREF — Unité centrale de renseignements financiers", "UCREF")
add(J, R4, "Quoi et quand", "DOS sans délai, quel que soit le montant, y compris les tentatives (art. 19 à 21)")
add(J, R4, "Canal", "Selon les modalités fixées par l'UCREF (formulaire et transmission sécurisée)", "UCREF", CONF)
add(J, R4, "Opposition", "L'UCREF peut s'opposer à l'exécution pendant 48 heures (art. 24)")
add(J, R4, "Confidentialité", "Révéler la déclaration ou s'abstenir de déclarer : 10 à 15 ans de réclusion et 2 à 100 millions HTG ; secret professionnel non opposable ; immunité de bonne foi")
add(J, R4, "Déclarations de transactions", "Selon les seuils de la circulaire BRH 95-5 (art. 16 à 18)", "BRH — circulaires")
add(J, R5, "Paiements en espèces", "Interdits au-delà de 400 000 HTG ; amende de 250 000 HTG par transaction (art. 73)")
add(J, R5, "Jeux de hasard", "Assujettissement à partir de 50 000 HTG ; identification des joueurs à partir de 500 000 HTG")
add(J, R5, "Métaux et pierres précieuses", "Opérations en espèces à partir de 2 500 000 HTG")
add(J, R5, "Actifs virtuels", "Opérations à partir de 150 000 HTG régies par voie réglementaire")
add(J, R5, "Espèces aux frontières", "Déclaration à l'AGD au-delà du seuil fixé par le MEF (art. 14-15)")
add(J, R6, "Bénéficiaire effectif", "Personne physique détenant plus de 10 % du capital ou des droits de vote, ou exerçant un contrôle (art. 6)")
add(J, R6, "KYC", "Identification et vérification sur documents fiables ; objet et nature de la relation (art. 25 à 40)")
add(J, R6, "KYB", "Statuts, registre de commerce (incomplet selon l'ENR : sources complémentaires), dirigeants, chaîne de détention")
add(J, R6, "PPE", "PPE étrangères, nationales et d'organisations internationales : vigilance renforcée (art. 63 à 66)")
add(J, R7, "Gel des fonds", "Gel sans délai des fonds des personnes désignées par le Conseil de sécurité (art. 97 à 112)")
add(J, R7, "Lignes directrices BRH", "Sanctions financières ciblées (terrorisme et prolifération), 16 février 2026", "BRH — circulaires")
add(J, R7, "Régime ONU Haïti", "Comité des sanctions créé par la résolution 2653", "ONU — régime de sanctions Haïti (2653)")
add(J, R7, "OFAC", "Désignations visant des acteurs haïtiens, à filtrer pour les flux en dollars", "OFAC — recherche SDN")
add(J, R8, "GAFI", "Haïti sous surveillance renforcée (liste grise, octobre 2026)", "GAFI — listes noire et grise")
add(J, R8, "GAFIC", "Organisme régional d'évaluation (Caraïbes)", "GAFIC")
add(J, R8, "Groupe Egmont", "Adhésion de l'UCREF recherchée (ENR, axe h)", "Groupe Egmont")
add(J, R8, "UNODC", "Appui aux pôles judiciaires et aux institutions anticorruption", "UNODC")

# =============================================================================== ÉTATS-UNIS
J = "États-Unis"
add(J, R1, "Bank Secrecy Act et AML Act of 2020", "Socle fédéral ; règles FinCEN au 31 CFR chapitre X", "31 CFR chapitre X")
add(J, R1, "FFIEC BSA/AML Examination Manual", "Référentiel d'examen des superviseurs bancaires", "FFIEC BSA/AML Manual")
add(J, R2, "Institutions couvertes", "Banques, money services businesses, broker-dealers, casinos, assureurs (produits couverts), négociants en métaux précieux, systèmes de cartes, prêteurs non bancaires")
add(J, R3, "FinCEN et superviseurs délégués", "OCC, Fed, FDIC, NCUA, SEC, FINRA, IRS (MSB et casinos), régulateurs d'État", "FinCEN")
add(J, R4, "Cellule de renseignement financier", "FinCEN", "FinCEN")
add(J, R4, "Canal", "Suspicious Activity Report (SAR) sur BSA E-Filing", "BSA E-Filing (FinCEN)")
add(J, R4, "Délais et seuils", "30 jours après la détection (60 si le suspect n'est pas identifié) ; seuils de 5 000 USD (banques) et 2 000 USD (MSB)")
add(J, R4, "Confidentialité", "Interdiction de révéler un SAR ; protection (safe harbor) du déclarant de bonne foi")
add(J, R5, "Currency Transaction Report", "Opérations en espèces de plus de 10 000 USD par jour")
add(J, R5, "Travel rule", "Transferts de fonds à partir de 3 000 USD")
add(J, R5, "Transport d'espèces (CMIR)", "Plus de 10 000 USD à l'entrée ou à la sortie du territoire")
add(J, R6, "Bénéficiaire effectif", "CDD Rule : 25 % ou plus, plus une personne exerçant le contrôle ; CTA : déclaration limitée aux sociétés étrangères depuis mars 2025")
add(J, R6, "KYC", "Customer Identification Program (CIP) et vigilance continue")
add(J, R7, "OFAC", "Liste SDN, blocage, déclaration sous 10 jours ouvrables", "OFAC — recherche SDN")
add(J, R8, "GAFI", "Rapport d'évaluation mutuelle attendu en décembre 2026", "GAFI")

# =============================================================================== CANADA
J = "Canada"
add(J, R1, "LRPCFAT / PCMLTFA et règlements", "Modifiés par les lois C-12 et C-15 (sanction royale le 26 mars 2026)", "LRPCFAT (Justice Canada)")
add(J, R2, "Entités déclarantes", "Entités financières, assureurs-vie, courtiers en valeurs mobilières, entreprises de services monétaires, casinos, négociants en métaux et pierres précieuses, courtiers et promoteurs immobiliers, comptables, notaires de la C.-B.")
add(J, R3, "CANAFE / FINTRAC", "Cellule de renseignement financier et superviseur LCB-FT ; BSIF pour le prudentiel", "CANAFE / FINTRAC")
add(J, R4, "Cellule de renseignement financier", "CANAFE / FINTRAC", "CANAFE / FINTRAC")
add(J, R4, "Quoi et quand", "Déclaration d'opération douteuse dès que possible, sans seuil, y compris les tentatives")
add(J, R4, "Confidentialité", "Interdiction de révéler la déclaration (LRPCFAT art. 8)")
add(J, R5, "Déclarations de seuil", "Espèces, télévirements internationaux et actifs virtuels de 10 000 CAD ou plus (règle des 24 heures)")
add(J, R5, "Règle de déplacement", "Télévirements et transferts d'actifs virtuels à partir de 1 000 CAD")
add(J, R6, "Bénéficiaire effectif", "25 % ou plus ; signalement des divergences (C-15)")
add(J, R7, "Sanctions", "Code criminel (art. 83.08 et s.), Loi sur les mesures économiques spéciales, Loi Sergueï Magnitski")
add(J, R8, "GAFI et Groupe Egmont", "Membre du GAFI", "GAFI")

# =============================================================================== MEXIQUE
J = "Mexique"
add(J, R1, "LFPIORPI réformée et Reglas generales", "Règles générales du 7 août 2026, en vigueur le 30 novembre 2026", "UIF Mexique", CONF)
add(J, R1, "Art. 115 de la Ley de Instituciones de Crédito", "Disposiciones de carácter general (DCG) de la CNBV", "", CONF)
add(J, R2, "Entités financières", "Banques, SOFOM, casas de cambio, institutions de technologie financière (ITF)")
add(J, R2, "Actividades vulnerables", "Immobilier, bijouterie, véhicules, jeux, notaires, dons, actifs virtuels…", "Portail PLD du SAT")
add(J, R3, "Superviseurs", "CNBV, CNSF, CONSAR ; SAT pour les actividades vulnerables")
add(J, R4, "Cellule de renseignement financier", "UIF (Unidad de Inteligencia Financiera)", "UIF Mexique")
add(J, R4, "Canal", "Reportes d'opérations inhabituelles et préoccupantes (entités financières) ; avisos sur le portail du SAT (actividades vulnerables)", "Portail PLD du SAT", CONF)
add(J, R5, "Espèces", "Restrictions d'usage des espèces pour les actividades vulnerables (art. 32 LFPIORPI) ; seuils à confirmer", "", CONF)
add(J, R6, "Bénéficiaire contrôlant", "25 % (réforme 2025), exigible au 1er mars 2027 pour les actividades vulnerables", "", CONF)
add(J, R7, "Liste des personnes bloquées", "Tenue par l'UIF", "UIF Mexique")
add(J, R8, "GAFI et GAFILAT", "Rapport d'évaluation mutuelle du GAFI attendu en décembre 2026", "GAFILAT")

# =============================================================================== RÉPUBLIQUE DOMINICAINE
J = "République dominicaine"
add(J, R1, "Ley 155-17 et décrets 407-17 et 408-17", "Loi LBC/FT et règlements d'application", "UAF République dominicaine", CONF)
add(J, R2, "Sujetos obligados", "Entités financières ; sujetos obligados no financieros (casinos, loteries, immobilier, notaires, avocats, comptables, joailliers, concessionnaires)")
add(J, R3, "Superviseurs", "SB, SIMV, SIPEN, Superintendencia de Seguros, DGII (non financiers)", "Superintendencia de Bancos (RD)")
add(J, R4, "Cellule de renseignement financier", "UAF (Unidad de Análisis Financiero)", "UAF République dominicaine")
add(J, R4, "Canal et délai", "Reporte de operación sospechosa (ROS) — délai légal à confirmer", "", CONF)
add(J, R5, "Transactions en espèces", "Reporte de transacciones en efectivo (RTE) — seuil à confirmer", "", CONF)
add(J, R6, "Bénéficiaire final", "Seuil à confirmer dans la Ley 155-17", "", CONF)
add(J, R7, "Sanctions financières ciblées", "Décret 407-17", "", CONF)
add(J, R8, "GAFILAT et Groupe Egmont", "Protocole d'accord UAF – UCREF (2023)", "GAFILAT")

fiches = pd.DataFrame(rows)
fiches.insert(2, "ordre", fiches.groupby(["juridiction", "rubrique"]).cumcount() + 1)
(ROOT / "data/referentiels").mkdir(parents=True, exist_ok=True)
fiches.to_csv(ROOT / "data/referentiels/fiches_juridictions.csv", index=False, encoding="utf-8-sig")

# =============================================================================== CIRCUITS
C = {
    "France / UE": [("Détection", "Équipes / outils", "Alerte d'un outil de surveillance ou remontée d'un collaborateur"),
                    ("Analyse", "Conformité", "Examen renforcé : profil client, cohérence, origine des fonds"),
                    ("Décision", "Déclarant Tracfin", "Décision motivée et documentée"),
                    ("Déclaration", "Tracfin (ERMES)", "Avant l'exécution de l'opération, en principe"),
                    ("Opposition éventuelle", "Tracfin", "Report de l'opération pendant 10 jours ouvrables"),
                    ("Suites", "Tracfin / procureur", "Analyse, transmission éventuelle à l'autorité judiciaire ; confidentialité maintenue")],
    "Haïti": [("Détection", "Équipes / outils", "Alerte, opération inhabituelle, tentative"),
              ("Analyse", "Conformité", "Examen renforcé (art. 22), recherches complémentaires"),
              ("Décision", "Responsable de la conformité", "Décision documentée"),
              ("Déclaration", "UCREF", "Sans délai, quel que soit le montant (art. 19 à 21)"),
              ("Opposition éventuelle", "UCREF", "Blocage de l'opération pendant 48 heures (art. 24)"),
              ("Suites", "UCREF / parquet / pôle financier", "Transmission éventuelle au parquet ; vigilance renforcée ; confidentialité")],
    "États-Unis": [("Detection", "Équipes / outils", "Alerte de monitoring, 314(a), remontée interne"),
                   ("Investigation", "BSA/AML", "Enquête et documentation"),
                   ("Décision", "BSA Officer / comité", "Décision de déposer ou non"),
                   ("SAR", "FinCEN (BSA E-Filing)", "Sous 30 jours après la détection"),
                   ("Activité continue", "BSA/AML", "Revue à 90 jours, SAR de suivi"),
                   ("Suites", "FinCEN / forces de l'ordre", "Exploitation par les autorités ; confidentialité du SAR")],
    "Canada": [("Détection", "Équipes / outils", "Alerte ou remontée interne"),
               ("Analyse", "Conformité", "Motifs raisonnables de soupçonner"),
               ("Décision", "Agent de conformité", "Décision documentée"),
               ("Déclaration", "CANAFE", "Dès que possible, sans seuil"),
               ("Suites", "CANAFE / forces de l'ordre", "Communication aux autorités ; confidentialité")],
    "Mexique": [("Detección", "Équipes / outils", "Alerte de monitoring"),
                ("Análisis", "Oficial de cumplimiento", "Analyse de l'opération"),
                ("Decisión", "Comité de Comunicación y Control", "Décision collégiale"),
                ("Reporte", "UIF (via CNBV ou SAT)", "Délai fixé par les DCG — à confirmer"),
                ("Suites", "UIF / FGR", "Transmission éventuelle au parquet")],
    "République dominicaine": [("Detección", "Équipes / outils", "Alerte ou remontée interne"),
                               ("Análisis", "Oficial de cumplimiento", "Analyse de l'opération"),
                               ("Reporte", "UAF", "ROS — délai légal à confirmer"),
                               ("Suites", "UAF / Ministerio Público", "Transmission éventuelle au parquet")],
}
crow = [dict(juridiction=j, etape_no=i, etape=e, acteur=a, detail=d) for j, steps in C.items() for i, (e, a, d) in enumerate(steps, 1)]
pd.DataFrame(crow).to_csv(ROOT / "data/referentiels/circuit_declaration.csv", index=False, encoding="utf-8-sig")
print(f"fiches : {len(fiches)} lignes ; circuits : {len(crow)} étapes")
