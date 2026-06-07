# Streamlit Projet WM

Application Streamlit de questionnaire de satisfaction pour l'evenement **Tissus d'Afrique & memoires tissees**.

## Apercu

![Affiche de l'evenement](assets/Image%20%C3%A9v%C3%A9nement.jpg)

Ce projet contient :

- Une page principale de questionnaire de satisfaction.
- Une page secondaire qui affiche une image d'affiche et un QR code vers le formulaire.
- Un export individuel de reponse au format CSV apres soumission.

## Structure du projet

```text
.
|- main.py
|- pages/
|  |- affiche_qr.py
|- assets/
|- # Questionnaire de satisfaction.md
```

## Prerequis

- Python 3.10+
- pip

## Installation

1. Ouvrir un terminal dans le dossier du projet.
2. (Optionnel) Creer et activer un environnement virtuel.
3. Installer Streamlit :

```powershell
pip install streamlit
```

## Lancer l'application

Depuis le dossier racine du projet :

```powershell
streamlit run main.py
```

L'application sera accessible localement, en general sur :

```text
http://localhost:8501
```

## Configuration rapide

### 1) Image de l'evenement

Placez une image dans le dossier `assets/` (formats supportes : `.jpg`, `.jpeg`, `.png`, `.webp`).

La premiere image trouvee est utilisee automatiquement sur les pages.

### 2) URL encodee dans le QR code

Dans `pages/affiche_qr.py`, modifiez la constante :

```python
SITE_URL = "http://localhost:8501"
```

Remplacez-la par l'URL finale de votre site (exemple : URL publique de deploiement).

## Fonctionnement du questionnaire

- Le formulaire est affiche dans `main.py`.
- A la soumission, les reponses sont preparees en memoire.
- Un bouton permet de telecharger la reponse au format CSV.

Nom du fichier exporte :

```text
satisfaction_tissus_afrique_2026.csv
```

## Notes

- Le fichier `# Questionnaire de satisfaction.md` contient une version texte du questionnaire.
- La navigation entre pages se fait via la sidebar Streamlit.
