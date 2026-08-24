# -*- coding: utf-8 -*-
"""Atlas — application de révision d'anatomie (crâne et dos).

Lancer avec :  streamlit run app.py
"""

import json
import random
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image

from data import PLANCHES, tous_les_labels, cle
from viewer import html_viewer

try:
    from streamlit_image_coordinates import streamlit_image_coordinates as clic_image
    CLIC_DISPO = True
except ImportError:
    CLIC_DISPO = False

RACINE = Path(__file__).parent
F_PROGRES = RACINE / "progression.json"
F_POINTS = RACINE / "reperes.json"
BOITES = 5  # système de Leitner

st.set_page_config(page_title="Atlas — révision d'anatomie", page_icon="🦴", layout="wide")

DOSSIER_MODELES = RACINE / "static"
F_CONFIG = RACINE / ".streamlit" / "config.toml"
CONFIG_ATTENDUE = """[server]
enableStaticServing = true
maxUploadSize = 400

[browser]
gatherUsageStats = false
"""


@st.cache_resource
def preparer_environnement():
    """Crée ce qui manque au premier lancement. Renvoie True si un redémarrage est nécessaire."""
    redemarrage = False
    try:
        DOSSIER_MODELES.mkdir(exist_ok=True)
        if not F_CONFIG.exists():
            F_CONFIG.parent.mkdir(exist_ok=True)
            F_CONFIG.write_text(CONFIG_ATTENDUE, encoding="utf-8")
            redemarrage = True
    except OSError:
        pass
    return redemarrage


BESOIN_REDEMARRAGE = preparer_environnement()


def modeles_disponibles():
    """Tous les .glb / .gltf trouvés dans le dépôt, sans configuration manuelle."""
    trouves = []
    for dossier in (DOSSIER_MODELES, RACINE, RACINE / "models"):
        if dossier.exists():
            for ext in ("*.glb", "*.gltf"):
                trouves += sorted(dossier.glob(ext))
    vus, uniques = set(), []
    for f in trouves:
        if f.name not in vus:
            vus.add(f.name)
            uniques.append(f)
    return uniques

# ------------------------------------------------- compatibilité des versions
def img(image):
    """st.image pleine largeur, quelle que soit la version de Streamlit."""
    try:
        st.image(image, width="stretch")
    except Exception:
        st.image(image, use_container_width=True)


def tableau(donnees):
    try:
        st.dataframe(donnees, width="stretch", hide_index=True)
    except Exception:
        st.dataframe(donnees, use_container_width=True, hide_index=True)


def bloc_html(code, hauteur):
    import streamlit.components.v1 as composants
    composants.html(code, height=hauteur, scrolling=False)



# ---------------------------------------------------------------- persistance
def charger(fichier):
    if fichier.exists():
        try:
            return json.loads(fichier.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def enregistrer(fichier, donnees):
    """Sauvegarde sur disque quand c'est possible.

    Sur un hébergement type Streamlit Cloud, le disque est éphémère ou en lecture
    seule : l'application continue alors de fonctionner avec la session en cours,
    et l'onglet Progrès propose d'exporter le fichier.
    """
    try:
        fichier.write_text(json.dumps(donnees, ensure_ascii=False, indent=1), encoding="utf-8")
        return True
    except OSError:
        st.session_state.disque_lecture_seule = True
        return False


if "progres" not in st.session_state:
    st.session_state.progres = charger(F_PROGRES)
if "points" not in st.session_state:
    st.session_state.points = charger(F_POINTS)


def fiche(k):
    return st.session_state.progres.setdefault(k, {"boite": 1, "vus": 0, "reussis": 0, "date": None})


def noter(k, reussi):
    f = fiche(k)
    f["vus"] += 1
    f["date"] = datetime.now().isoformat(timespec="seconds")
    if reussi:
        f["reussis"] += 1
        f["boite"] = min(BOITES, f["boite"] + 1)
    else:
        f["boite"] = 1
    enregistrer(F_PROGRES, st.session_state.progres)


# ---------------------------------------------------------------------- thème
def appliquer_theme(sombre):
    if sombre:
        fond, texte, panneau, bordure, doux = "#12141a", "#ffffff", "#191c23", "#2b3039", "#a7adba"
    else:
        fond, texte, panneau, bordure, doux = "#fbfaf7", "#000000", "#f2f0ea", "#dcd8ce", "#54595f"
    accent = "#c2454a"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Spectral:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
        .stApp {{ background: {fond}; }}
        .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div,
        .stMarkdown, .stRadio label, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {texte};
            font-family: 'IBM Plex Sans', -apple-system, sans-serif;
        }}
        .stApp h1, .stApp h2, .stApp h3 {{
            color: {texte}; font-family: 'Spectral', Georgia, serif; font-weight: 600; letter-spacing: -.01em;
        }}
        section[data-testid="stSidebar"] {{ background: {panneau}; border-right: 1px solid {bordure}; }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 2px; border-bottom: 1px solid {bordure}; }}
        .stTabs [data-baseweb="tab"] {{ color: {doux}; }}
        .stTabs [aria-selected="true"] {{ color: {texte}; border-bottom: 2px solid {accent}; }}
        .stButton button {{
            background: {fond}; color: {texte}; border: 1px solid {bordure}; border-radius: 6px;
            font-family: 'IBM Plex Sans', sans-serif;
        }}
        .stButton button:hover {{ border-color: {accent}; color: {texte}; }}
        .carte {{
            background: {panneau}; border: 1px solid {bordure}; border-left: 3px solid {accent};
            border-radius: 8px; padding: 18px 22px; margin: 6px 0;
        }}
        .carte .nom {{ font-family: 'Spectral', serif; font-size: 26px; line-height: 1.25; }}
        .carte .note {{ font-size: 15px; margin-top: 10px; color: {texte}; }}
        .eyebrow {{
            font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: {doux};
            margin-bottom: 2px;
        }}
        .pastille {{
            display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 999px;
            border: 1px solid {bordure}; color: {doux}; margin-right: 6px;
        }}
        code {{ color: {accent}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------- barre latérale
with st.sidebar:
    st.markdown("### Atlas")
    sombre = st.toggle("Mode sombre", value=True)
    st.divider()
    st.caption("Modèle 3D")
    trouves = modeles_disponibles()
    if trouves:
        noms = [f.name for f in trouves]
        choisi = st.selectbox("Modèle détecté", noms, label_visibility="collapsed")
        fichier_modele = choisi
    else:
        fichier_modele = ""
        st.caption("Aucun fichier .glb dans le dépôt.")
    url_saisie = st.text_input("Ou une URL .glb", value="", placeholder="https://…",
                               label_visibility="collapsed")
    depose = st.file_uploader("Charger un .glb", type=["glb", "gltf"], label_visibility="collapsed")
    if depose is not None:
        try:
            DOSSIER_MODELES.mkdir(exist_ok=True)
            (DOSSIER_MODELES / depose.name).write_bytes(depose.getbuffer())
            st.success(f"{depose.name} chargé.")
            fichier_modele = depose.name
        except OSError:
            st.error("Impossible d'écrire dans `static/` sur cet hébergement. Utilise plutôt une URL.")
    st.divider()
    total = len(tous_les_labels())
    acquis = sum(1 for f in st.session_state.progres.values() if f["boite"] >= 4)
    st.metric("Structures acquises", f"{acquis} / {total}")
    st.progress(acquis / total if total else 0)
    if st.button("Réinitialiser la progression"):
        st.session_state.progres = {}
        enregistrer(F_PROGRES, {})
        st.rerun()

appliquer_theme(sombre)

if url_saisie.strip().startswith("http"):
    url_modele = url_saisie.strip()
elif fichier_modele:
    url_modele = "/app/static/" + fichier_modele
else:
    url_modele = ""

if BESOIN_REDEMARRAGE:
    st.warning("Configuration créée au premier lancement. Redémarre l'application "
               "(ou clique sur *Reboot app* sur Streamlit Cloud) pour activer la vue 3D.")
if st.session_state.get("disque_lecture_seule"):
    st.info("Disque en lecture seule : ta progression reste en mémoire pendant la session. "
            "Exporte-la depuis l'onglet Progrès pour la conserver.")

st.markdown("<div class='eyebrow'>Crâne · Rachis · Muscles du dos</div>", unsafe_allow_html=True)
st.title("Atlas de révision")

onglets = st.tabs(["Vue 3D", "Planches", "Cartes", "Quiz", "Progrès"])


# ------------------------------------------------------------------- 1. Vue 3D
with onglets[0]:
    g, d = st.columns([3, 1])
    with g:
        st.markdown(
            "Fais tourner le modèle avec le clic gauche, zoome à la molette, déplace-toi au clic droit. "
            "Survole une pièce pour lire son nom, clique pour la sélectionner, clic droit dans la liste "
            "pour la masquer. Le bouton **Lancer un test** te demande de retrouver une structure au hasard."
        )
    with d:
        hauteur = st.select_slider("Hauteur", options=[480, 620, 760, 900], value=620)
    bloc_html(html_viewer(url_modele, sombre, hauteur), hauteur + 12)
    if not url_modele:
        st.caption("Dépose un fichier .glb depuis la barre latérale, ou colle l'URL d'un modèle "
                   "hébergé en ligne. Les autres onglets fonctionnent sans modèle 3D.")
    with st.expander("Où trouver un modèle 3D annoté ?"):
        st.markdown(
            """
Il te faut un fichier `.glb` dont **chaque maillage porte le nom de la structure** — c'est ce nom
que l'application affiche et utilise pour les tests.

- **Z-Anatomy** — atlas libre et complet (nomenclature latine), ouvre le `.blend` dans Blender puis
  *Fichier → Exporter → glTF 2.0*. Tu peux n'exporter que le crâne ou que les muscles du dos.
- **BodyParts3D / Life Science DB** — modèles libres par organe.
- **Sketchfab** — beaucoup de crânes téléchargeables ; vérifie que les pièces sont séparées et nommées.

Charge-le ensuite depuis la barre latérale : il est détecté automatiquement, sans configuration.
Un modèle de plus de ~150 Mo mettra du temps à s'afficher, et GitHub refuse les fichiers de plus
de 100 Mo — dans ce cas, héberge le `.glb` ailleurs et colle son URL.
            """
        )


# ------------------------------------------------------------------ 2. Planches
with onglets[1]:
    ids = list(PLANCHES.keys())
    pid = st.selectbox("Planche", ids, format_func=lambda i: PLANCHES[i]["titre"])
    planche = PLANCHES[pid]
    image = Image.open(RACINE / planche["image"])

    mode = st.radio(
        "Mode",
        ["Consulter", "Placer les repères", "Se tester sur l'image"],
        horizontal=True,
        help="Place d'abord les repères en cliquant sur l'image pour pouvoir te tester dessus.",
    )
    gauche, droite = st.columns([3, 2])

    with gauche:
        st.markdown(f"**{planche['titre']}** — {planche['sous_titre']}")
        if mode == "Consulter" or not CLIC_DISPO:
            img(image)
            if mode != "Consulter" and not CLIC_DISPO:
                st.info("Installe `streamlit-image-coordinates` pour cliquer sur l'image : "
                        "`pip install streamlit-image-coordinates`")
        else:
            largeur = 720
            apercu = image.copy()
            apercu.thumbnail((largeur, largeur * 2))
            clic = clic_image(apercu, key=f"clic_{pid}_{mode}")

            if mode == "Placer les repères":
                noms = [l["nom"] for l in planche["labels"]]
                choix = st.selectbox("Structure à situer", noms, key=f"pose_{pid}")
                k = cle(pid, choix)
                if clic:
                    st.session_state.points[k] = [clic["x"] / apercu.width, clic["y"] / apercu.height]
                    enregistrer(F_POINTS, st.session_state.points)
                deja = sum(1 for l in planche["labels"] if cle(pid, l["nom"]) in st.session_state.points)
                st.caption(f"{deja} / {len(noms)} repères placés sur cette planche."
                           + (" Position enregistrée." if k in st.session_state.points else ""))
            else:
                places = [l for l in planche["labels"] if cle(pid, l["nom"]) in st.session_state.points]
                if not places:
                    st.warning("Aucun repère placé sur cette planche. Passe d'abord en mode « Placer les repères ».")
                else:
                    if st.session_state.get("cible_planche") != pid or "cible" not in st.session_state:
                        st.session_state.cible = random.choice(places)["nom"]
                        st.session_state.cible_planche = pid
                    st.markdown(f"### Montre : *{st.session_state.cible}*")
                    if clic:
                        ref = st.session_state.points[cle(pid, st.session_state.cible)]
                        dx = clic["x"] / apercu.width - ref[0]
                        dy = clic["y"] / apercu.height - ref[1]
                        juste = (dx * dx + dy * dy) ** 0.5 < 0.045
                        noter(cle(pid, st.session_state.cible), juste)
                        if juste:
                            st.success("Exact.")
                        else:
                            st.error("À côté — la structure est ailleurs sur la planche.")
                        st.session_state.cible = random.choice(places)["nom"]
                    if st.button("Passer à une autre structure"):
                        st.session_state.cible = random.choice(places)["nom"]
                        st.rerun()

    with droite:
        filtre = st.text_input("Filtrer les légendes", key=f"f_{pid}")
        cats = sorted({l["cat"] for l in planche["labels"]})
        gardees = st.multiselect("Catégories", cats, default=cats, key=f"c_{pid}")
        st.caption(f"{len(planche['labels'])} légendes")
        for lab in planche["labels"]:
            if lab["cat"] not in gardees:
                continue
            if filtre and filtre.lower() not in lab["nom"].lower():
                continue
            f = fiche(cle(pid, lab["nom"]))
            with st.expander(f"{lab['nom']}  ·  boîte {f['boite']}"):
                st.markdown(f"<span class='pastille'>{lab['cat']}</span>", unsafe_allow_html=True)
                st.write(lab["note"] or "—")


# -------------------------------------------------------------------- 3. Cartes
with onglets[2]:
    labels = tous_les_labels()
    regions = ["Tout"] + sorted({l["region"] for l in labels})
    r = st.selectbox("Jeu de cartes", regions, key="deck")
    jeu = [l for l in labels if r == "Tout" or l["region"] == r]

    if not jeu:
        st.info("Aucune carte dans ce jeu.")
    else:
        def tirer():
            poids = [max(1, BOITES + 1 - fiche(cle(l["planche"], l["nom"]))["boite"]) for l in jeu]
            st.session_state.carte = random.choices(jeu, weights=poids, k=1)[0]
            st.session_state.retournee = False

        if "carte" not in st.session_state or st.session_state.get("deck_courant") != r:
            st.session_state.deck_courant = r
            tirer()

        c = st.session_state.carte
        k = cle(c["planche"], c["nom"])
        f = fiche(k)

        st.markdown(
            f"<div class='carte'><div class='eyebrow'>{c['titre']} · {c['cat']} · boîte {f['boite']}/{BOITES}</div>"
            f"<div class='nom'>{c['nom']}</div>"
            + (f"<div class='note'>{c['note']}</div>" if st.session_state.retournee else
               "<div class='note' style='opacity:.45'>Que retenir de cette structure ?</div>")
            + "</div>",
            unsafe_allow_html=True,
        )

        if not st.session_state.retournee:
            if st.button("Retourner la carte", type="primary"):
                st.session_state.retournee = True
                st.rerun()
        else:
            a, b, c3 = st.columns(3)
            if a.button("Je savais"):
                noter(k, True); tirer(); st.rerun()
            if b.button("À revoir"):
                noter(k, False); tirer(); st.rerun()
            if c3.button("Voir la planche"):
                img(Image.open(RACINE / PLANCHES[c["planche"]]["image"]))


# ---------------------------------------------------------------------- 4. Quiz
with onglets[3]:
    labels = [l for l in tous_les_labels() if l["note"]]
    regions = ["Tout"] + sorted({l["region"] for l in labels})
    rq = st.selectbox("Portée", regions, key="quiz_region")
    bassin = [l for l in labels if rq == "Tout" or l["region"] == rq]

    def nouvelle_question():
        bonne = random.choice(bassin)
        meme_cat = [l for l in bassin if l["cat"] == bonne["cat"] and l["nom"] != bonne["nom"]]
        autres = random.sample(meme_cat, k=min(3, len(meme_cat)))
        if len(autres) < 3:
            reste = [l for l in bassin if l["nom"] != bonne["nom"] and l not in autres]
            autres += random.sample(reste, k=3 - len(autres))
        sens = random.choice(["note_vers_nom", "nom_vers_note"])
        options = [bonne] + autres
        random.shuffle(options)
        st.session_state.q = {"bonne": bonne, "options": options, "sens": sens, "repondu": False}

    if "q" not in st.session_state or st.session_state.get("quiz_portee") != rq:
        st.session_state.quiz_portee = rq
        st.session_state.score = [0, 0]
        nouvelle_question()

    q = st.session_state.q
    bonne = q["bonne"]
    st.caption(f"Score : {st.session_state.score[0]} / {st.session_state.score[1]}")

    if q["sens"] == "note_vers_nom":
        st.markdown(f"#### Quelle structure correspond à cette description ?")
        st.markdown(f"*{bonne['note']}*")
        propositions = [o["nom"] for o in q["options"]]
        attendue = bonne["nom"]
    else:
        st.markdown(f"#### {bonne['nom']}")
        st.caption("Quelle description correspond ?")
        propositions = [o["note"] for o in q["options"]]
        attendue = bonne["note"]

    choix = st.radio("Réponses", propositions, index=None, key=f"rep_{id(q)}", label_visibility="collapsed")

    col_a, col_b = st.columns([1, 3])
    if col_a.button("Valider", type="primary", disabled=q["repondu"] or choix is None):
        juste = choix == attendue
        q["repondu"] = True
        st.session_state.score[1] += 1
        st.session_state.score[0] += 1 if juste else 0
        noter(cle(bonne["planche"], bonne["nom"]), juste)
        st.session_state.dernier_verdict = (juste, bonne)
        st.rerun()

    if q["repondu"] and "dernier_verdict" in st.session_state:
        juste, b = st.session_state.dernier_verdict
        if juste:
            st.success(f"Correct — {b['nom']}")
        else:
            st.error(f"La réponse était : {b['nom']}")
        st.caption(f"{b['titre']} · {b['cat']} — {b['note']}")
        if col_b.button("Question suivante"):
            nouvelle_question()
            st.rerun()


# ------------------------------------------------------------------ 5. Progrès
with onglets[4]:
    labels = tous_les_labels()
    lignes = []
    for pid, p in PLANCHES.items():
        boites = [fiche(cle(pid, l["nom"]))["boite"] for l in p["labels"]]
        lignes.append({
            "Planche": p["titre"],
            "Structures": len(boites),
            "Acquises (boîte ≥ 4)": sum(1 for b in boites if b >= 4),
            "À revoir (boîte 1)": sum(1 for b in boites if b == 1),
        })
    tableau(lignes)

    repartition = {f"Boîte {i}": 0 for i in range(1, BOITES + 1)}
    for l in labels:
        repartition[f"Boîte {fiche(cle(l['planche'], l['nom']))['boite']}"] += 1
    st.bar_chart(repartition)

    faibles = sorted(
        [l for l in labels if fiche(cle(l["planche"], l["nom"]))["vus"] > 0
         and fiche(cle(l["planche"], l["nom"]))["boite"] <= 2],
        key=lambda l: -fiche(cle(l["planche"], l["nom"]))["vus"],
    )[:15]
    st.markdown("#### Sauvegarde")
    a, b = st.columns(2)
    a.download_button(
        "Exporter ma progression",
        data=json.dumps({"progres": st.session_state.progres, "reperes": st.session_state.points},
                        ensure_ascii=False, indent=1),
        file_name="progression-atlas.json",
        mime="application/json",
    )
    reprise = b.file_uploader("Importer une sauvegarde", type=["json"], label_visibility="collapsed")
    if reprise is not None:
        try:
            contenu = json.loads(reprise.getvalue().decode("utf-8"))
            st.session_state.progres = contenu.get("progres", {})
            st.session_state.points = contenu.get("reperes", {})
            enregistrer(F_PROGRES, st.session_state.progres)
            enregistrer(F_POINTS, st.session_state.points)
            st.success("Sauvegarde restaurée.")
        except (ValueError, UnicodeDecodeError):
            st.error("Fichier illisible : attends-toi à un export produit par cette application.")

    st.markdown("#### Tes points faibles")
    if faibles:
        for l in faibles:
            f = fiche(cle(l["planche"], l["nom"]))
            st.markdown(f"- **{l['nom']}** — {f['reussis']}/{f['vus']} réussites · {l['titre']}")
    else:
        st.caption("Rien à signaler pour l'instant : réponds à quelques questions pour alimenter cette liste.")
