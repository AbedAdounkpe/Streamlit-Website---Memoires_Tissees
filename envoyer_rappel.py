"""Envoi groupe (one-shot, local) d'un email de rappel aux participants.

Utilisation :
  1. Renseigne les adresses email dans « destinataires.txt » (une par ligne).
  2. Cree un mot de passe d'application Gmail :
     Compte Google > Securite > Validation en 2 etapes > Mots de passe des applications.
  3. Apercu (n'envoie rien) :
         python envoyer_rappel.py
  4. Envoi reel (le mot de passe d'application est demande de maniere securisee) :
         python envoyer_rappel.py --envoyer

Chaque participant reçoit un email individuel : personne ne voit les autres adresses.
"""

from __future__ import annotations

import argparse
import getpass
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

# --- Parametres de l'evenement (a ajuster si besoin) ---------------------------
NOM_EVENEMENT = "Tissus d'Afrique & memoires tissees"
DATE_EVENEMENT = "20 juin 2026"
LIEU_EVENEMENT = "Centre Andre Malraux, Rouen"
NOM_EXPEDITEUR = "Association Mikwabo"
# ------------------------------------------------------------------------------

DOSSIER = Path(__file__).resolve().parent
FICHIER_DESTINATAIRES = DOSSIER / "destinataires.txt"
MOTIF_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def lire_destinataires() -> list[str]:
    if not FICHIER_DESTINATAIRES.exists():
        sys.exit(
            f"Fichier introuvable : {FICHIER_DESTINATAIRES}\n"
            "Cree-le avec une adresse email par ligne."
        )

    emails: list[str] = []
    vus: set[str] = set()
    invalides: list[str] = []

    for ligne in FICHIER_DESTINATAIRES.read_text(encoding="utf-8").splitlines():
        valeur = ligne.strip()
        if not valeur or valeur.startswith("#"):
            continue
        # tolere les separateurs , ou ; sur une meme ligne
        for morceau in re.split(r"[,;]", valeur):
            email = morceau.strip().lower()
            if not email:
                continue
            if MOTIF_EMAIL.match(email):
                if email not in vus:
                    vus.add(email)
                    emails.append(email)
            else:
                invalides.append(email)

    if invalides:
        print("Adresses ignorees (format invalide) :")
        for email in invalides:
            print(f"  - {email}")

    return emails


def construire_message(expediteur: str, destinataire: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = "Rappel – Événement du 20 juin à Rouen"
    message["From"] = formataddr((NOM_EXPEDITEUR, expediteur))
    message["To"] = destinataire  # un seul destinataire par email (aucune adresse partagee)

    corps_texte = (
        "Bonjour,\n\n"
        "Toute l'équipe de l'association Mikwabo vous remercie pour votre "
        "inscription à Tissus d’Afrique et mémoires tissées.\n\n"
        "Nous avons le plaisir de vous donner rendez-vous le samedi 20 juin, de 13h à 18h, "
        "pour une après-midi placée sous le signe de la découverte, du partage et de la "
        "valorisation des patrimoines textiles africains.\n\n"
        "Afin de profiter pleinement du programme, nous vous invitons à arriver à l'heure.\n\n"
        "En cas d'empêchement de dernière minute, merci de bien vouloir nous en informer : "
        "vous permettrez ainsi à une autre personne de profiter de l'événement.\n\n"
        "Dans l'attente de vous accueillir, nous vous adressons nos salutations les plus cordiales.\n\n"
        "L'équipe de l'association Mikwabo"
    )

    corps_html = """\
<html>
  <body style="font-family: Arial, sans-serif; color: #1a1a1a; line-height: 1.5;">
    <p>Bonjour,</p>
    <p>Toute l'équipe de l'association Mikwabo vous remercie chaleureusement pour votre
       inscription à <strong>Tissus d’Afrique et mémoires tissées</strong>.</p>
    <p>Nous avons le plaisir de vous donner rendez-vous le
       <strong>samedi 20 juin, de 13h à 18h</strong>, pour une après-midi placée sous le signe
       de la découverte, du partage et de la valorisation des patrimoines textiles africains.</p>
    <p>Afin de profiter pleinement du programme, nous vous invitons à arriver à l'heure.</p>
    <p>En cas d'empêchement de dernière minute, merci de bien vouloir nous en informer :
       vous permettrez ainsi à une autre personne de profiter de l'événement.</p>
    <p>Dans l'attente de vous accueillir, nous vous adressons nos salutations les plus cordiales.</p>
    <p>L'équipe de l'association Mikwabo</p>
  </body>
</html>"""

    message.set_content(corps_texte)
    message.add_alternative(corps_html, subtype="html")
    return message


def envoyer(emails: list[str]) -> None:
    expediteur = input("Adresse Gmail expeditrice : ").strip()
    if not MOTIF_EMAIL.match(expediteur):
        sys.exit("Adresse expeditrice invalide.")
    mot_de_passe = getpass.getpass("Mot de passe d'application Gmail (saisie masquee) : ").strip()
    if not mot_de_passe:
        sys.exit("Mot de passe vide, abandon.")

    contexte = ssl.create_default_context()
    print("Connexion a Gmail...")
    envoyes = 0
    echecs: list[str] = []
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
        serveur.login(expediteur, mot_de_passe)
        for email in emails:
            try:
                # Un message distinct par destinataire : personne ne voit les autres adresses.
                serveur.send_message(construire_message(expediteur, email))
                envoyes += 1
                print(f"  envoye -> {email}")
            except Exception as erreur:  # noqa: BLE001
                echecs.append(email)
                print(f"  ECHEC  -> {email} ({erreur})")

    print(f"\nEmail de rappel envoye a {envoyes} participant(s) sur {len(emails)}.")
    if echecs:
        print("Echecs :")
        for email in echecs:
            print(f"  - {email}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Envoi d'un email de rappel aux participants.")
    parser.add_argument(
        "--envoyer",
        action="store_true",
        help="Envoie reellement les emails (sinon, simple apercu).",
    )
    args = parser.parse_args()

    emails = lire_destinataires()
    if not emails:
        sys.exit("Aucune adresse email valide trouvee dans destinataires.txt")

    print(f"\n{len(emails)} adresse(s) email valide(s) :")
    for email in emails:
        print(f"  - {email}")

    if not args.envoyer:
        print("\nApercu uniquement. Relance avec --envoyer pour envoyer reellement.")
        return

    confirmation = input(f"\nEnvoyer le rappel a ces {len(emails)} adresses ? (oui/non) : ").strip().lower()
    if confirmation not in {"oui", "o", "yes", "y"}:
        print("Annule.")
        return

    envoyer(emails)


if __name__ == "__main__":
    main()
