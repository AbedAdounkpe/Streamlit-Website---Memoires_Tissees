import csv
import base64
import mimetypes
from pathlib import Path
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components


def enregistrer_dans_google_sheets(donnees: dict) -> bool:
    """Ajoute une ligne dans le Google Sheet configure via st.secrets.

    Retourne True si l'enregistrement a reussi, False sinon (secrets absents
    ou erreur), afin de permettre un repli sur le CSV local.
    """
    if "gcp_service_account" not in st.secrets or "google_sheet" not in st.secrets:
        return False
    try:
        import gspread

        client = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
        config = st.secrets["google_sheet"]
        classeur = client.open_by_key(config["sheet_id"])
        feuille = classeur.worksheet(config.get("worksheet", "Feuille 1"))

        if not feuille.row_values(1):
            feuille.append_row(list(donnees.keys()), value_input_option="USER_ENTERED")
        feuille.append_row(
            [str(valeur) for valeur in donnees.values()],
            value_input_option="USER_ENTERED",
        )
        return True
    except Exception as erreur:  # noqa: BLE001 - on veut un repli robuste
        st.warning(f"Enregistrement Google Sheets indisponible, sauvegarde locale utilisee. ({erreur})")
        return False


def enregistrer_dans_csv_local(donnees: dict) -> None:
    fichier_reponses = Path(__file__).resolve().parent / "reponses" / "reponses_satisfaction.csv"
    fichier_reponses.parent.mkdir(parents=True, exist_ok=True)
    fichier_existe = fichier_reponses.exists()
    with fichier_reponses.open("a", newline="", encoding="utf-8-sig") as flux:
        writer = csv.DictWriter(flux, fieldnames=list(donnees.keys()))
        if not fichier_existe:
            writer.writeheader()
        writer.writerow(donnees)


st.set_page_config(
    page_title="Satisfaction - Tissus d'Afrique & mémoires tissées",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def trouver_image_evenement() -> Path | None:
    assets = Path("assets")
    if not assets.exists():
        return None
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    for ext in extensions:
        fichiers = sorted(assets.glob(ext))
        if fichiers:
            return fichiers[0]
    return None


def image_vers_data_uri(path_image: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path_image.name)
    if mime_type is None:
        mime_type = "image/jpeg"
    contenu = path_image.read_bytes()
    encode = base64.b64encode(contenu).decode("ascii")
    return f"data:{mime_type};base64,{encode}"


image_evenement = trouver_image_evenement()


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

        .stApp {
            background: #000000;
            color: #FFFFFF;
            font-family: 'Montserrat', sans-serif;
        }

        .block-container {
            padding-top: 5.5rem;
            padding-bottom: 1rem;
        }

        /* Bandeau noir en haut + barre Streamlit opaque pour ne rien masquer */
        header[data-testid="stHeader"] {
            background: #000000;
            height: 2cm;
        }

        /* Barre de progression flottante en haut du site */
        .barre-progression-fixe {
            position: fixed;
            top: 2cm;
            left: 0;
            width: 100%;
            height: 28px;
            background: #161616;
            border-bottom: 1px solid #B3001B;
            z-index: 1000;
            overflow: hidden;
        }

        .barre-progression-remplissage {
            height: 100%;
            background: linear-gradient(90deg, #B3001B, #FF3B57);
            transition: width 350ms ease;
        }

        .barre-progression-texte {
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            line-height: 28px;
            font-size: 0.82rem;
            font-weight: 700;
            color: #FFFFFF;
            white-space: nowrap;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
        }

        section[data-testid="stSidebar"] {
            background: #0A0A0A;
            border-right: 2px solid #B3001B;
        }

        section[data-testid="stSidebarNav"]::before {
            content: "Navigation";
            display: block;
            color: #FFFFFF;
            font-size: 1.12rem;
            font-weight: 700;
            margin: 0 0 0.65rem 0;
        }

        section[data-testid="stSidebar"] * {
            font-size: 1.08rem !important;
        }

        section[data-testid="stSidebar"] .stButton button {
            font-size: 1.08rem !important;
            padding: 0.65rem 0.8rem;
        }

        .bloc-hero {
            background: transparent;
            border: none;
            padding: 0;
            margin-top: 0;
            margin-bottom: 1rem;
        }

        .titre-principal {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.1;
            margin: 0;
            color: #FFFFFF;
            text-align: center;
        }

        .sous-titre {
            margin-top: 0.5rem;
            font-size: 1.05rem;
            color: #F2F2F2;
        }

        .badge {
            display: inline-block;
            margin-top: 0.85rem;
            margin-right: 0.45rem;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            background: #111111;
            border: 1px solid #B3001B;
            color: #FFFFFF;
            font-size: 0.84rem;
            font-weight: 600;
        }

        .bloc-formulaire {
            background: #050505;
            border: none;
            border-radius: 18px;
            padding: 1.2rem;
        }

        .image-flottante {
            position: sticky;
            top: 0;
            z-index: 5;
        }

        .image-flottante img {
            width: 100%;
            max-height: calc(100vh - 2rem);
            object-fit: contain;
            border: 2px solid #B3001B;
            border-radius: 14px;
        }

        .stSlider > div[data-baseweb='slider'] > div > div {
            background: #B3001B;
        }

        .stButton button, .stDownloadButton button {
            background: #B3001B;
            color: #FFFFFF;
            border: 0;
            font-weight: 700;
            border-radius: 12px;
            padding: 0.55rem 1rem;
        }

        .stButton button:hover, .stDownloadButton button:hover {
            filter: brightness(1.02);
            transform: translateY(-1px);
            transition: all 120ms ease;
        }

        .aide {
            font-size: 0.9rem;
            color: #EDEDED;
        }

        p, li, label, .stMarkdown, .stCaption, h1, h2, h3 {
            color: #FFFFFF !important;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] > div {
            background: #101010 !important;
            color: #FFFFFF !important;
            border: 1px solid #B3001B !important;
        }

        /* Choix en cartes cliquables (proposition 2) - une carte par ligne */
        div[data-testid="stElementContainer"]:has(div[role="radiogroup"]) {
            width: 100% !important;
        }

        div[data-testid="stRadio"] {
            width: 100% !important;
            max-width: 420px;
            margin-left: auto;
            margin-right: auto;
        }

        div[data-testid="stRadio"] > div {
            width: 100% !important;
        }

        div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            flex-wrap: nowrap;
            align-items: stretch;
            gap: 0.6rem;
            margin-top: 0.4rem;
            width: 100% !important;
        }

        div[role="radiogroup"] > label {
            position: relative;
            width: 100% !important;
            max-width: none;
            box-sizing: border-box;
            height: 56px;
            margin: 0 !important;
            padding: 0.5rem 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            line-height: 1.2;
            background: #0B0B0B;
            border: 1.5px solid #2A2A2A;
            border-radius: 14px;
            cursor: pointer;
            font-weight: 600;
            transition: all 140ms ease;
        }

        /* Masque le rond radio natif, on garde juste le libellé */
        div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        div[role="radiogroup"] > label > div:last-child {
            margin: 0 !important;
            white-space: normal;
            overflow-wrap: anywhere;
        }

        div[role="radiogroup"] > label:hover {
            border-color: #B3001B;
            transform: translateY(-2px);
        }

        div[role="radiogroup"] > label:has(input:checked) {
            border-color: #B3001B;
            background: linear-gradient(180deg, rgba(179, 0, 27, 0.28), rgba(179, 0, 27, 0.10));
            box-shadow: 0 6px 16px rgba(179, 0, 27, 0.35);
        }

        div[role="radiogroup"] > label:has(input:checked)::after {
            content: "✓";
            position: absolute;
            top: 6px;
            right: 9px;
            color: #FFFFFF;
            font-weight: 800;
            font-size: 0.95rem;
        }

        @media (max-width: 992px) {
            .image-flottante {
                position: static;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col_gauche, col_droite = st.columns([35, 65], gap="large", vertical_alignment="top")

if st.session_state.pop("revenir_en_haut", False):
    components.html(
        """
        <script>
            const doc = window.parent.document;
            const conteneur = doc.querySelector('section.main')
                || doc.querySelector('[data-testid="stMain"]')
                || doc.scrollingElement;
            if (conteneur) { conteneur.scrollTo({ top: 0, behavior: 'smooth' }); }
            window.parent.scrollTo({ top: 0, behavior: 'smooth' });
        </script>
        """,
        height=0,
    )

with col_gauche:
    if image_evenement is not None:
        data_uri_image = image_vers_data_uri(image_evenement)
        st.markdown(
            f"""
            <div class="image-flottante">
                <img src="{data_uri_image}" alt="Affiche de l'evenement" />
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Aucune image détectée dans le dossier assets.")

with col_droite:
    st.markdown(
        """
        <section class="bloc-hero">
            <h1 class="titre-principal">Tissus d'Afrique & mémoires tissées</h1>
            <span class="badge">Patrimoines textiles africains</span>
            <span class="badge">Conférence-débat</span>
            <span class="badge">Performances artistiques</span>
            <span class="badge">Découverte culinaire béninoise</span>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Merci d'avoir participé à cette journée. Votre avis est précieux et nous aidera à améliorer nos futurs projets."
    )

    st.markdown('<div class="bloc-formulaire">', unsafe_allow_html=True)

    version_formulaire = st.session_state.get("version_formulaire", 0)

    q1_canal = st.radio(
        "1) Comment avez-vous connu l'événement ?",
        [
            "Réseaux sociaux",
            "Bouche-a-oreille",
            "Association",
            "Partenaire",
            "Presse / Media",
        ],
        index=None,
        horizontal=True,
        key=f"q1_canal_{version_formulaire}",
    )

    q2_experience = st.radio(
        "2) Globalement, comment évaluez-vous votre expérience ?",
        [
            "1 étoile",
            "2 étoiles",
            "3 étoiles",
            "4 étoiles",
            "5 étoiles",
        ],
        index=None,
        horizontal=True,
        key=f"q2_experience_{version_formulaire}",
    )

    q3_temps_forts = st.radio(
        "3) Quel temps fort avez-vous le plus apprécié ?",
        [
            "Exposition",
            "Conférence-débat",
            "Défilé",
            "Danses traditionnelles",
            "Découverte culinaire",
            "Échanges avec les intervenants",
        ],
        index=None,
        horizontal=True,
        key=f"q3_temps_forts_{version_formulaire}",
    )

    q4_apprentissage = st.radio(
        "4) Pensez-vous avoir découvert ou appris de nouvelles choses sur les textiles africains ?",
        ["Oui, beaucoup", "Oui, un peu", "Pas vraiment", "Pas du tout"],
        index=None,
        horizontal=True,
        key=f"q4_apprentissage_{version_formulaire}",
    )

    q5_regard = st.radio(
        "5) Après cet événement, portez-vous un regard différent sur les tissus traditionnels africains ?",
        ["Oui", "Non", "Je ne sais pas"],
        index=None,
        horizontal=True,
        key=f"q5_regard_{version_formulaire}",
    )

    reponses_principales = [
        q1_canal,
        q2_experience,
        q3_temps_forts,
        q4_apprentissage,
        q5_regard,
    ]
    nb_repondu = sum(1 for reponse in reponses_principales if reponse is not None)
    nb_total = len(reponses_principales)
    progression = round(nb_repondu / nb_total * 100)

    st.markdown(
        f"""
        <div class="barre-progression-fixe">
            <div class="barre-progression-remplissage" style="width: {progression}%;"></div>
            <span class="barre-progression-texte">Progression : {nb_repondu}/{nb_total} questions ({progression} %)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    deja_envoye = st.session_state.get("envoi_effectue", False)
    soumis = st.button("Envoyer mon avis", disabled=deja_envoye)

    st.markdown("</div>", unsafe_allow_html=True)

    if deja_envoye:
        st.success("Merci ! Votre avis a bien été enregistré.")
        if st.button("Répondre à nouveau"):
            st.session_state["version_formulaire"] = (
                st.session_state.get("version_formulaire", 0) + 1
            )
            st.session_state.pop("envoi_effectue", None)
            st.session_state["revenir_en_haut"] = True
            st.rerun()
    elif soumis:
        questions_manquantes = [
            index + 1
            for index, reponse in enumerate(reponses_principales)
            if reponse is None
        ]
        if questions_manquantes:
            if len(questions_manquantes) == 1:
                liste_manquantes = str(questions_manquantes[0])
                st.error(f"Merci de répondre à la question : {liste_manquantes}.")
            else:
                liste_manquantes = (
                    ", ".join(str(numero) for numero in questions_manquantes[:-1])
                    + " et "
                    + str(questions_manquantes[-1])
                )
                st.error(f"Merci de répondre aux questions : {liste_manquantes}.")
        else:
            donnees = {
                "horodatage": datetime.now().isoformat(timespec="seconds"),
                "q1_canal_connaissance": q1_canal,
                "q2_experience": q2_experience,
                "q3_temps_forts": q3_temps_forts,
                "q4_apprentissage_textiles": q4_apprentissage,
                "q5_regard_different": q5_regard,
            }

            if not enregistrer_dans_google_sheets(donnees):
                enregistrer_dans_csv_local(donnees)

            st.session_state.envoi_effectue = True
            st.rerun()

    st.caption(
        "Association Mikwabo - Enquête de satisfaction de l'événement du 20 juin 2026, Centre André Malraux, Rouen."
    )
