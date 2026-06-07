from pathlib import Path
from urllib.parse import quote_plus

import streamlit as st

st.set_page_config(
    page_title="Affiche & QR",
    page_icon="📌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# URL du site a ouvrir via QR code.
# Remplacez cette valeur par l'URL finale de votre site si besoin.
SITE_URL = "https://app-website---memoirestissees-7pgqjgjtebe5onpzpccntj.streamlit.app/"


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


IMAGE_PATH = trouver_image_evenement()

st.markdown(
    """
    <style>
        .stApp { background: #000000; }
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
        [data-testid="stAppViewContainer"] { padding-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

if IMAGE_PATH is None:
    st.error("Image introuvable : ajoutez une image dans le dossier assets")
    st.stop()

col_image, col_qr = st.columns([3, 2], gap="large")

with col_image:
    st.image(str(IMAGE_PATH), width=420)

with col_qr:
    qr_url = (
        "https://api.qrserver.com/v1/create-qr-code/"
        f"?size=800x800&margin=10&data={quote_plus(SITE_URL)}"
    )
    st.image(qr_url, width=300)
    st.markdown(
        """
        <p style="
            color: #FFFFFF;
            font-size: clamp(1.8rem, 3.2vw, 2.6rem);
            font-weight: 800;
            line-height: 1.15;
            margin-top: 1rem;
            margin-bottom: 0;
        ">
            Merci de nous partager vos avis sur cet événement !
        </p>
        """,
        unsafe_allow_html=True,
    )
