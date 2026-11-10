# -*- coding: utf-8 -*-
"""Habillage : CSS, en-tête de navigation, pied de page et composants visuels."""
import html

import streamlit as st

from .config import BRAND, COLORS as C, FOOTER_LINE, DISCLAIMER, CONTACT_CITY, CONTACT_EMAIL, CONTACT_PHONE, LINKEDIN_URL

PAGES_PUBLIQUES = [
    ("accueil", "Accueil"), ("cabinet", "Le cabinet"), ("expertises", "Nos expertises"),
    ("juridictions", "Juridictions"), ("actualites", "Actualités"), ("contact", "Contact"),
]

LOGO_SVG = f"""
<svg width="46" height="46" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="32" cy="32" r="29" fill="none" stroke="{C['navy']}" stroke-width="3.2"/>
  <ellipse cx="32" cy="32" rx="12.5" ry="29" fill="none" stroke="{C['navy']}" stroke-width="2.4"/>
  <path d="M5 23h54M5 41h54" stroke="{C['navy']}" stroke-width="2.4"/>
  <path d="M19 33l9 9 18-20" fill="none" stroke="{C['copper']}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def go(page: str):
    st.session_state.page = page
    st.session_state.pop("scroll_top", None)


def inject_css():
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');
:root {{ --navy:{C['navy']}; --navy2:{C['navy2']}; --copper:{C['copper']}; --copper-l:{C['copper_light']};
        --ink:{C['ink']}; --muted:{C['muted']}; --line:{C['line']}; --bg:{C['bg']}; }}
html, body, [data-testid="stAppViewContainer"], .stApp {{ background:#fff; color:var(--ink); font-family:'Inter',system-ui,sans-serif; }}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{ display:none !important; }}
header[data-testid="stHeader"] {{ background:transparent; height:0; }}
.block-container {{ padding-top:0.6rem; padding-bottom:0; max-width:1240px; }}
.stApp {{ color-scheme:light; }}
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
[data-testid="stWidgetLabel"] p, label, .stRadio label p, .stCaption, [data-testid="stCaptionContainer"] {{ color:var(--ink); }}
[data-testid="stCaptionContainer"] p {{ color:var(--muted); }}
h1,h2,h3 {{ font-family:'Cormorant Garamond',Georgia,serif !important; color:var(--navy); letter-spacing:.2px; }}
a {{ color:var(--navy2); }}

/* ---------- barre de navigation */
.st-key-topnav {{ border-bottom:1px solid var(--line); padding:6px 0 4px 0; margin-bottom:0; position:sticky; top:0; background:#fff; z-index:50; }}
.st-key-topnav button[kind="tertiary"] {{ color:var(--navy) !important; font-size:.74rem; letter-spacing:.6px; text-transform:uppercase; font-weight:600; padding:4px 0; min-width:0; }}
.st-key-topnav button p {{ white-space:nowrap !important; overflow:visible !important; text-overflow:clip !important; }}
.st-key-topnav button[kind="tertiary"] {{ cursor:pointer; }}
.st-key-topnav button[kind="tertiary"]:hover p, .st-key-topnav button[kind="tertiary"] strong {{
   text-decoration:underline; text-decoration-color:var(--copper); text-decoration-thickness:2px; text-underline-offset:7px; }}
.st-key-topnav button[kind="tertiary"]:hover {{ color:var(--navy) !important; }}
.st-key-topnav button[kind="primary"] {{ background:var(--navy); border:1px solid var(--navy); border-radius:2px; font-size:.78rem; letter-spacing:.6px; text-transform:uppercase; }}
.st-key-topnav button[kind="primary"]:hover {{ background:var(--copper); border-color:var(--copper); }}
.st-key-topnav button[kind="secondary"] {{ border-radius:2px; font-size:.78rem; }}
.navactive button[kind="tertiary"] {{ color:var(--copper) !important; }}
.cw-brand {{ display:flex; align-items:center; gap:10px; text-decoration:none; }}
.cw-brand .t1 {{ white-space:nowrap; font-family:'Cormorant Garamond',serif; font-weight:700; font-size:1.42rem; color:var(--navy); line-height:1; letter-spacing:.6px; }}
.cw-brand .t2 {{ white-space:nowrap; font-size:.56rem; letter-spacing:2.4px; color:var(--copper); font-weight:600; margin-top:3px; }}
.cw-bar {{ width:70px; height:6px; background:var(--copper); margin-left:8px; }}

/* ---------- hero (fond blanc) */
.cw-hero {{ position:relative; background:linear-gradient(110deg, var(--navy) 0%, var(--navy2) 100%); border-left:5px solid var(--copper); padding:38px 40px 26px 40px; margin-top:26px; overflow:hidden; }}
.cw-hero .kicker {{ font-size:.78rem; letter-spacing:4px; text-transform:uppercase; color:var(--copper-l) !important; font-weight:600; }}
.cw-hero h1 {{ color:#FFFFFF !important; font-size:2.9rem; line-height:1.1; margin:.35rem 0 .9rem 0; }}
.cw-hero h1 em {{ color:var(--copper-l) !important; font-style:normal; }}
.cw-hero p {{ color:#E4E8F0 !important; font-size:1.05rem; line-height:1.7; max-width:640px; }}
.cw-newsbox {{ border:1px solid var(--line); border-top:3px solid var(--navy); padding:18px 20px 6px; margin-top:26px; background:#fff; }}
.cw-newsbox h4 {{ font-family:'Cormorant Garamond',serif; color:var(--navy); font-size:1.45rem; margin:0 0 .3rem 0; }}
.cw-newsbox .it {{ border-bottom:1px solid var(--line); padding:9px 0; }}
.cw-newsbox .it:last-child {{ border-bottom:none; }}
.cw-newsbox .d {{ color:var(--copper); font-size:.7rem; letter-spacing:1.4px; text-transform:uppercase; font-weight:600; }}
.cw-newsbox .t {{ color:var(--navy); font-size:.9rem; font-weight:600; line-height:1.35; }}
.cw-newsbox .t a {{ color:var(--navy); text-decoration:none; }} .cw-newsbox .t a:hover {{ text-decoration:underline; }}

/* ---------- sections */
.cw-section {{ padding:58px 0 18px 0; }}
.cw-eyebrow {{ color:var(--copper); font-size:.76rem; letter-spacing:3.5px; text-transform:uppercase; font-weight:600; }}
.cw-title {{ font-family:'Cormorant Garamond',serif; font-size:2.35rem; color:var(--navy); margin:.2rem 0 .4rem 0; font-weight:600; }}
.cw-rule {{ width:64px; height:4px; background:var(--copper); margin:.3rem 0 1.2rem 0; }}
.cw-lead {{ color:var(--muted); font-size:1.02rem; max-width:780px; line-height:1.65; }}
.cw-card {{ border:1px solid var(--line); border-top:3px solid var(--navy); padding:22px 22px 18px; height:100%; background:#fff; transition:all .2s; }}
.cw-card:hover {{ border-top-color:var(--copper); box-shadow:0 10px 26px rgba(15,30,61,.08); transform:translateY(-2px); }}
.cw-card .ico {{ font-size:1.5rem; color:var(--copper); }}
.cw-card h4 {{ font-family:'Cormorant Garamond',serif; font-size:1.32rem; color:var(--navy); margin:.4rem 0 .45rem 0; }}
.cw-card p {{ color:var(--muted); font-size:.9rem; line-height:1.55; margin:0; }}
.cw-card .more {{ color:var(--copper); font-size:.78rem; letter-spacing:1px; text-transform:uppercase; font-weight:600; margin-top:.8rem; display:block; }}
.cw-quote {{ background:var(--bg); border-left:5px solid var(--copper); padding:34px 44px; margin:40px 0 10px; font-family:'Cormorant Garamond',serif; font-size:1.65rem; color:var(--navy); font-style:italic; }}
.cw-quote small {{ display:block; font-family:'Inter',sans-serif; font-style:normal; font-size:.8rem; color:var(--muted); margin-top:.6rem; letter-spacing:1px; }}
.cw-step {{ text-align:left; padding:6px 4px; }}
.cw-step .num {{ font-family:'Cormorant Garamond',serif; font-size:2.6rem; color:var(--copper); line-height:1; }}
.cw-step h5 {{ color:var(--navy); margin:.2rem 0; font-weight:700; font-size:1rem; }}
.cw-step p {{ color:var(--muted); font-size:.88rem; }}
.cw-jur {{ background:#fff; border:1px solid var(--line); border-top:3px solid var(--copper); padding:24px 22px; height:100%; }}
.cw-jur h4 {{ color:var(--navy); font-family:'Cormorant Garamond',serif; font-size:1.5rem; margin:0 0 .3rem 0; }}
.cw-jur .tag {{ color:var(--copper); font-size:.72rem; letter-spacing:2.5px; text-transform:uppercase; font-weight:600; }}
.cw-jur ul {{ padding-left:1.1rem; margin:.6rem 0 0 0; }} .cw-jur li {{ color:var(--ink); font-size:.88rem; margin-bottom:.3rem; }}
.cw-news {{ border-bottom:1px solid var(--line); padding:14px 0; }}
.cw-news .meta {{ color:var(--copper); font-size:.74rem; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; }}
.cw-news .t {{ color:var(--navy); font-weight:600; font-size:1rem; margin:.15rem 0; }}
.cw-news .r {{ color:var(--muted); font-size:.88rem; }}
.cw-kpi {{ border:1px solid var(--line); padding:14px 16px; background:#fff; }}
.cw-kpi .v {{ font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--navy); line-height:1.1; font-weight:700; }}
.cw-kpi .l {{ color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:1px; }}
.cw-band {{ background:linear-gradient(110deg, var(--navy), var(--navy2)); border-left:5px solid var(--copper); padding:26px 30px; margin:40px 0 12px; }}
.cw-band h3 {{ color:#FFFFFF !important; margin:0; }} .cw-band p {{ color:#E4E8F0 !important; margin:.2rem 0 0 0; }}
.cw-badge {{ display:inline-block; padding:2px 9px; font-size:.72rem; font-weight:600; border-radius:2px; margin-right:4px; }}
.b-red {{ background:#F7E3E3; color:{C['red']}; }} .b-amber {{ background:#FBF0DA; color:{C['amber']}; }}
.b-green {{ background:#E1F1EA; color:{C['green']}; }} .b-navy {{ background:#E5E9F2; color:var(--navy); }}
.cw-pagehead {{ background:linear-gradient(110deg, var(--navy), var(--navy2)); border-left:5px solid var(--copper); padding:30px 36px 24px; margin:16px 0 12px; }}
.cw-pagehead h1 {{ color:#FFFFFF !important; margin:0; font-size:2.4rem; }} .cw-pagehead p {{ color:#E4E8F0 !important; margin:.3rem 0 0 0; }}
.cw-pagehead .crumb {{ color:var(--copper-l) !important; font-size:.74rem; letter-spacing:2.5px; text-transform:uppercase; font-weight:600; }}
.cw-pagehead::after {{ content:""; display:block; width:64px; height:4px; background:var(--copper-l); margin-top:14px; }}

/* ---------- pied de page */
.cw-footer {{ background:var(--navy); color:#E4E8F0; border-top:4px solid var(--copper); margin:60px 0 0; padding:36px 40px 18px; font-size:.86rem; }}
.cw-footer h6 {{ color:#FFFFFF !important; font-size:.78rem; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:.7rem; font-weight:700; }}
.cw-footer .col {{ min-width:200px; flex:1; color:#D3D9E5; }} .cw-footer .row {{ display:flex; gap:36px; flex-wrap:wrap; }}
.cw-footer .legal {{ border-top:1px solid rgba(255,255,255,.18); margin-top:26px; padding-top:14px; font-size:.74rem; color:#C3CAD8; line-height:1.55; }}
.cw-footer .ver {{ color:var(--copper-l); font-weight:600; }}
[data-testid="stHeaderActionElements"], .cw-hero a.anchor-link, h1 a[href^="#"] {{ display:none !important; }}

/* ---------- formulaires et boutons généraux */
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primaryFormSubmit"] {{ background:var(--navy); border-color:var(--navy); border-radius:2px; }}
button[kind="primary"] p, button[kind="primaryFormSubmit"] p {{ color:#fff !important; }}
.stButton button[kind="secondary"] {{ background:#fff; color:var(--navy); border-color:var(--navy); }}
.stButton button[kind="secondary"] p {{ color:var(--navy); }}
.stButton button[kind="primary"]:hover {{ background:var(--copper); border-color:var(--copper); }}
.stDownloadButton button {{ border-radius:2px; border-color:var(--navy); color:var(--navy); }}
[data-testid="stTabs"] button[role="tab"] p {{ font-weight:600; letter-spacing:.3px; }}
[data-baseweb="tab-highlight"] {{ background:var(--copper) !important; }}
@media (max-width: 760px) {{
  .cw-hero h1 {{ font-size:2.05rem; }} .cw-hero {{ padding:26px 20px 18px; }} .cw-pagehead {{ padding:24px 20px; }} .cw-footer {{ padding:30px 20px 16px; }}
  .cw-pagehead h1 {{ font-size:1.9rem; }}
}}
</style>""", unsafe_allow_html=True)


def brand_html():
    return f"""<div class="cw-brand">{LOGO_SVG}<div><div class="t1">COMPLY WORLD</div>
    <div class="t2">CONSULTING · ADVISORY</div></div></div>"""


def topnav(user: dict | None):
    page = st.session_state.get("page", "accueil")
    with st.container(key="topnav"):
        c = st.columns([1.9, .58, .8, .98, .92, .84, .64, 1.6], vertical_alignment="center")
        c[0].markdown(brand_html(), unsafe_allow_html=True)
        for i, (key, label) in enumerate(PAGES_PUBLIQUES, start=1):
            txt = f"**{label}**" if key == page else label
            c[i].button(txt, key=f"nav_{key}", type="tertiary", on_click=go, args=(key,), width="stretch")
        with c[7]:
            if user:
                lbl = "Admin" if user.get("role") == "admin" else "Mon espace"
                target = "admin" if user.get("role") == "admin" else "espace"
                b1, b2 = st.columns([3, 1.1])
                b1.button(f"👤 {lbl}", key="nav_space", type="primary", on_click=go, args=(target,), width="stretch")
                b2.button("⏻", key="nav_logout", help="Se déconnecter", on_click=logout, width="stretch")
            else:
                st.button("👤 Espace client", key="nav_login", type="primary", on_click=go, args=("connexion",),
                          width="stretch", help="Accès réservé aux abonnés")


def logout():
    st.session_state.user = None
    st.session_state.page = "accueil"


def home_button(key: str = "home"):
    st.button("← Retour à l'accueil", key=f"home_{key}", on_click=go, args=("accueil",), type="secondary")


def page_head(crumb: str, title: str, lead: str = ""):
    st.markdown(f"""<div class="cw-pagehead"><div class="crumb">{html.escape(crumb)}</div>
    <h1>{html.escape(title)}</h1><p>{html.escape(lead)}</p></div>""", unsafe_allow_html=True)


def section(eyebrow: str, title: str, lead: str = ""):
    st.markdown(f"""<div class="cw-section"><div class="cw-eyebrow">{html.escape(eyebrow)}</div>
    <div class="cw-title">{html.escape(title)}</div><div class="cw-rule"></div>
    {f'<div class="cw-lead">{html.escape(lead)}</div>' if lead else ''}</div>""", unsafe_allow_html=True)


def card(icon: str, title: str, text: str, more: str = ""):
    st.markdown(f"""<div class="cw-card"><div class="ico">{icon}</div><h4>{html.escape(title)}</h4>
    <p>{html.escape(text)}</p>{f'<span class="more">+ {html.escape(more)}</span>' if more else ''}</div>""", unsafe_allow_html=True)


def kpi(value, label):
    st.markdown(f'<div class="cw-kpi"><div class="v">{html.escape(str(value))}</div><div class="l">{html.escape(label)}</div></div>',
                unsafe_allow_html=True)


def badge(text: str, tone: str = "navy"):
    return f'<span class="cw-badge b-{tone}">{html.escape(text)}</span>'


FOOTER_EXPERTISES = ["Diagnostic et cartographie des risques", "Parcours de mise en conformité", "Dispositif de contrôle interne",
                     "KYC / KYB et remédiation", "Sanctions et gel des avoirs", "Déclarations de soupçon", "Formation et sensibilisation",
                     "Veille réglementaire"]


def _open_expertise(titre: str):
    st.session_state.expertise_once = titre
    go("expertises")


def footer():
    """Pied de page bleu nuit ; les liens sont de vrais boutons (la session et la connexion sont conservées)."""
    st.markdown("""<style>
    .st-key-cwfooter {{ background:var(--navy); border-top:4px solid var(--copper); margin-top:60px; padding:34px 40px 18px; }}
    .st-key-cwfooter button[kind="tertiary"] {{ padding:1px 0; min-height:0; justify-content:flex-start; }}
    .st-key-cwfooter button[kind="tertiary"] p {{ color:#D3D9E5 !important; font-size:.86rem; text-align:left; }}
    .st-key-cwfooter button[kind="tertiary"]:hover p {{ color:#FFFFFF !important; text-decoration:underline; text-decoration-color:var(--copper-l);
        text-underline-offset:4px; }}
    .st-key-cwfooter [data-testid="stVerticalBlock"] {{ gap:.15rem; }}
    .cwf-h {{ color:#FFFFFF; font-size:.78rem; letter-spacing:2.5px; text-transform:uppercase; font-weight:700; margin-bottom:.5rem; }}
    .cwf-t {{ color:#D3D9E5; font-size:.86rem; line-height:1.6; }}
    @media (max-width: 760px) {{ .st-key-cwfooter {{ padding:26px 18px 14px; }} }}
    </style>""".replace("{{", "{").replace("}}", "}"), unsafe_allow_html=True)
    contact = [html.escape(x) for x in (CONTACT_EMAIL, CONTACT_PHONE) if x] + [html.escape(CONTACT_CITY)]
    with st.container(key="cwfooter"):
        c1, c2, c3, c4 = st.columns([1.4, .8, 1.2, .9], gap="medium")
        with c1:
            st.markdown("""<div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:#FFFFFF;font-weight:700;letter-spacing:.6px;line-height:1.2">COMPLY WORLD CONSULTING</div>
            <div style="color:#E9C9A6;font-size:.7rem;letter-spacing:3px;margin:.35rem 0 .8rem;font-weight:600">ADVISORY &amp; REGULATORY</div>
            <div class="cwf-t">Cabinet de conseil en conformité financière : LCB-FT, sanctions internationales, contrôle interne et actualités réglementaires,
            pour les acteurs financiers et non financiers d'Europe, d'Haïti et des Amériques.</div>""", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="cwf-h">Naviguer</div>', unsafe_allow_html=True)
            for key, label in PAGES_PUBLIQUES:
                st.button(label, key=f"ft_{key}", type="tertiary", on_click=go, args=(key,))
            st.button("Espace client", key="ft_login", type="tertiary", on_click=go, args=("connexion",))
        with c3:
            st.markdown('<div class="cwf-h">Expertises</div>', unsafe_allow_html=True)
            for i, t in enumerate(FOOTER_EXPERTISES):
                st.button(t, key=f"ft_exp_{i}", type="tertiary", on_click=_open_expertise, args=(t,))
        with c4:
            st.markdown('<div class="cwf-h">Contact</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="cwf-t">{"<br>".join(contact)}</div>', unsafe_allow_html=True)
            st.button("Nous écrire →", key="ft_write", type="tertiary", on_click=go, args=("contact",))
            if LINKEDIN_URL:
                st.markdown(f'<a href="{html.escape(LINKEDIN_URL)}" target="_blank" style="color:#E9C9A6">LinkedIn</a>', unsafe_allow_html=True)
        st.markdown(f"""<div style="border-top:1px solid rgba(255,255,255,.18);margin-top:20px;padding-top:12px;font-size:.74rem;color:#C3CAD8;line-height:1.55">
        <span style="color:#E9C9A6;font-weight:600">{html.escape(FOOTER_LINE)}</span><br>{html.escape(DISCLAIMER)}<br>
        © 2026 {html.escape(BRAND)} — Mentions légales · Politique de confidentialité</div>""", unsafe_allow_html=True)


def require(user, service: str) -> bool:
    from .auth import can
    if can(user, service):
        return True
    st.info("Ce service n'est pas inclus dans votre abonnement. Contactez-nous pour faire évoluer votre offre.")
    return False


# ============================================================================ TABLEAUX, LIENS ET SCHÉMAS (rendu HTML, indépendant du thème)
_TABLE_CSS = """<style>
.cw-table-wrap { overflow-x:auto; margin:.4rem 0 1rem; border:1px solid #E3E6EE; }
table.cw-table { width:100%; border-collapse:collapse; font-size:.9rem; background:#FFFFFF; }
table.cw-table th { background:#0F1E3D; color:#FFFFFF !important; text-align:left; font-weight:600; padding:10px 12px; font-size:.8rem;
    letter-spacing:.4px; text-transform:uppercase; border-right:1px solid rgba(255,255,255,.12); }
table.cw-table td { color:#1C2333 !important; padding:9px 12px; border-top:1px solid #E3E6EE; vertical-align:top; line-height:1.45; }
table.cw-table tr:nth-child(even) td { background:#F7F8FB; }
table.cw-table td:first-child { font-weight:600; color:#0F1E3D !important; }
table.cw-table a, .cw-links a { color:#B8743A !important; text-decoration:none; font-weight:600; }
table.cw-table a:hover, .cw-links a:hover { text-decoration:underline; }
.cw-links { font-size:.8rem; margin:.15rem 0 .55rem 0; }
.cw-links a { margin-right:12px; white-space:nowrap; }
.cw-ref { margin-bottom:.35rem; color:#1C2333; }
.cw-flow { display:flex; flex-wrap:wrap; align-items:stretch; gap:0; margin:.5rem 0 1rem; }
.cw-flow .st { flex:1 1 150px; background:#FFFFFF; border:1px solid #E3E6EE; border-top:3px solid #0F1E3D; padding:10px 12px; min-width:140px; }
.cw-flow .st .n { color:#B8743A; font-size:.7rem; letter-spacing:1.5px; text-transform:uppercase; font-weight:700; }
.cw-flow .st .t { color:#0F1E3D; font-weight:700; font-size:.95rem; margin:.15rem 0; }
.cw-flow .st .a { color:#1B2E57; font-size:.8rem; font-weight:600; }
.cw-flow .st .d { color:#5B6478; font-size:.8rem; margin-top:.25rem; line-height:1.35; }
.cw-flow .ar { align-self:center; color:#B8743A; font-size:1.4rem; padding:0 6px; }
</style>"""


def _cell(v) -> str:
    s = "" if v is None else str(v)
    if s in ("nan", "None"):
        return ""
    if s.startswith("http"):
        return f'<a href="{html.escape(s)}" target="_blank">Ouvrir ↗</a>'
    return html.escape(s)


def html_table(columns, rows):
    """Tableau HTML sobre (en-tête bleu nuit, lignes alternées) — rendu identique en thème clair ou sombre."""
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in columns)
    body = "".join("<tr>" + "".join(f"<td>{_cell(v)}</td>" for v in r) + "</tr>" for r in rows)
    st.markdown(_TABLE_CSS + f'<div class="cw-table-wrap"><table class="cw-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>',
                unsafe_allow_html=True)


def df_table(df, columns: dict | None = None):
    """Affiche un DataFrame avec html_table ; `columns` = {colonne: libellé} pour sélectionner et renommer."""
    if columns:
        df = df[list(columns)]
        cols = list(columns.values())
    else:
        cols = list(df.columns)
    html_table(cols, df.values.tolist())


def links_html(pairs) -> str:
    if not pairs:
        return ""
    return '<div class="cw-links">' + "".join(f'<a href="{html.escape(u)}" target="_blank">↗ {html.escape(n)}</a>' for n, u in pairs) + "</div>"


def ref_list(items):
    """Liste de références réglementaires avec liens officiels détectés automatiquement."""
    from .links import autolinks
    out = []
    for it in items:
        out.append(f'<div class="cw-ref">• {html.escape(it)}</div>{links_html(autolinks(it))}')
    st.markdown(_TABLE_CSS + "".join(out), unsafe_allow_html=True)


def flow(steps):
    """Schéma du circuit : steps = [(étape, acteur, détail), ...]."""
    parts = []
    for i, (e, a, d) in enumerate(steps, 1):
        if i > 1:
            parts.append('<div class="ar">→</div>')
        parts.append(f'<div class="st"><div class="n">Étape {i}</div><div class="t">{html.escape(e)}</div>'
                     f'<div class="a">{html.escape(a)}</div><div class="d">{html.escape(d)}</div></div>')
    st.markdown(_TABLE_CSS + f'<div class="cw-flow">{"".join(parts)}</div>', unsafe_allow_html=True)
