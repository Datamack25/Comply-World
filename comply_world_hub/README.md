# Comply World Consulting — site du cabinet et Compliance Hub (v1.3.0, novembre 2026)

Site vitrine du cabinet (accueil, cabinet, expertises, juridictions, actualités, contact) et espace abonné
(parcours de mise en conformité, dispositif de contrôle, cartographie Haïti, référentiels, pays à risque, veille).

## Lancer
```bash
pip install -r requirements.txt
streamlit run app.py
```
Premier lancement : la page « Espace client » propose de créer le compte administrateur.
Sur Streamlit Cloud, définissez plutôt l'administrateur dans *Settings > Secrets* (voir `.streamlit/secrets.toml.example`).

## Navigation
- Bouton **Accueil** dans la barre de navigation + bouton « Retour à l'accueil » sur chaque page.
- Icône **👤 Espace client** : connexion des abonnés et demande d'abonnement (activée par l'administrateur).
- **Administration** : bouton « Mettre à jour la veille conformité », gestion des abonnés et offres, messages, édition/remplacement des CSV.

## Offres (services activés manuellement)
| Offre | Services |
|---|---|
| Essentiel | Veille, référentiel, pays à risque |
| Professionnel | + parcours, dispositif de contrôle, cartographie Haïti |
| Intégral | + exports PDF / Word / Excel |

## Données (`data/`)
- `haiti/` : cadre juridique, entités assujetties (art. 4-5 du décret du 30 avril 2023), seuils, menaces, vulnérabilités, produits bancaires, plan d'action (ENR déc. 2025)
- `parcours/` : étapes par juridiction × type d'entité (40 combinaisons), dispositif de contrôle (25 contrôles × 6 juridictions)
- `europe/`, `ameriques/`, `referentiels/` (pays GAFI oct. 2026 / UE janv. 2026, liens officiels, échéancier, références par thème)
- `veille/` : sources suivies (RSS + pages officielles) et actualités
- Régénération complète : `python tools/build_data.py` (écrase les CSV).

Les références marquées « à confirmer » (Mexique, République dominicaine) doivent être vérifiées dans les textes officiels.

## Persistance
Comptes (`data/runtime/users.json`, mots de passe PBKDF2), messages et journal de veille sont stockés localement.
Sur Streamlit Cloud le disque est éphémère : prévoir une base (ex. Supabase) pour la production.

---
Comply World Compliance Hub · version 1.3.0 (Novembre 2026) · Conçu et développé par Mackenson CINEUS
