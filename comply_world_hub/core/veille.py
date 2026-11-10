# -*- coding: utf-8 -*-
"""Veille conformité : collecte des flux RSS et surveillance des pages officielles.

Déclenchée depuis l'espace administrateur (bouton « Mettre à jour la veille »).
- Flux RSS : nouveaux articles filtrés par mots-clés, dédoublonnés par lien et par titre.
- Pages officielles : une empreinte du contenu est conservée ; toute modification est signalée
  comme actualité « Page officielle modifiée » afin d'être analysée par un consultant.
"""
import hashlib
import json
import re
from datetime import datetime, date

import pandas as pd
import requests

from .config import RUNTIME
from .data import load, save

HASHES = RUNTIME / "veille_empreintes.json"
LOG = RUNTIME / "veille_journal.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; ComplyWorldVeille/1.3; +conformite)"}

MOTS_CLES = [
    "blanchiment", "lcb", "lbc", "financement du terrorisme", "gafi", "fatf", "amla", "amlr", "aml", "anti-money",
    "money laundering", "sanction", "gel des avoirs", "ofac", "tracfin", "ucref", "brh", "fincen", "fintrac", "canafe",
    "lavado", "uif", "uaf", "pld", "kyc", "bénéficiaire effectif", "beneficial owner", "ppe", "pep", "embargo",
    "crypto", "mica", "terrorist financing", "compliance", "conformité",
]


def _pertinent(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in MOTS_CLES)


def _clean(html: str) -> str:
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html or "", flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()


def _load_json(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
    except Exception:
        return default


def mettre_a_jour(max_par_source: int = 8, timeout: int = 12) -> dict:
    import feedparser

    sources = load("veille/veille_sources.csv")
    sources = sources[sources.actif.astype(int) == 1]
    actus = load("veille/veille_actualites.csv").copy()
    liens_connus = set(actus["lien"].astype(str))
    titres_connus = set(actus["titre"].astype(str).str.lower().str.strip())
    hashes = _load_json(HASHES, {})
    nouvelles, rapport = [], []

    for _, s in sources.iterrows():
        try:
            if s.type == "rss":
                r = requests.get(s.url, headers=UA, timeout=timeout)
                r.raise_for_status()
                feed = feedparser.parse(r.content)
                n = 0
                for e in feed.entries[: max_par_source * 3]:
                    titre = _clean(e.get("title", ""))
                    lien = e.get("link", "")
                    resume = _clean(e.get("summary", ""))[:400]
                    if not titre or lien in liens_connus or titre.lower().strip() in titres_connus:
                        continue
                    if not _pertinent(titre + " " + resume):
                        continue
                    d = e.get("published_parsed") or e.get("updated_parsed")
                    d = date(*d[:3]).isoformat() if d else date.today().isoformat()
                    src = e.get("source", {}).get("title") if isinstance(e.get("source"), dict) else None
                    nouvelles.append(dict(date=d, juridiction=s.juridiction, theme=s.theme, titre=titre, resume=resume,
                                          source=src or s.nom, lien=lien, origine="Flux RSS"))
                    liens_connus.add(lien); titres_connus.add(titre.lower().strip())
                    n += 1
                    if n >= max_par_source:
                        break
                rapport.append(dict(source=s.nom, statut="OK", nouveautes=n))
            else:  # page officielle surveillée
                r = requests.get(s.url, headers=UA, timeout=timeout)
                r.raise_for_status()
                h = hashlib.sha256(_clean(r.text).encode()).hexdigest()
                ancien = hashes.get(s.url)
                hashes[s.url] = h
                if ancien is None:
                    rapport.append(dict(source=s.nom, statut="Référence enregistrée", nouveautes=0))
                elif ancien != h:
                    nouvelles.append(dict(date=date.today().isoformat(), juridiction=s.juridiction, theme=s.theme,
                                          titre=f"Page officielle modifiée : {s.nom}",
                                          resume="Le contenu de la page a changé depuis la dernière vérification. Analyse à réaliser par un consultant.",
                                          source=s.nom, lien=s.url, origine="Surveillance de page"))
                    rapport.append(dict(source=s.nom, statut="Modifiée", nouveautes=1))
                else:
                    rapport.append(dict(source=s.nom, statut="Inchangée", nouveautes=0))
        except Exception as ex:  # réseau indisponible, site bloqué…
            rapport.append(dict(source=s.nom, statut=f"Erreur : source injoignable ({type(ex).__name__})", nouveautes=0))

    if nouvelles:
        actus = pd.concat([pd.DataFrame(nouvelles), actus], ignore_index=True)
        save("veille/veille_actualites.csv", actus)
    HASHES.write_text(json.dumps(hashes, indent=1), encoding="utf-8")
    entry = dict(horodatage=datetime.now().isoformat(timespec="seconds"), nouveautes=len(nouvelles),
                 erreurs=sum(1 for r in rapport if r["statut"].startswith("Erreur")))
    journal = _load_json(LOG, [])
    journal.insert(0, entry)
    LOG.write_text(json.dumps(journal[:50], ensure_ascii=False, indent=1), encoding="utf-8")
    return dict(nouveautes=len(nouvelles), rapport=pd.DataFrame(rapport), entree=entry)


def derniere_maj() -> str:
    j = _load_json(LOG, [])
    return j[0]["horodatage"].replace("T", " à ") if j else "jamais"


def ajouter_manuellement(d, juridiction, theme, titre, resume, source, lien):
    actus = load("veille/veille_actualites.csv").copy()
    row = pd.DataFrame([dict(date=str(d), juridiction=juridiction, theme=theme, titre=titre, resume=resume,
                             source=source, lien=lien, origine="Saisie consultant")])
    save("veille/veille_actualites.csv", pd.concat([row, actus], ignore_index=True))
