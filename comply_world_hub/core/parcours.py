# -*- coding: utf-8 -*-
"""Moteur de génération des parcours de mise en conformité et des dispositifs de contrôle."""
from datetime import date, timedelta

import pandas as pd

from .data import load, ref

OPTIONS = {
    "transfrontalier": "Opérations transfrontalières / corridors",
    "ppe": "Clientèle PPE ou à forte notoriété",
    "crypto": "Exposition aux actifs virtuels",
    "especes": "Volume significatif d'espèces",
    "agents": "Recours à des agents, distributeurs ou tiers introducteurs",
}

# Références spécifiques aux options, par juridiction
_OPT_REFS = {
    "transfrontalier": {
        "France / UE": "TFR (UE) 2023/1113 ; CMF L561-10 ; liste UE des pays tiers à haut risque",
        "Haïti": "Décret 2023 art. 47 à 54 (virements électroniques) ; ENR 2025 §3.2.1 et §3.2.3",
        "États-Unis": "31 CFR 1010.410 (travel rule ≥ 3 000 USD) ; OFAC",
        "Canada": "Règle de déplacement ; DTE ≥ 10 000 CAD",
        "Mexique": "DCG CNBV — transferencias internacionales (à confirmer)",
        "République dominicaine": "Normes SB — transferencias (à confirmer)",
    },
    "crypto": {
        "France / UE": "MiCA (UE) 2023/1114 ; TFR (UE) 2023/1113 ; orientations AMLA",
        "Haïti": "Décret 2023 art. 6 (PSAV, seuil 150 000 HTG) ; Recommandation 15 GAFI",
        "États-Unis": "FinCEN Guidance FIN-2019-G001 (CVC) ; 31 CFR 1010.410",
        "Canada": "LRPCFAT — actifs virtuels (DOMV ≥ 10 000 CAD, règle de déplacement)",
        "Mexique": "Ley Fintech — activos virtuales (à confirmer)",
        "République dominicaine": "Recommandation 15 GAFI (régime national à confirmer)",
    },
    "especes": {
        "France / UE": "CMF L112-6 (plafond 1 000 € résidents) ; AMLR art. 80 (plafond UE de 10 000 € au 10/07/2027)",
        "Haïti": "Décret 2023 art. 16-18 (DTE) et art. 73 (interdiction > 400 000 HTG)",
        "États-Unis": "31 CFR 1010.311 (CTR) ; 31 U.S.C. 5324 (structuring)",
        "Canada": "DOIE ≥ 10 000 CAD ; règle des 24 heures",
        "Mexique": "LFPIORPI art. 32 — restrictions d'usage des espèces (à confirmer)",
        "République dominicaine": "RTE — Ley 155-17 (à confirmer)",
    },
    "agents": {
        "France / UE": "CMF L561-7 (tiers introducteurs) ; L523-1 (agents de PSP)",
        "Haïti": "Décret 2023 art. 68 à 70 (recours à des tiers)",
        "États-Unis": "31 CFR 1022.210(d) — MSB principals & agents",
        "Canada": "Règlement — mandataires et agents",
        "Mexique": "DCG CNBV — comisionistas (à confirmer)",
        "République dominicaine": "Normes SB — subagentes (à confirmer)",
    },
}


def _extra_steps(j: str, opts: list[str]) -> list[dict]:
    out = []

    def add(ph, phase, etape, desc, liv, reference, d, resp, prio):
        out.append(dict(juridiction=j, phase_no=ph, phase=phase, etape=etape, description=desc, livrable=liv,
                        reference=reference, delai_jours=d, responsable=resp, priorite=prio, nature="Liée au profil d'activité"))

    if "transfrontalier" in opts:
        add(2, "Évaluation des risques", "Cartographier les corridors de flux",
            "Volumes par pays d'origine et de destination, statut GAFI/UE des pays, banques correspondantes.",
            "Cartographie des corridors", _OPT_REFS["transfrontalier"][j], 45, "Conformité", "Haute")
        add(5, "Surveillance et déclarations", "Contrôler la complétude des informations des transferts",
            "Données donneur d'ordre / bénéficiaire ; rejet ou suspension des transferts incomplets.",
            "Contrôle automatisé", _OPT_REFS["transfrontalier"][j], 60, "Opérations / Conformité", "Haute")
    if "ppe" in opts:
        add(4, "Vigilance clientèle", "Renforcer le dispositif PPE",
            "Listes PPE nationales et étrangères, membres de la famille et proches, revue annuelle, origine du patrimoine.",
            "Registre PPE + revue annuelle", ref(j, "ppe"), 45, "Conformité", "Critique")
    if "crypto" in opts:
        add(5, "Surveillance et déclarations", "Encadrer l'exposition aux actifs virtuels",
            "Règle de voyage, analyse on-chain, contreparties PSAV agréées, adresses auto-hébergées.",
            "Procédure actifs virtuels", _OPT_REFS["crypto"][j], 60, "Conformité", "Critique")
    if "especes" in opts:
        add(5, "Surveillance et déclarations", "Renforcer la surveillance des espèces",
            "Détection du fractionnement, plafonds légaux de paiement en espèces, origine des fonds des dépôts importants.",
            "Scénarios espèces", _OPT_REFS["especes"][j], 45, "Conformité", "Critique")
    if "agents" in opts:
        add(3, "Corpus procédural", "Encadrer les agents et tiers introducteurs",
            "Sélection, convention, formation, contrôle sur place, remontée des informations KYC.",
            "Programme de contrôle des tiers", _OPT_REFS["agents"][j], 75, "Conformité", "Haute")
    return out


def entites(juridiction: str) -> list[str]:
    df = load("parcours/entites_par_juridiction.csv")
    return df[df.juridiction == juridiction].type_entite.tolist()


def generer_parcours(juridiction: str, entite: str, taille: str = "Moyenne", risque: str = "Standard",
                     options: list[str] | None = None, debut: date | None = None) -> pd.DataFrame:
    options = options or []
    debut = debut or date.today()
    df = load("parcours/parcours_etapes.csv")
    df = df[(df.juridiction == juridiction) & (df.type_entite == entite)].copy()
    extra = pd.DataFrame(_extra_steps(juridiction, options))
    if not extra.empty:
        extra["type_entite"] = entite
        extra["fiabilite_reference"] = df.fiabilite_reference.iloc[0] if len(df) else ""
        df = pd.concat([df, extra], ignore_index=True)

    # Ajustement des délais : taille (capacité) et niveau de risque (urgence)
    k_taille = {"Petite": 0.85, "Moyenne": 1.0, "Grande": 1.25}.get(taille, 1.0)
    df["delai_jours"] = (df["delai_jours"] * k_taille).round().astype(int)
    if risque == "Élevé":
        crit = df.priorite.isin(["Critique", "Haute"])
        df.loc[crit, "delai_jours"] = (df.loc[crit, "delai_jours"] * 0.75).round().astype(int)
        df.loc[df.priorite == "Haute", "priorite"] = "Critique"

    df["echeance"] = [debut + timedelta(days=int(d)) for d in df["delai_jours"]]
    prio_order = {"Critique": 0, "Haute": 1, "Moyenne": 2}
    df["_p"] = df.priorite.map(prio_order).fillna(3)
    df = df.sort_values(["phase_no", "_p", "delai_jours"]).drop(columns="_p").reset_index(drop=True)
    df.insert(0, "n", range(1, len(df) + 1))
    return df


def generer_controles(juridiction: str, risque: str = "Standard", taille: str = "Moyenne",
                      options: list[str] | None = None) -> pd.DataFrame:
    options = options or []
    df = load("parcours/dispositif_controles.csv")
    df = df[df.juridiction == juridiction].copy()
    if "agents" not in options:
        df = df[df.domaine != "Tiers et agents"]
    if risque == "Élevé":
        upgrade = {"Annuelle": "Semestrielle", "Semestrielle": "Trimestrielle", "Trimestrielle": "Mensuelle"}
        df["frequence"] = df["frequence"].replace(upgrade)
    if taille == "Petite":
        df["methode"] = df["methode"].str.replace("≥ 5 %", "≥ 10 dossiers", regex=False)
    df = df.reset_index(drop=True)
    df.insert(0, "ref", [f"C{n:02d}" for n in range(1, len(df) + 1)])
    return df


def contexte(juridiction: str, entite: str) -> dict:
    """Informations de contexte affichées au-dessus du parcours."""
    refs = load("referentiels/references_par_theme.csv")
    crf = {"France / UE": "Tracfin", "Haïti": "UCREF", "États-Unis": "FinCEN", "Canada": "CANAFE / FINTRAC",
           "Mexique": "UIF", "République dominicaine": "UAF"}[juridiction]
    ctx = dict(juridiction=juridiction, entite=entite, crf=crf, cadre=ref(juridiction, "cadre"),
               conservation=ref(juridiction, "conservation"), be=ref(juridiction, "be"))
    if juridiction == "Haïti":
        he = load("haiti/haiti_entites_assujetties.csv")
        r = he[he.type_entite == entite]
        if len(r):
            r = r.iloc[0]
            ctx.update(superviseur=r.autorite_controle, vulnerabilite=r.vulnerabilite_enr, niveau_enr=r.niveau_enr,
                       seuil=r.seuil_declencheur, attention=r.points_attention, base_legale=r.base_legale)
    return ctx


def gantt_frame(df: pd.DataFrame, debut: date) -> pd.DataFrame:
    """Une barre par phase : de la date de début à l'échéance la plus tardive."""
    g = df.groupby(["phase_no", "phase"]).agg(fin=("echeance", "max"), n=("etape", "count")).reset_index()
    g["debut"] = debut
    return g
