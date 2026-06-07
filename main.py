import csv
import io
import base64
import mimetypes
from pathlib import Path
from datetime import datetime

import streamlit as st
from streamlit.errors import StreamlitAPIException


st.set_page_config(
    page_title="Satisfaction - Tissus d'Afrique & mémoires tissées",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with st.sidebar:
    st.markdown("### Navigation")
    st.button("Questionnaire", use_container_width=True, disabled=True)
    if st.button("Affiche + QR", use_container_width=True):
        navigation_ok = False
        candidats = [
            "pages/affiche_qr.py",
            "affiche_qr.py",
            "Affiche Qr",
            "Affiche & QR",
        ]
        for cible in candidats:
            try:
                st.switch_page(cible)
                navigation_ok = True
                break
            except StreamlitAPIException:
                continue
        if not navigation_ok:
            st.error("Navigation impossible pour le moment. Redémarrez l'application Streamlit.")


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

        q1_canal = st.selectbox(
            "1) Comment avez-vous connu l'événement ?",
            [
                "Réseaux sociaux",
                "Bouche-a-oreille",
                "Association",
                "Partenaire",
                "Presse / Media",
                "Autre",
            ],
            index=None,
            placeholder="Choisissez une option",
        )
        q1_autre = ""
        if q1_canal == "Autre":
            q1_autre = st.text_input("Précisez le canal")

        q2_experience = st.selectbox(
            "2) Globalement, comment évaluez-vous votre expérience ?",
            [
                "1 étoile",
                "2 étoiles",
                "3 étoiles",
                "4 étoiles",
                "5 étoiles",
                "Autre",
            ],
            index=None,
            placeholder="Choisissez une option",
        )
        q2_autre = ""
        if q2_experience == "Autre":
            q2_autre = st.text_input("Précisez votre évaluation globale")

        q3_temps_forts = st.selectbox(
            "3) Quel temps fort avez-vous le plus apprécié ?",
            [
                "Exposition",
                "Conférence-débat",
                "Défilé",
                "Danses traditionnelles",
                "Découverte culinaire",
                "Échanges avec les intervenants",
                "Autre",
            ],
            index=None,
            placeholder="Choisissez une option",
        )
        q3_autre = ""
        if q3_temps_forts == "Autre":
            q3_autre = st.text_input("Précisez le temps fort")

        q4_apprentissage = st.selectbox(
            "4) Pensez-vous avoir découvert ou appris de nouvelles choses sur les textiles africains ?",
            ["Oui, beaucoup", "Oui, un peu", "Pas vraiment", "Pas du tout", "Autre"],
            index=None,
            placeholder="Choisissez une option",
        )
        q4_autre = ""
        if q4_apprentissage == "Autre":
            q4_autre = st.text_input("Précisez votre réponse")

        q5_regard = st.selectbox(
            "5) Après cet événement, portez-vous un regard différent sur les tissus traditionnels africains ?",
            ["Oui", "Non", "Je ne sais pas", "Autre"],
            index=None,
            placeholder="Choisissez une option",
        )
        q5_autre = ""
        if q5_regard == "Autre":
            q5_autre = st.text_input("Précisez votre réponse ", key="q5_autre")

        q6_valorisation = st.selectbox(
            "6) Selon vous, l'événement a-t-il permis de mieux valoriser le patrimoine culturel béninois et africain ?",
            ["Tout à fait", "Plutôt oui", "Plutôt non", "Pas du tout", "Autre"],
            index=None,
            placeholder="Choisissez une option",
        )
        q6_autre = ""
        if q6_valorisation == "Autre":
            q6_autre = st.text_input("Précisez votre réponse", key="q6_autre")

        q7_recommandation = st.selectbox(
            "7) Recommanderiez-vous cet événement à votre entourage ?",
            ["Oui", "Non", "Autre"],
            index=None,
            placeholder="Choisissez une option",
        )
        q7_autre = ""
        if q7_recommandation == "Autre":
            q7_autre = st.text_input("Précisez votre réponse", key="q7_autre")

        q8_suggestions = st.selectbox(
            "8) Avez-vous des suggestions pour une prochaine édition ?",
            [
                "Ateliers pratiques",
                "Plus de temps d'échanges",
                "Programme sur plusieurs jours",
                "Davantage d'exposants",
                "Aucune suggestion",
                "Autre",
            ],
            index=None,
            placeholder="Choisissez une option",
        )
        q8_autre = ""
        if q8_suggestions == "Autre":
            q8_autre = st.text_area(
                "Précisez votre suggestion",
                placeholder="Vos idées, propositions et recommandations...",
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
        autres_a_completer = [
            (q1_canal, q1_autre),
            (q2_experience, q2_autre),
            (q3_temps_forts, q3_autre),
            (q4_apprentissage, q4_autre),
            (q5_regard, q5_autre),
            (q6_valorisation, q6_autre),
            (q7_recommandation, q7_autre),
            (q8_suggestions, q8_autre),
        ]

        if any(reponse is None for reponse in reponses_principales):
            st.error("Merci de répondre à toutes les questions avant l'envoi.")
        elif any(reponse == "Autre" and not texte.strip() for reponse, texte in autres_a_completer):
            st.error("Merci de préciser chaque réponse marquée 'Autre'.")
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
                "q1_autre_precision": q1_autre,
                "q2_experience": q2_experience,
                "q2_autre_precision": q2_autre,
                "q3_temps_forts": q3_temps_forts,
                "q3_autre_precision": q3_autre,
                "q4_apprentissage_textiles": q4_apprentissage,
                "q4_autre_precision": q4_autre,
                "q5_regard_different": q5_regard,
                "q5_autre_precision": q5_autre,
                "q6_valorisation_patrimoine": q6_valorisation,
                "q6_autre_precision": q6_autre,
                "q7_recommandation": q7_recommandation,
                "q7_autre_precision": q7_autre,
                "q8_suggestions": q8_suggestions,
                "q8_autre_precision": q8_autre,
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
