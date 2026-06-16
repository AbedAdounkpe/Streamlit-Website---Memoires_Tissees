import csv
import io
import base64
import mimetypes
from pathlib import Path
from datetime import datetime

import streamlit as st


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
            padding-top: 1rem;
            padding-bottom: 1rem;
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
            background: #000000;
            border: 2px solid #B3001B;
            border-radius: 20px;
            padding: 1.4rem 1.6rem;
            margin-top: 0;
            margin-bottom: 1rem;
            box-shadow: 0 10px 24px rgba(179, 0, 27, 0.2);
        }

        .titre-principal {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.1;
            margin: 0;
            color: #FFFFFF;
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
            border: 1px solid #B3001B;
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

        /* Choix en cartes cliquables (proposition 2) - tous sur une ligne */
        div[role="radiogroup"] {
            display: flex;
            flex-wrap: nowrap;
            gap: 0.6rem;
            margin-top: 0.4rem;
        }

        div[role="radiogroup"] > label {
            position: relative;
            flex: 1 1 0;
            min-width: 0;
            min-height: 64px;
            margin: 0 !important;
            padding: 0.85rem 0.7rem;
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
            content: "\2713";
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
            <p class="sous-titre">
                Questionnaire de satisfaction de l'événement du 20 juin 2026 à Rouen.
            </p>
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

    with st.form("formulaire_satisfaction"):
        st.subheader("Questionnaire de satisfaction")

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
        )

        q4_apprentissage = st.radio(
            "4) Pensez-vous avoir découvert ou appris de nouvelles choses sur les textiles africains ?",
            ["Oui, beaucoup", "Oui, un peu", "Pas vraiment", "Pas du tout"],
            index=None,
            horizontal=True,
        )

        q5_regard = st.radio(
            "5) Après cet événement, portez-vous un regard différent sur les tissus traditionnels africains ?",
            ["Oui", "Non", "Je ne sais pas"],
            index=None,
            horizontal=True,
        )

        q6_valorisation = st.radio(
            "6) Selon vous, l'événement a-t-il permis de mieux valoriser le patrimoine culturel béninois et africain ?",
            ["Tout à fait", "Plutôt oui", "Plutôt non", "Pas du tout"],
            index=None,
            horizontal=True,
        )

        q7_recommandation = st.radio(
            "7) Recommanderiez-vous cet événement à votre entourage ?",
            ["Oui", "Non"],
            index=None,
            horizontal=True,
        )

        q8_suggestions = st.radio(
            "8) Avez-vous des suggestions pour une prochaine édition ?",
            [
                "Ateliers pratiques",
                "Plus de temps d'échanges",
                "Programme sur plusieurs jours",
                "Davantage d'exposants",
                "Aucune suggestion",
            ],
            index=None,
            horizontal=True,
        )

        consentement = st.checkbox(
            "J'accepte que mes réponses soient utilisées de manière anonyme pour améliorer l'événement.",
            value=True,
        )

        soumis = st.form_submit_button("Envoyer mon avis")

    st.markdown("</div>", unsafe_allow_html=True)

    if soumis:
        reponses_principales = [
            q1_canal,
            q2_experience,
            q3_temps_forts,
            q4_apprentissage,
            q5_regard,
            q6_valorisation,
            q7_recommandation,
            q8_suggestions,
        ]

        if any(reponse is None for reponse in reponses_principales):
            st.error("Merci de répondre à toutes les questions avant l'envoi.")
        elif not consentement:
            st.error("Merci d'accepter l'utilisation anonyme des réponses pour valider l'envoi.")
        else:
            score_mapping = {
                "1 étoile": 1,
                "2 étoiles": 2,
                "3 étoiles": 3,
                "4 étoiles": 4,
                "5 étoiles": 5,
            }
            score_numerique = score_mapping.get(q2_experience)

            st.success("Merci ! Votre avis a bien été enregistré.")
            if score_numerique is not None:
                st.metric("Évaluation globale", f"{score_numerique} / 5")
                st.progress(score_numerique / 5)
            else:
                st.info("Évaluation globale personnalisée enregistrée.")

            if score_numerique is not None and score_numerique >= 4:
                st.info("Merci pour votre retour positif. Vos suggestions nous aideront à faire encore mieux.")
            else:
                st.warning("Merci pour votre sincérité. Nous allons prioriser les points d'amélioration cités.")

            donnees = {
                "horodatage": datetime.now().isoformat(timespec="seconds"),
                "q1_canal_connaissance": q1_canal,
                "q2_experience": q2_experience,
                "q3_temps_forts": q3_temps_forts,
                "q4_apprentissage_textiles": q4_apprentissage,
                "q5_regard_different": q5_regard,
                "q6_valorisation_patrimoine": q6_valorisation,
                "q7_recommandation": q7_recommandation,
                "q8_suggestions": q8_suggestions,
                "consentement": consentement,
                "score_global_5": score_numerique if score_numerique is not None else "Personnalise",
                "score_global_100": round(score_numerique / 5 * 100, 1) if score_numerique is not None else "N/A",
            }

            tampon = io.StringIO()
            writer = csv.DictWriter(tampon, fieldnames=list(donnees.keys()))
            writer.writeheader()
            writer.writerow(donnees)

            st.download_button(
                label="Télécharger ma réponse (CSV)",
                data=tampon.getvalue().encode("utf-8"),
                file_name="satisfaction_tissus_afrique_2026.csv",
                mime="text/csv",
            )

    st.caption(
        "Association Mikwabo - Enquête de satisfaction de l'événement du 20 juin 2026, Centre André Malraux, Rouen."
    )
