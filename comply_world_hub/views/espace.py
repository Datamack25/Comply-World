# -*- coding: utf-8 -*-
"""Espace abonné : tableau de bord, parcours, dispositif de contrôle, Haïti, référentiel, pays, veille."""
import html
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from core import ui, auth, parcours as P, exports as X
from core.config import COLORS as C, ZONES, SERVICES_LABELS, BRAND
from core.data import load, actualites
from core.veille import derniere_maj
from views import haiti_contexte

NIV_COLORS = {"Élevé": C["red"], "Moyennement élevé": "#D0703A", "Moyen": C["amber"], "Moyennement faible à moyen": "#A99A3A",
              "Moyennement faible": C["green"], "Faible": C["green"]}
PRIO_TONE = {"Critique": "red", "Haute": "amber", "Moyenne": "navy"}


def _layout(fig, h=360):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="white", plot_bgcolor="white",
                      font=dict(family="Inter, sans-serif", color=C["ink"], size=12), legend=dict(orientation="h", y=-0.15))
    fig.update_xaxes(gridcolor=C["line"]); fig.update_yaxes(gridcolor=C["line"])
    return fig


def page(user):
    ui.page_head("Espace abonné", f"Bonjour {user.get('name') or user['login']}",
                 f"{user.get('org') or BRAND} · offre {user.get('plan', '')}")
    c1, c2, _ = st.columns([1.3, 1.5, 4])
    c1.button("← Retour à l'accueil", on_click=ui.go, args=("accueil",), key="esp_home")
    if user.get("role") == "admin":
        c2.button("⚙️ Administration", on_click=ui.go, args=("admin",), key="esp_admin")

    tabs = st.tabs(["Tableau de bord", "Parcours de conformité", "Dispositif de contrôle", "Haïti — ENR 2025",
                    "Dispositif légal", "Référentiel réglementaire", "Pays et corridors", "Actualités réglementaires"])
    with tabs[0]:
        dashboard(user)
    with tabs[1]:
        if ui.require(user, "parcours"):
            parcours_tab(user)
    with tabs[2]:
        if ui.require(user, "controles"):
            controles_tab(user)
    with tabs[3]:
        if ui.require(user, "haiti"):
            haiti_tab(user)
    with tabs[4]:
        if ui.require(user, "referentiel"):
            dispositif_legal_tab(user)
    with tabs[5]:
        if ui.require(user, "referentiel"):
            referentiel_tab()
    with tabs[6]:
        if ui.require(user, "pays"):
            pays_tab()
    with tabs[7]:
        if ui.require(user, "veille"):
            veille_tab()


# ============================================================================ TABLEAU DE BORD
def dashboard(user):
    pays = load("referentiels/pays_a_risque.csv")
    ech = load("referentiels/echeancier.csv").copy()
    ech["date"] = pd.to_datetime(ech["date"])
    futur = ech[ech.date >= pd.Timestamp(date.today())].sort_values("date")
    k = st.columns(4)
    with k[0]:
        ui.kpi(int(pays.statut_gafi.str.startswith("Liste grise").sum()), "Juridictions sous surveillance GAFI")
    with k[1]:
        ui.kpi(int((pays.liste_ue_haut_risque == "Oui").sum()), "Pays tiers à haut risque (UE)")
    with k[2]:
        ui.kpi(futur.date.iloc[0].strftime("%d/%m/%Y") if len(futur) else "—", "Prochaine échéance")
    with k[3]:
        ui.kpi(derniere_maj().split(" à ")[0] if derniere_maj() != "jamais" else "Initiale", "Dernière mise à jour des actualités")
    st.write("")
    a, b = st.columns([1.1, 1])
    with a:
        st.markdown("#### Échéancier réglementaire")
        f = futur.copy(); f["date"] = f.date.dt.strftime("%d/%m/%Y")
        st.dataframe(f, hide_index=True, width="stretch")
    with b:
        st.markdown("#### Dernières actualités")
        for _, r in actualites(5).iterrows():
            st.markdown(f"**{r['date']:%d/%m/%Y} · {r['juridiction']}** — {r['titre']}")
    st.markdown("#### Vos services")
    st.markdown(" ".join(ui.badge(SERVICES_LABELS[s], "green" if auth.can(user, s) else "navy") for s in SERVICES_LABELS),
                unsafe_allow_html=True)


# ============================================================================ PARCOURS
def _selection(prefix: str):
    zone = st.radio("Zone", list(ZONES), horizontal=True, key=f"{prefix}_zone")
    a, b = st.columns(2)
    jur = a.selectbox("Juridiction", ZONES[zone], key=f"{prefix}_jur")
    ent = b.selectbox("Type d'entité assujettie", P.entites(jur), key=f"{prefix}_ent")
    return jur, ent


def parcours_tab(user):
    st.markdown("#### Générer un parcours de mise en conformité")
    st.caption("Le parcours combine les obligations communes de la juridiction, les exigences propres au type d'entité et celles liées à votre profil d'activité.")
    jur, ent = _selection("pc")
    a, b, c = st.columns(3)
    nom = a.text_input("Nom de l'entité accompagnée", value=user.get("org", ""), key="pc_nom")
    taille = b.selectbox("Taille", ["Petite", "Moyenne", "Grande"], index=1, key="pc_taille")
    risque = c.selectbox("Exposition au risque", ["Standard", "Élevé"], key="pc_risque")
    a, b = st.columns([2, 1])
    opts = a.multiselect("Profil d'activité", list(P.OPTIONS), format_func=lambda k: P.OPTIONS[k], key="pc_opts", placeholder="Sélectionner une ou plusieurs caractéristiques")
    debut = b.date_input("Date de démarrage", value=date.today(), format="DD/MM/YYYY", key="pc_debut")
    if st.button("Générer le parcours", type="primary", key="pc_go"):
        st.session_state.parcours = dict(df=P.generer_parcours(jur, ent, taille, risque, opts, debut),
                                         ctrl=P.generer_controles(jur, risque, taille, opts),
                                         ctx=P.contexte(jur, ent), meta=dict(jur=jur, ent=ent, nom=nom, taille=taille, risque=risque,
                                                                            opts=opts, debut=debut))
    res = st.session_state.get("parcours")
    if not res:
        return
    df, ctx, m = res["df"], res["ctx"], res["meta"]
    if (m["jur"], m["ent"]) != (jur, ent):
        st.info("Les paramètres ont changé : cliquez sur « Générer le parcours » pour actualiser.")

    st.divider()
    st.markdown(f"### {html.escape(m['nom']) + ' — ' if m['nom'] else ''}{html.escape(m['ent'])} ({html.escape(m['jur'])})", unsafe_allow_html=True)
    info = [f"**Cellule de renseignement financier :** {ctx['crf']}", f"**Cadre :** {ctx['cadre']}",
            f"**Bénéficiaire effectif :** {ctx['be']}", f"**Conservation :** {ctx['conservation']}"]
    if ctx.get("superviseur"):
        info += [f"**Autorité de contrôle :** {ctx['superviseur']} ({ctx['base_legale']})", f"**Seuil déclencheur :** {ctx['seuil']}",
                 f"**ENR 2025 :** vulnérabilité {ctx['vulnerabilite'] if pd.notna(ctx['vulnerabilite']) else 'non notée'} — {ctx['niveau_enr']}. {ctx['attention']}"]
    st.info("  \n".join(info))
    if df.fiabilite_reference.astype(str).str.contains("confirmer").any():
        st.warning("Certaines références de cette juridiction sont marquées « à confirmer » : vérifiez-les dans le texte officiel avant diffusion.")

    k = st.columns(4)
    with k[0]: ui.kpi(len(df), "Étapes")
    with k[1]: ui.kpi(int((df.priorite == "Critique").sum()), "Étapes critiques")
    with k[2]: ui.kpi(df.phase.nunique(), "Phases")
    with k[3]: ui.kpi(f"{int(df.delai_jours.max())} j", "Horizon du parcours")

    g = df.copy()
    g["debut"] = pd.Timestamp(m["debut"]); g["fin"] = pd.to_datetime(g["echeance"])
    g["libelle"] = g["n"].astype(str) + ". " + g["etape"].str.slice(0, 55)
    fig = px.timeline(g, x_start="debut", x_end="fin", y="libelle", color="phase",
                      color_discrete_sequence=[C["navy"], C["copper"], "#4F6D9A", "#8E5A2E", "#2E7D5B", "#7A8399"],
                      hover_data=dict(priorite=True, responsable=True, debut=False, libelle=False))
    fig.update_yaxes(autorange="reversed", title=None); fig.update_xaxes(title=None)
    st.plotly_chart(_layout(fig, max(380, 22 * len(g))), width="stretch")

    for ph, sub in df.groupby(["phase_no", "phase"], sort=True):
        with st.expander(f"Phase {ph[0]} — {ph[1]} ({len(sub)} étapes)", expanded=ph[0] == 1):
            for _, r in sub.iterrows():
                st.markdown(f"""{ui.badge(r.priorite, PRIO_TONE.get(r.priorite, 'navy'))}{ui.badge(r.nature, 'navy')}
**{r.n}. {html.escape(r.etape)}** — échéance {r.echeance:%d/%m/%Y} · {html.escape(r.responsable)}  \n{html.escape(r.description)}  \n
*Livrable :* {html.escape(r.livrable)} · *Référence :* {html.escape(str(r.reference))}""", unsafe_allow_html=True)

    _exports_parcours(user, res)


def _export_tables(res):
    df, ctrl = res["df"], res["ctrl"]
    pt = df[["n", "phase", "etape", "description", "livrable", "reference", "responsable", "priorite", "echeance"]].copy()
    pt["echeance"] = pd.to_datetime(pt["echeance"]).dt.strftime("%d/%m/%Y")
    pt.columns = ["N°", "Phase", "Étape", "Description", "Livrable", "Référence", "Responsable", "Priorité", "Échéance"]
    ct = ctrl[["ref", "domaine", "controle", "niveau", "frequence", "methode", "preuve", "indicateur", "reference"]].copy()
    ct.columns = ["Réf.", "Domaine", "Contrôle", "Niveau", "Fréquence", "Méthode", "Preuve", "Indicateur", "Référence"]
    return pt, ct


def _exports_parcours(user, res):
    st.markdown("#### Exporter le dossier de mise en conformité")
    if not auth.can(user, "exports"):
        st.caption("Les exports PDF, Word et Excel sont inclus dans l'offre Intégrale.")
        return
    m, ctx = res["meta"], res["ctx"]
    pt, ct = _export_tables(res)
    meta = {"Entité": m["nom"] or "—", "Type d'entité": m["ent"], "Juridiction": m["jur"], "Taille / exposition": f"{m['taille']} / {m['risque']}",
            "Profil d'activité": ", ".join(P.OPTIONS[o] for o in m["opts"]) or "—", "Démarrage": m["debut"].strftime("%d/%m/%Y"),
            "Cellule de renseignement financier": ctx["crf"], "Cadre de référence": ctx["cadre"]}
    if ctx.get("superviseur"):
        meta["Autorité de contrôle"] = ctx["superviseur"]
        meta["Évaluation nationale des risques"] = f"{ctx['niveau_enr']} — {ctx['attention']}"
    sections = [("Parcours de mise en conformité", pt), ("__pagebreak__", None), ("Dispositif de contrôle permanent", ct)]
    titre = f"Dossier de mise en conformité LCB-FT — {m['nom'] or m['ent']}"
    sous = f"{m['ent']} · {m['jur']} · généré par {BRAND}"
    base = f"parcours_{m['jur']}_{m['ent']}".replace(" ", "_").replace("/", "-")[:60]
    a, b, c, d = st.columns(4)
    a.download_button("📄 PDF", X.to_pdf(titre, sous, meta, sections), f"{base}.pdf", "application/pdf", width="stretch")
    b.download_button("📝 Word", X.to_docx(titre, sous, meta, sections), f"{base}.docx",
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.document", width="stretch")
    c.download_button("📊 Excel", X.to_xlsx({"Parcours": pt, "Dispositif de contrôle": ct, "Contexte": pd.DataFrame(meta.items(), columns=["Élément", "Valeur"])}),
                      f"{base}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", width="stretch")
    d.download_button("🗂️ CSV", X.to_csv(pt), f"{base}.csv", "text/csv", width="stretch")


# ============================================================================ DISPOSITIF DE CONTRÔLE
def controles_tab(user):
    st.markdown("#### Dispositif de contrôle permanent")
    a, b, c = st.columns(3)
    zone = a.selectbox("Zone", list(ZONES), key="ct_zone")
    jur = b.selectbox("Juridiction", ZONES[zone], key="ct_jur")
    risque = c.selectbox("Exposition au risque", ["Standard", "Élevé"], key="ct_risque")
    opts = st.multiselect("Profil d'activité", list(P.OPTIONS), format_func=lambda k: P.OPTIONS[k], key="ct_opts", placeholder="Sélectionner une ou plusieurs caractéristiques")
    df = P.generer_controles(jur, risque, "Moyenne", opts)
    k = st.columns(4)
    with k[0]: ui.kpi(len(df), "Contrôles")
    with k[1]: ui.kpi(int(df.niveau.str.contains("N1").sum()), "Niveau 1")
    with k[2]: ui.kpi(int(df.niveau.str.contains("N2").sum()), "Niveau 2")
    with k[3]: ui.kpi(int((df.niveau == "N3").sum()), "Niveau 3 (audit)")
    dom = st.multiselect("Filtrer par domaine", sorted(df.domaine.unique()), key="ct_dom", placeholder="Tous les domaines")
    view = df[df.domaine.isin(dom)] if dom else df
    st.dataframe(view[["ref", "domaine", "controle", "niveau", "frequence", "methode", "preuve", "indicateur", "reference"]],
                 hide_index=True, width="stretch", height=520)
    if auth.can(user, "exports"):
        x1, x2, x3 = st.columns(3)
        titre, sous = f"Plan de contrôle permanent LCB-FT — {jur}", f"Exposition {risque.lower()} · {BRAND}"
        tbl = view[["ref", "domaine", "controle", "niveau", "frequence", "methode", "preuve", "indicateur", "reference"]]
        x1.download_button("📄 PDF", X.to_pdf(titre, sous, {}, [("Contrôles", tbl)]), "plan_de_controle.pdf", width="stretch")
        x2.download_button("📝 Word", X.to_docx(titre, sous, {}, [("Contrôles", tbl)]), "plan_de_controle.docx", width="stretch")
        x3.download_button("📊 Excel", X.to_xlsx({"Plan de contrôle": tbl}), "plan_de_controle.xlsx", width="stretch")


# ============================================================================ HAÏTI
def haiti_tab(user):
    st.markdown("#### Haïti — Évaluation nationale des risques (décembre 2025) et décret du 30 avril 2023")
    k = st.columns(4)
    with k[0]: ui.kpi("Élevé", "Risque global de BC")
    with k[1]: ui.kpi("Élevée", "Menace globale")
    with k[2]: ui.kpi("Moy. élevée", "Vulnérabilité globale")
    with k[3]: ui.kpi("Liste grise", "Statut GAFI (oct. 2026)")
    st.write("")
    a, b = st.columns(2)
    with a:
        s = load("haiti/haiti_vulnerabilites_sectorielles_enr.csv").sort_values("vulnerabilite")
        fig = px.bar(s, x="vulnerabilite", y="secteur", orientation="h", color="niveau", color_discrete_map=NIV_COLORS,
                     text="vulnerabilite", title="Vulnérabilité sectorielle (0 à 1)")
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", cliponaxis=False)
        fig.update_xaxes(range=[0, 1], title=None); fig.update_yaxes(title=None)
        st.plotly_chart(_layout(fig, 470), width="stretch")
    with b:
        p = load("haiti/haiti_produits_bancaires_enr.csv")
        fig = go.Figure()
        fig.add_bar(y=p.produit, x=p.vulnerabilite_inherente, name="Inhérente", orientation="h", marker_color=C["copper"])
        fig.add_bar(y=p.produit, x=p.vulnerabilite_finale, name="Après contrôles", orientation="h", marker_color=C["navy"])
        fig.update_layout(barmode="group", title="Banque — vulnérabilité des produits")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(_layout(fig, 300), width="stretch")
        mz = load("haiti/haiti_menaces_enr.csv")
        st.markdown("**Menaces (ENR 2025)**")
        st.dataframe(mz, hide_index=True, width="stretch", height=180)
    t0, t1, t2, t5, t6, t7, t3, t4 = st.tabs(["Situation et liste grise", "Entités assujetties", "Seuils et obligations", "Circulaires BRH", "Acteurs institutionnels",
                                           "Sanctions pénales", "Plan d'action national", "Cadre juridique"])
    with t0:
        haiti_contexte.render()
    with t5:
        st.caption("Liste publiée par la BRH. La circulaire 129-1 (6 février 2026) est un PDF scanné : son contenu détaillé reste à intégrer aux parcours.")
        st.dataframe(load("haiti/haiti_circulaires_brh.csv"), hide_index=True, width="stretch", column_config={"lien": st.column_config.LinkColumn("Lien", display_text="Ouvrir")})
    with t6:
        st.dataframe(load("haiti/haiti_acteurs_institutionnels.csv"), hide_index=True, width="stretch", column_config={"lien": st.column_config.LinkColumn("Lien", display_text="Ouvrir")})
    with t7:
        st.dataframe(load("haiti/haiti_sanctions_penales.csv"), hide_index=True, width="stretch")
    with t1:
        st.dataframe(load("haiti/haiti_entites_assujetties.csv"), hide_index=True, width="stretch")
    with t2:
        st.dataframe(load("haiti/haiti_seuils_obligations.csv"), hide_index=True, width="stretch")
    with t3:
        st.dataframe(load("haiti/haiti_actions_prioritaires_enr.csv"), hide_index=True, width="stretch")
    with t4:
        st.dataframe(load("haiti/haiti_cadre_juridique.csv"), hide_index=True, width="stretch",
                     column_config={"lien": st.column_config.LinkColumn("Lien", display_text="Ouvrir")})
    if auth.can(user, "exports"):
        sheets = {"Entités assujetties": load("haiti/haiti_entites_assujetties.csv"), "Seuils": load("haiti/haiti_seuils_obligations.csv"),
                  "Menaces ENR": load("haiti/haiti_menaces_enr.csv"), "Vulnérabilités ENR": load("haiti/haiti_vulnerabilites_sectorielles_enr.csv"),
                  "Produits bancaires ENR": load("haiti/haiti_produits_bancaires_enr.csv"), "Plan d'action ENR": load("haiti/haiti_actions_prioritaires_enr.csv"),
                  "Cadre juridique": load("haiti/haiti_cadre_juridique.csv"), "Circulaires BRH": load("haiti/haiti_circulaires_brh.csv"),
                  "Acteurs": load("haiti/haiti_acteurs_institutionnels.csv"), "Sanctions pénales": load("haiti/haiti_sanctions_penales.csv")}
        st.download_button("📊 Télécharger le référentiel Haïti (Excel)", X.to_xlsx(sheets), "referentiel_haiti_lcbft.xlsx")


# ============================================================================ DISPOSITIF LÉGAL
INTRO_DISPOSITIF = {
    "Haïti": "Le dispositif haïtien repose sur le décret du 30 avril 2023 (prévention, répression et gel des fonds), complété par les circulaires de la BRH "
             "(dont la 129-1 du 6 février 2026), la réorganisation de l'UCREF (novembre 2023), l'évaluation nationale des risques de décembre 2025 "
             "et, depuis mai 2026, des pôles judiciaires spécialisés. Haïti reste sous surveillance renforcée du GAFI (octobre 2026).",
    "France": "Le dispositif français combine les obligations préventives du Code monétaire et financier (L561-1 et s.), les incriminations du Code pénal "
              "(blanchiment, financement du terrorisme, corruption), le gel des avoirs (L562-1 et s.) et un réseau d'autorités : Tracfin, ACPR, AMF, DGCCRF, "
              "PNF, AFA et AGRASC. Il basculera vers le règlement européen AMLR le 10 juillet 2027.",
    "Union européenne": "Le paquet LCB-FT européen (AMLR, AMLD6, règlement AMLA) s'applique pour l'essentiel au 10 juillet 2027 ; l'AMLA, opérationnelle, "
                        "prépare les normes techniques et exercera une supervision directe à partir de 2028. Il s'articule avec les règles pénales "
                        "(directives 2018/1673 et 2024/1226), les mesures restrictives et le Parquet européen.",
}


def dispositif_legal_tab(user):
    a, b = st.tabs(["Fiche juridiction et mise en conformité", "Synthèse criminalité financière (Haïti, France, UE)"])
    with a:
        fiche_juridiction_tab(user)
    with b:
        _synthese_criminalite(user)


def fiche_juridiction_tab(user):
    from core.config import JURIDICTIONS
    st.markdown("#### Fiche juridiction et dispositif de mise en conformité")
    st.caption("Pour une juridiction et un type d'entité : cadre légal avec liens officiels, entités assujetties, autorités de contrôle, "
               "à qui et comment déclarer un soupçon (schéma du circuit), seuils, bénéficiaire effectif et KYC/KYB, gel des avoirs, "
               "puis le parcours de mise en conformité et le plan de contrôle. Téléchargeable en PDF, Word ou Excel.")
    fiches = load("referentiels/fiches_juridictions.csv")
    circuits = load("referentiels/circuit_declaration.csv")
    a, b, c = st.columns([1, 1.4, 1])
    jur = a.selectbox("Juridiction", JURIDICTIONS, key="fj_j")
    ent = b.selectbox("Type d'entité", P.entites(jur), key="fj_e")
    risque = c.selectbox("Exposition au risque", ["Standard", "Élevé"], key="fj_r")
    a, b, c = st.columns([1, 1, 1.4])
    inc_p = a.checkbox("Inclure le parcours", value=True, key="fj_p")
    inc_c = b.checkbox("Inclure le plan de contrôle", value=True, key="fj_c")
    nom = c.text_input("Entité accompagnée (facultatif)", key="fj_n")

    f = fiches[fiches.juridiction == jur].sort_values(["rubrique", "ordre"])
    circ = circuits[circuits.juridiction == jur].sort_values("etape_no")
    steps = list(zip(circ.etape, circ.acteur, circ.detail))
    if f.fiabilite.eq("À confirmer").any():
        st.warning("Certaines informations de cette juridiction sont marquées « À confirmer » : vérifiez-les dans le texte officiel avant diffusion.")

    if jur == "Haïti":
        with st.expander("Situation du pays et raisons du maintien sur la liste grise du GAFI", expanded=False):
            haiti_contexte.render()
    for rub, sub in f.groupby("rubrique", sort=True):
        st.markdown(f"##### {rub}")
        ui.df_table(sub, {"element": "Élément", "detail": "Détail", "lien": "Lien officiel"})
        if rub.startswith("4."):
            st.markdown("**Schéma du circuit de déclaration**")
            ui.flow(steps)

    parcours_df = ctrl_df = None
    if inc_p:
        parcours_df = P.generer_parcours(jur, ent, "Moyenne", risque, [], date.today())
        st.markdown(f"##### 9. Parcours de mise en conformité — {ent}")
        pv = parcours_df.copy(); pv["echeance"] = pd.to_datetime(pv["echeance"]).dt.strftime("%d/%m/%Y")
        ui.df_table(pv, {"n": "N°", "phase": "Phase", "etape": "Étape", "livrable": "Livrable", "reference": "Référence", "priorite": "Priorité", "echeance": "Échéance"})
    if inc_c:
        ctrl_df = P.generer_controles(jur, risque, "Moyenne", [])
        st.markdown("##### 10. Plan de contrôle permanent")
        ui.df_table(ctrl_df, {"ref": "Réf.", "domaine": "Domaine", "controle": "Contrôle", "niveau": "Niveau", "frequence": "Fréquence", "indicateur": "Indicateur"})

    # ---- export
    cols = {"element": "Élément", "detail": "Détail", "lien": "Lien officiel"}
    sections = []
    for rub, sub in f.groupby("rubrique", sort=True):
        sections.append((rub, sub[list(cols)].rename(columns=cols)))
        if rub.startswith("4."):
            sections.append(("Schéma du circuit de déclaration de soupçon", {"flow": steps}))
    if jur == "Haïti":
        sections = haiti_contexte.export_sections() + [("__pagebreak__", None)] + sections
    if parcours_df is not None:
        pt = parcours_df[["n", "phase", "etape", "livrable", "reference", "responsable", "priorite", "echeance"]].copy()
        pt["echeance"] = pd.to_datetime(pt["echeance"]).dt.strftime("%d/%m/%Y")
        pt.columns = ["N°", "Phase", "Étape", "Livrable", "Référence", "Responsable", "Priorité", "Échéance"]
        sections += [("__pagebreak__", None), (f"9. Parcours de mise en conformité — {ent}", pt)]
    if ctrl_df is not None:
        ct = ctrl_df[["ref", "domaine", "controle", "niveau", "frequence", "preuve", "indicateur"]].copy()
        ct.columns = ["Réf.", "Domaine", "Contrôle", "Niveau", "Fréquence", "Preuve", "Indicateur"]
        sections += [("__pagebreak__", None), ("10. Plan de contrôle permanent", ct)]
    titre = f"Dispositif de mise en conformité LCB-FT — {jur}"
    sous = f"{ent}" + (f" · {nom}" if nom else "") + f" · {BRAND}"
    meta = {"Juridiction": jur, "Type d'entité": ent, "Exposition au risque": risque, "Mise à jour des données": "10 novembre 2026"}
    sheets = {"Fiche juridiction": f[["rubrique", "element", "detail", "lien", "fiabilite"]],
              **({"Situation Haïti": load("haiti/haiti_contexte_pays.csv"), "Plan d'action GAFI": load("haiti/haiti_plan_action_gafi.csv")}
                 if jur == "Haïti" else {}),
              "Circuit de déclaration": circ[["etape_no", "etape", "acteur", "detail"]]}
    if parcours_df is not None:
        sheets["Parcours"] = pt
    if ctrl_df is not None:
        sheets["Plan de contrôle"] = ct
    base = f"dispositif_conformite_{jur}_{ent}".replace(" ", "_").replace("/", "-")[:70]
    st.markdown("#### Télécharger la fiche")
    x1, x2, x3 = st.columns(3)
    x1.download_button("📄 PDF", X.to_pdf(titre, sous, meta, sections), f"{base}.pdf", "application/pdf", width="stretch", key="fj_pdf")
    x2.download_button("📝 Word", X.to_docx(titre, sous, meta, sections), f"{base}.docx",
                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document", width="stretch", key="fj_docx")
    x3.download_button("📊 Excel", X.to_xlsx(sheets), f"{base}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       width="stretch", key="fj_xlsx")


def _synthese_criminalite(user):
    st.markdown("#### Dispositif légal de lutte contre la criminalité financière")
    st.caption("Générez une synthèse du cadre légal (prévention, répression pénale, sanctions financières, institutions, corruption, coopération) "
               "pour une ou plusieurs juridictions, puis téléchargez-la en PDF, Word, Excel ou CSV.")
    df = load("referentiels/dispositif_legal_criminalite_financiere.csv")
    a, b = st.columns(2)
    jur = a.multiselect("Juridictions", list(INTRO_DISPOSITIF), default=["Haïti"], key="dl_j", placeholder="Choisir")
    pil = b.multiselect("Piliers", list(dict.fromkeys(df.pilier)), default=list(dict.fromkeys(df.pilier)), key="dl_p", placeholder="Choisir")
    a, b = st.columns(2)
    annexes = a.checkbox("Ajouter les annexes Haïti (entités assujetties, seuils, sanctions, circulaires BRH, acteurs)", value=True, key="dl_ann")
    nom = b.text_input("Destinataire du document (facultatif)", key="dl_nom")
    v = df[df.juridiction.isin(jur) & df.pilier.isin(pil)]
    if not jur or v.empty:
        st.info("Sélectionnez au moins une juridiction et un pilier.")
        return
    k = st.columns(3)
    with k[0]: ui.kpi(len(v), "Textes et acteurs")
    with k[1]: ui.kpi(v.pilier.nunique(), "Piliers")
    with k[2]: ui.kpi(int(v.fiabilite.ne("Texte officiel").sum()), "Éléments à confirmer")
    for j in jur:
        st.markdown(f"##### {j}")
        st.write(INTRO_DISPOSITIF[j])
        for p in pil:
            sub = v[(v.juridiction == j) & (v.pilier == p)]
            if len(sub):
                with st.expander(f"{p} ({len(sub)})"):
                    st.dataframe(sub[["intitule", "reference", "contenu", "seuil_ou_sanction", "fiabilite", "lien"]], hide_index=True, width="stretch",
                                 column_config={"lien": st.column_config.LinkColumn("Lien", display_text="Ouvrir")})

    # ---- construction du document
    cols = {"intitule": "Texte / acteur", "reference": "Référence", "contenu": "Contenu clé", "seuil_ou_sanction": "Seuil / sanction", "fiabilite": "Fiabilité"}
    sections = []
    for i, j in enumerate(jur):
        if i:
            sections.append(("__pagebreak__", None))
        sections.append((f"{j} — vue d'ensemble", INTRO_DISPOSITIF[j]))
        for p in pil:
            sub = v[(v.juridiction == j) & (v.pilier == p)]
            if len(sub):
                sections.append((f"{j} — {p}", sub[list(cols)].rename(columns=cols)))
    sheets = {"Dispositif légal": v.drop(columns=[]).copy()}
    if "Haïti" in jur:
        idx = next((i for i, sct in enumerate(sections) if sct[0].startswith("Haïti — vue")), 0)
        sections[idx + 1:idx + 1] = haiti_contexte.export_sections()
    if annexes and "Haïti" in jur:
        ann = [("Annexe Haïti — entités assujetties", load("haiti/haiti_entites_assujetties.csv")[["type_entite", "famille", "base_legale", "autorite_controle", "seuil_declencheur"]]),
               ("Annexe Haïti — seuils et obligations", load("haiti/haiti_seuils_obligations.csv")),
               ("Annexe Haïti — sanctions pénales", load("haiti/haiti_sanctions_penales.csv")),
               ("Annexe Haïti — circulaires BRH", load("haiti/haiti_circulaires_brh.csv")[["numero", "date", "destinataires", "objet", "statut"]]),
               ("Annexe Haïti — acteurs institutionnels", load("haiti/haiti_acteurs_institutionnels.csv")[["sigle", "nom", "role", "missions"]])]
        sections.append(("__pagebreak__", None))
        sections += ann
        sheets.update({t.replace("Annexe Haïti — ", "HT ")[:31]: d for t, d in ann})
    sources = load("referentiels/liens_officiels.csv")
    sources = sources[sources.juridiction.isin([{"Union européenne": "UE"}.get(j, j) for j in jur] + ["International"])]
    sections.append(("Sources officielles", sources[["juridiction", "organisme", "url"]]))
    titre = "Dispositif légal de lutte contre la criminalité financière"
    sous = " · ".join(jur) + (f" — préparé pour {nom}" if nom else "") + f" · {BRAND}"
    meta = {"Juridictions": ", ".join(jur), "Piliers": ", ".join(pil), "Mise à jour des données": "10 novembre 2026"}
    base = "dispositif_legal_" + "_".join(j.split()[0].lower() for j in jur)
    st.markdown("#### Télécharger")
    x1, x2, x3, x4 = st.columns(4)
    x1.download_button("📄 PDF", X.to_pdf(titre, sous, meta, sections), f"{base}.pdf", "application/pdf", width="stretch", key="dl_pdf")
    x2.download_button("📝 Word", X.to_docx(titre, sous, meta, sections), f"{base}.docx",
                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document", width="stretch", key="dl_docx")
    x3.download_button("📊 Excel", X.to_xlsx(sheets), f"{base}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", width="stretch", key="dl_xlsx")
    x4.download_button("🗂️ CSV", X.to_csv(v), f"{base}.csv", "text/csv", width="stretch", key="dl_csv")


# ============================================================================ RÉFÉRENTIEL
def referentiel_tab():
    t1, t2, t3, t4, t5 = st.tabs(["Europe", "Haïti", "Amériques", "Références par thème", "Liens officiels"])
    link = {"lien": st.column_config.LinkColumn("Lien", display_text="Ouvrir"), "url": st.column_config.LinkColumn("Lien", display_text="Ouvrir")}
    with t1:
        st.dataframe(load("europe/europe_cadre_reglementaire.csv"), hide_index=True, width="stretch", column_config=link)
    with t2:
        st.dataframe(load("haiti/haiti_cadre_juridique.csv"), hide_index=True, width="stretch", column_config=link)
    with t3:
        st.dataframe(load("ameriques/ameriques_juridictions.csv"), hide_index=True, width="stretch", column_config=link)
    with t4:
        r = load("referentiels/references_par_theme.csv")
        theme = st.selectbox("Thème", sorted(r.theme.unique()), key="ref_theme")
        st.dataframe(r[r.theme == theme][["juridiction", "reference", "fiabilite"]], hide_index=True, width="stretch")
    with t5:
        st.dataframe(load("referentiels/liens_officiels.csv"), hide_index=True, width="stretch", column_config=link)


# ============================================================================ PAYS
def pays_tab():
    df = load("referentiels/pays_a_risque.csv")
    st.caption("GAFI : décisions du 30 octobre 2026 · UE : règlement délégué (UE) 2016/1675 dans sa version du 29 janvier 2026.")
    st.markdown("#### Analyse d'un corridor")
    corridors = sorted(set(df.pays) | {"France", "Haïti", "États-Unis", "Canada", "République dominicaine", "Chili", "Brésil", "Mexique"})
    a, b = st.columns(2)
    o = a.selectbox("Pays d'origine des fonds", corridors, index=corridors.index("France"), key="cor_o")
    d = b.selectbox("Pays de destination", corridors, index=corridors.index("Haïti"), key="cor_d")
    for p in (o, d):
        r = df[df.pays == p]
        g = r.statut_gafi.iloc[0] if len(r) else "Non listé"
        u = r.liste_ue_haut_risque.iloc[0] if len(r) else "Non"
        tone = "red" if g.startswith("Liste noire") else ("amber" if g.startswith("Liste grise") or u == "Oui" else "green")
        st.markdown(f"**{p}** : {ui.badge('GAFI — ' + g, tone)} {ui.badge('Liste UE : ' + u, 'amber' if u == 'Oui' else 'green')}",
                    unsafe_allow_html=True)
    risk = [p for p in (o, d) if len(df[df.pays == p]) and (df[df.pays == p].statut_gafi.iloc[0] != "Non listé" or df[df.pays == p].liste_ue_haut_risque.iloc[0] == "Oui")]
    if risk:
        st.warning("Corridor exposé : appliquer les mesures de vigilance renforcée (origine des fonds, objet des opérations, "
                   "approbation hiérarchique, surveillance renforcée des flux) et documenter l'analyse.")
    else:
        st.success("Aucun des deux pays n'est listé par le GAFI ni par l'UE : vigilance standard selon votre classification des risques.")
    st.markdown("#### Liste consolidée")
    f = st.radio("Afficher", ["Tous", "Liste noire GAFI", "Liste grise GAFI", "Liste UE"], horizontal=True, key="pays_f")
    v = df
    if f == "Liste noire GAFI":
        v = df[df.statut_gafi.str.startswith("Liste noire")]
    elif f == "Liste grise GAFI":
        v = df[df.statut_gafi.str.startswith("Liste grise")]
    elif f == "Liste UE":
        v = df[df.liste_ue_haut_risque == "Oui"]
    st.dataframe(v, hide_index=True, width="stretch")


# ============================================================================ VEILLE
def veille_tab():
    df = actualites()
    st.caption(f"Dernière mise à jour : {derniere_maj()}")
    a, b, c = st.columns([1, 1, 2])
    j = a.multiselect("Juridiction", sorted(df.juridiction.dropna().unique()), key="v_j", placeholder="Toutes")
    t = b.multiselect("Thème", sorted(df.theme.dropna().unique()), key="v_t", placeholder="Tous")
    q = c.text_input("Recherche", key="v_q")
    v = df
    if j: v = v[v.juridiction.isin(j)]
    if t: v = v[v.theme.isin(t)]
    if q: v = v[v.titre.str.contains(q, case=False, na=False) | v.resume.str.contains(q, case=False, na=False)]
    st.write(f"{len(v)} actualité(s)")
    for _, r in v.head(60).iterrows():
        lien = str(r.get("lien") or "")
        st.markdown(f"""<div class="cw-news"><div class="meta">{r['date']:%d/%m/%Y} · {html.escape(str(r['juridiction']))} · {html.escape(str(r['theme']))} · {html.escape(str(r['source']))}</div>
        <div class="t">{html.escape(str(r['titre']))}</div><div class="r">{html.escape(str(r['resume']))}
        {f' · <a href="{html.escape(lien)}" target="_blank">Lire</a>' if lien.startswith('http') else ''}</div></div>""", unsafe_allow_html=True)
    out = v.copy(); out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    st.download_button("🗂️ Exporter la sélection (CSV)", X.to_csv(out), "actualites_reglementaires.csv", "text/csv")
