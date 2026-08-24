# -*- coding: utf-8 -*-
"""Quiz visuel d'anatomie — crâne et muscles du dos.

Lancer avec :  streamlit run quiz.py
Les 198 légendes des six planches sont ci-dessous ; l'application est tout en bas.
"""

OS = "Os"
SUTURE = "Suture"
ORIFICE = "Foramen / canal / fissure"
RELIEF = "Relief osseux"
CAVITE = "Cavité / sinus / sillon"
MUSCLE = "Muscle"
FASCIA = "Fascia / aponévrose"
REPERE = "Repère"


def L(nom, cat, note=""):
    return {"nom": nom, "cat": cat, "note": note}


PLANCHES = {
    "crane_face": {
        "titre": "Crâne — vue antérieure",
        "sous_titre": "Norma frontalis",
        "image": "images/crane_face.png",
        "region": "Tête",
        "labels": [
            L("Os frontal, écaille", OS, "Écaille verticale du front, ferme la boîte crânienne en avant."),
            L("Os nasal", OS, "Petit os pair formant le dos osseux du nez."),
            L("Os lacrymal", OS, "Le plus petit os de la face, paroi médiale de l'orbite, loge le sac lacrymal."),
            L("Os zygomatique", OS, "Pommette : relie maxillaire, frontal, sphénoïde et temporal."),
            L("Maxillaire", OS, "Os pair de la mâchoire supérieure, porte les dents supérieures."),
            L("Os pariétal, angle sphénoïdal", OS, "Angle antéro-inférieur du pariétal, s'articule avec la grande aile (ptérion)."),
            L("Vomer, septum nasal osseux", OS, "Lame impaire médiane, partie postéro-inférieure du septum nasal."),
            L("Cornets nasaux moyen et inférieur", OS, "Moyen = ethmoïde ; inférieur = os indépendant."),
            L("Grande aile", OS, "Grande aile du sphénoïde, visible au fond de l'orbite et sur la tempe."),
            L("Petite aile", OS, "Petite aile du sphénoïde, borde en haut la fissure orbitaire supérieure."),
            L("Face orbitaire de l'os frontal", OS, "Toit de l'orbite."),
            L("Face orbitaire de l'os sphénoïde", OS, "Paroi postéro-latérale de l'orbite (grande aile)."),
            L("Processus frontal de l'os maxillaire", RELIEF, "Montant du maxillaire qui remonte vers le frontal, borde le nez."),
            L("Processus zygomatique de l'os frontal", RELIEF, "Descend du frontal pour rejoindre l'os zygomatique (suture fronto-zygomatique)."),
            L("Processus alvéolaire du maxillaire", RELIEF, "Arc dentaire supérieur, contient les alvéoles."),
            L("Épine nasale antérieure", RELIEF, "Pointe médiane sous l'ouverture piriforme."),
            L("Bord supra-orbitaire", RELIEF, "Rebord supérieur de l'orbite (arcade sourcilière)."),
            L("Bord infra-orbitaire", RELIEF, "Rebord inférieur de l'orbite, formé par maxillaire + zygomatique."),
            L("Corps mandibulaire", OS, "Partie horizontale de la mandibule portant les dents inférieures."),
            L("Ramus mandibulaire", OS, "Branche montante verticale de la mandibule."),
            L("Suture internasale", SUTURE, "Entre les deux os nasaux, sur la ligne médiane."),
            L("Suture fronto-nasale", SUTURE, "Frontal / os nasal — point médian = nasion."),
            L("Suture fronto-maxillaire", SUTURE, "Frontal / processus frontal du maxillaire."),
            L("Suture fronto-lacrymale", SUTURE, "Frontal / os lacrymal, dans la paroi médiale de l'orbite."),
            L("Suture sphéno-frontale", SUTURE, "Grande + petite aile du sphénoïde / frontal."),
            L("Suture sphéno-pariétale", SUTURE, "Grande aile / pariétal — une des 4 sutures du ptérion."),
            L("Suture sphéno-zygomatique", SUTURE, "Grande aile / os zygomatique, paroi latérale de l'orbite."),
            L("Suture coronale", SUTURE, "Frontal / pariétaux, transversale au sommet du crâne."),
            L("Suture naso-maxillaire", SUTURE, "Os nasal / processus frontal du maxillaire."),
            L("Suture zygomatico-maxillaire", SUTURE, "Zygomatique / maxillaire, sous le rebord infra-orbitaire."),
            L("Foramen supra-orbitaire", ORIFICE, "Nerf et vaisseaux supra-orbitaires (V1)."),
            L("Foramen infra-orbitaire", ORIFICE, "Nerf infra-orbitaire (V2), à ~1 cm sous le rebord orbitaire."),
            L("Foramen mentonnier", ORIFICE, "Nerf mentonnier (V3), en regard de la 2e prémolaire."),
            L("Fissure orbitaire supérieure", ORIFICE, "Entre les deux ailes du sphénoïde : nerfs III, IV, V1, VI."),
            L("Fissure orbitaire inférieure", ORIFICE, "Entre grande aile et maxillaire : nerf infra-orbitaire (V2)."),
        ],
    },
    "crane_lateral": {
        "titre": "Crâne — vue latérale",
        "sous_titre": "Norma lateralis",
        "image": "images/crane_lateral.png",
        "region": "Tête",
        "labels": [
            L("Os pariétal", OS, "Grande voûte latérale du crâne, entre coronale, sagittale, lambdoïde et squameuse."),
            L("Os temporal (pars squamosa)", OS, "Écaille temporale, paroi de la fosse temporale."),
            L("Squama occipitalis (écaille occipitale)", OS, "Partie postérieure du crâne, en arrière de la suture lambdoïde."),
            L("Écaille de l'os frontal", OS, "Front, en avant de la suture coronale."),
            L("Ala major (grande aile)", OS, "Grande aile du sphénoïde, au centre du ptérion."),
            L("Os zygomaticum", OS, "Os zygomatique = pommette."),
            L("Maxilla", OS, "Maxillaire, mâchoire supérieure."),
            L("Os nasal", OS, "Dos osseux du nez."),
            L("Os lacrymal", OS, "Paroi médiale de l'orbite."),
            L("Lame orbitaire de l'os ethmoïde", OS, "Ancienne « lame papyracée », paroi médiale de l'orbite, très fine."),
            L("Arcus zygomaticus (arcade zygomatique)", RELIEF, "Pont osseux zygomatique + processus temporal ; passage du muscle temporal."),
            L("Fossa temporalis (fosse temporale)", CAVITE, "Dépression latérale où s'insère le muscle temporal."),
            L("Planum temporale", RELIEF, "Surface plane de l'écaille temporale, entre les lignes temporales."),
            L("Processus mastoideus", RELIEF, "Mastoïde : insertion du sterno-cléido-mastoïdien, contient les cellules mastoïdiennes."),
            L("Processus styloïde", RELIEF, "Fine épine du temporal, insertion du bouquet de Riolan."),
            L("Condyle occipital", RELIEF, "Surface d'articulation avec l'atlas (C1)."),
            L("Ligne temporale supérieure", RELIEF, "Insertion du fascia temporal."),
            L("Ligne temporale inférieure", RELIEF, "Insertion du muscle temporal."),
            L("Processus coronoïde de la mandibule", RELIEF, "Pointe antérieure du ramus : insertion du muscle temporal."),
            L("Processus condylaire de la mandibule", RELIEF, "Tête mandibulaire : articulation temporo-mandibulaire."),
            L("Base de la mandibule", RELIEF, "Bord inférieur du corps mandibulaire."),
            L("Corps mandibulaire", OS, "Partie horizontale dentée de la mandibule."),
            L("Protubérance mentonnière", RELIEF, "Menton osseux, propre à l'espèce humaine."),
            L("Épine nasale antérieure", RELIEF, "Pointe médiane sous l'ouverture piriforme."),
            L("Pore acoustique externe", ORIFICE, "Entrée du conduit auditif externe (os temporal)."),
            L("Foramen mentonnier", ORIFICE, "Sortie du nerf mentonnier sur la face latérale du corps mandibulaire."),
            L("Suture coronale", SUTURE, "Frontal / pariétal."),
            L("Suture squameuse", SUTURE, "Écaille du temporal / pariétal, en écaille de poisson."),
            L("Suture lambdoïde", SUTURE, "Pariétaux / occipital, en arrière."),
            L("Suture pariéto-mastoïdienne", SUTURE, "Pariétal / partie mastoïdienne du temporal."),
            L("Suture occipito-mastoïdienne", SUTURE, "Occipital / mastoïde."),
            L("Suture sphéno-frontale", SUTURE, "Grande aile / frontal."),
            L("Suture sphéno-squameuse", SUTURE, "Grande aile / écaille du temporal."),
            L("Suture sphéno-zygomatique", SUTURE, "Grande aile / zygomatique."),
            L("Suture fronto-zygomatique", SUTURE, "Frontal / zygomatique, angle latéral de l'orbite."),
            L("Suture temporo-zygomatique", SUTURE, "Processus temporal du zygomatique / processus zygomatique du temporal."),
            L("Suture naso-maxillaire", SUTURE, "Os nasal / maxillaire."),
            L("Suture lacrymo-maxillaire", SUTURE, "Os lacrymal / maxillaire."),
        ],
    },
    "crane_sagittal": {
        "titre": "Crâne — coupe sagittale médiane",
        "sous_titre": "Face interne de la base du crâne",
        "image": "images/crane_sagittal.png",
        "region": "Tête",
        "labels": [
            L("Crista galli", RELIEF, "Crête de l'ethmoïde, insertion de la faux du cerveau."),
            L("Lame criblée", ORIFICE, "Ethmoïde : passage des filets du nerf olfactif (I)."),
            L("Foramen caecum", ORIFICE, "Entre frontal et crista galli, veine émissaire inconstante."),
            L("Dos de la selle turcique", RELIEF, "Paroi postérieure de la loge hypophysaire (sphénoïde)."),
            L("Jugums cérébraux", RELIEF, "Reliefs de la face interne de la voûte moulés sur les gyri."),
            L("Impressions digitées", RELIEF, "Empreintes des circonvolutions cérébrales sur l'os."),
            L("Sillons artériels", CAVITE, "Gouttières de l'artère méningée moyenne sur la face interne."),
            L("Foramen émissaire pariétal", ORIFICE, "Veine émissaire pariétale, près de la suture sagittale."),
            L("Sinus frontal", CAVITE, "Cavité pneumatique dans l'écaille frontale."),
            L("Sinus sphénoïdal", CAVITE, "Cavité dans le corps du sphénoïde, sous la selle turcique."),
            L("Lame perpendiculaire de l'os ethmoïde", OS, "Partie supérieure du septum nasal osseux."),
            L("Vomer", OS, "Partie postéro-inférieure du septum nasal."),
            L("Crête nasale", RELIEF, "Sur le plancher nasal, reçoit le bord inférieur du vomer."),
            L("Canal incisif", ORIFICE, "Nerf naso-palatin et artère grande palatine, en avant du palais."),
            L("Foramen incisif", ORIFICE, "Ouverture buccale du canal incisif."),
            L("Alvéoles dentaires", CAVITE, "Loges osseuses des racines dentaires."),
            L("Fosse ptérygoïdienne", CAVITE, "Entre lames latérale et médiale du processus ptérygoïde ; muscle ptérygoïdien médial."),
            L("Hamulus ptérygoïdien", RELIEF, "Crochet de la lame médiale ; poulie du muscle tenseur du voile."),
            L("Incisure ptérygoïdienne", RELIEF, "Échancrure entre les deux lames ptérygoïdiennes."),
            L("Processus styloïde", RELIEF, "Épine du temporal."),
            L("Processus intrajugulaire", RELIEF, "Sépare les compartiments du foramen jugulaire."),
            L("Canal du n. hypoglosse", ORIFICE, "Nerf XII, au-dessus du condyle occipital."),
            L("Pore et méat acoustiques internes", ORIFICE, "Nerfs VII et VIII dans le rocher."),
            L("Apex du rocher", RELIEF, "Pointe antéro-médiale de la partie pétreuse du temporal."),
            L("Éminence arquée", RELIEF, "Relief du canal semi-circulaire antérieur sur le rocher."),
            L("Foramen mastoïdien", ORIFICE, "Veine émissaire mastoïdienne vers le sinus sigmoïde."),
            L("Sillon du sinus pétreux supérieur", CAVITE, "Le long du bord supérieur du rocher."),
            L("Sillon du sinus transverse", CAVITE, "Gouttière horizontale sur l'occipital."),
            L("Sillon du sinus sigmoïde", CAVITE, "Trajet en S vers le foramen jugulaire."),
            L("Planum occipital", RELIEF, "Partie de l'écaille occipitale au-dessus des lignes nuchales."),
            L("Protubérance occipitale externe", RELIEF, "Inion : repère palpable, insertion du ligament nuchal."),
            L("Partie squameuse de l'os temporal", OS, "Écaille du temporal."),
            L("Suture coronale", SUTURE, "Frontal / pariétal."),
            L("Suture squameuse", SUTURE, "Temporal / pariétal."),
            L("Suture lambdoïde", SUTURE, "Pariétal / occipital."),
            L("Os nasal", OS, "Dos osseux du nez."),
        ],
    },
    "dos_superficiel": {
        "titre": "Dos — plan superficiel",
        "sous_titre": "Trapèze, grand dorsal, deltoïde",
        "image": "images/dos_superficiel.png",
        "region": "Dos",
        "labels": [
            L("Muscle trapèze", MUSCLE, "Occiput → C7-T12 vers clavicule/scapula. Élève, sonne et adduit la scapula. N. accessoire (XI)."),
            L("Muscle grand dorsal", MUSCLE, "T7-sacrum + crête iliaque → sillon intertuberculaire. Adduction, rotation médiale, rétropulsion. N. thoraco-dorsal."),
            L("Muscle deltoïde", MUSCLE, "Clavicule/acromion/épine scapulaire → tubérosité deltoïdienne. Abduction du bras. N. axillaire."),
            L("Muscle sterno-cléido-mastoïdien", MUSCLE, "Sternum + clavicule → mastoïde. Inclinaison homolatérale, rotation controlatérale. N. XI."),
            L("Muscle splénius de la tête", MUSCLE, "Ligament nuchal + T1-T3 → mastoïde. Extension et rotation homolatérale de la tête."),
            L("Muscle splénius du cou", MUSCLE, "T3-T6 → tubercules postérieurs C1-C3."),
            L("Muscle semi-épineux de la tête", MUSCLE, "Processus transverses C4-T6 → écaille occipitale. Puissant extenseur de la tête."),
            L("Muscle élévateur de la scapula", MUSCLE, "C1-C4 → angle supérieur de la scapula. N. dorsal de la scapula."),
            L("Muscle petit rhomboïde", MUSCLE, "C7-T1 → bord médial de la scapula (au-dessus de l'épine)."),
            L("Muscle grand rhomboïde", MUSCLE, "T2-T5 → bord médial de la scapula. Adduction et sonnette médiale."),
            L("Muscle supra-épineux", MUSCLE, "Fosse supra-épineuse → tubercule majeur. Initie l'abduction. Coiffe des rotateurs."),
            L("Muscle petit rond", MUSCLE, "Bord latéral de la scapula → tubercule majeur. Rotation latérale. Coiffe des rotateurs."),
            L("Muscle grand rond", MUSCLE, "Angle inférieur de la scapula → lèvre médiale du sillon intertuberculaire. Rotation médiale."),
            L("Muscle dentelé postéro-supérieur", MUSCLE, "C7-T3 → côtes 2-5. Muscle inspirateur accessoire."),
            L("Muscle dentelé postéro-inférieur", MUSCLE, "T11-L2 → côtes 9-12. Abaisse les côtes (expiration)."),
            L("Muscle dentelé antérieur", MUSCLE, "Côtes 1-9 → bord médial de la scapula. Plaque la scapula sur le thorax. N. thoracique long."),
            L("Muscle érecteur du rachis", MUSCLE, "Masse commune lombaire → ilio-costal + longissimus + épineux. Extension du rachis."),
            L("Muscle oblique externe", MUSCLE, "Côtes 5-12 → crête iliaque et ligne blanche. Rotation controlatérale du tronc."),
            L("Muscle oblique interne", MUSCLE, "Crête iliaque + fascia thoraco-lombaire → côtes 10-12. Rotation homolatérale."),
            L("Muscle grand fessier", MUSCLE, "Ilion + sacrum → tractus ilio-tibial et tubérosité glutéale. Extenseur de hanche."),
            L("Fascia thoraco-lombaire", FASCIA, "Losange aponévrotique lombaire ; relie grand dorsal, transverse et obliques."),
            L("Fascia infra-épineux", FASCIA, "Recouvre le muscle infra-épineux dans la fosse infra-épineuse."),
            L("Fascia glutéal", FASCIA, "Recouvre le muscle moyen fessier."),
            L("Triangle cervical postérieur", REPERE, "Entre SCM, trapèze et clavicule ; contient le plexus brachial."),
            L("Triangle lombaire (de Petit)", REPERE, "Grand dorsal, oblique externe, crête iliaque : zone de faiblesse herniaire."),
            L("Ligne nuchale supérieure", REPERE, "Sur l'occipital : insertion trapèze, SCM, splénius."),
            L("Processus épineux de la vertèbre C2", REPERE, "Axis : première épineuse bifide palpable sous l'occiput."),
            L("Processus épineux de la vertèbre C7", REPERE, "Vertèbre proéminente : repère de comptage."),
            L("Processus épineux de la vertèbre T12", REPERE, "Charnière thoraco-lombaire."),
            L("Épine de la scapula", REPERE, "Sépare fosses supra- et infra-épineuse ; se prolonge par l'acromion."),
            L("Crête iliaque", REPERE, "Bord supérieur de l'ilion ; son sommet est en regard de L4."),
            L("12e côte", REPERE, "Côte flottante, repère de la loge rénale."),
        ],
    },
    "dos_intermediaire": {
        "titre": "Dos — muscle érecteur du rachis",
        "sous_titre": "Plan profond, colonnes latérale, intermédiaire et médiale",
        "image": "images/dos_intermediaire.png",
        "region": "Dos",
        "labels": [
            L("Muscle érecteur du rachis", MUSCLE, "3 colonnes : ilio-costal (latéral), longissimus (moyen), épineux (médial). « I Love Spaghetti » de dehors en dedans."),
            L("Muscle ilio-costal", MUSCLE, "Colonne la plus latérale, va de l'ilion aux côtes."),
            L("Muscle ilio-costal des lombes", MUSCLE, "Sacrum et crête iliaque → angles des côtes inférieures."),
            L("Muscle ilio-costal du thorax", MUSCLE, "Côtes inférieures → côtes supérieures."),
            L("Muscle ilio-costal du cou", MUSCLE, "Côtes 3-6 → processus transverses C4-C6."),
            L("Muscle longissimus", MUSCLE, "Colonne intermédiaire, la plus longue, du sacrum à la mastoïde."),
            L("Muscle longissimus du thorax", MUSCLE, "Masse commune → processus transverses et côtes."),
            L("Muscle longissimus du cou", MUSCLE, "T1-T5 → processus transverses C2-C6."),
            L("Muscle longissimus de la tête", MUSCLE, "T1-C4 → processus mastoïde. Extension et rotation homolatérale."),
            L("Muscle épineux", MUSCLE, "Colonne médiale, tendue d'épineuse à épineuse."),
            L("Muscle épineux du thorax", MUSCLE, "Épineuses T10-L2 → épineuses T2-T8."),
            L("Muscle épineux du cou", MUSCLE, "Épineuses C6-T2 → épineuses C2-C4."),
            L("Muscle semi-épineux de la tête", MUSCLE, "Transverses C4-T6 → écaille occipitale, entre les lignes nuchales."),
            L("Muscle petit droit postérieur de la tête", MUSCLE, "Tubercule postérieur de C1 → occipital. Triangle sous-occipital."),
            L("Muscle grand droit postérieur de la tête", MUSCLE, "Épineuse de C2 → occipital. Extension et rotation de la tête."),
            L("Muscle oblique supérieur de la tête", MUSCLE, "Transverse de C1 → occipital. Paroi du triangle sous-occipital."),
            L("Muscle oblique inférieur de la tête", MUSCLE, "Épineuse de C2 → transverse de C1. Rotation de l'atlas."),
            L("Muscles splénius de la tête et du cou", MUSCLE, "En « bandage » sur la nuque, recouvrent les muscles profonds."),
            L("Muscle dentelé postéro-supérieur", MUSCLE, "Inspirateur accessoire, sous les rhomboïdes."),
            L("Muscle dentelé postéro-inférieur", MUSCLE, "Expirateur accessoire, sous le grand dorsal."),
            L("Muscle transverse de l'abdomen", MUSCLE, "Fibres horizontales, le plus profond des muscles abdominaux ; sangle abdominale."),
            L("Aponévrose d'origine du muscle transverse de l'abdomen", FASCIA, "Naît du feuillet du fascia thoraco-lombaire."),
            L("Muscle oblique interne", MUSCLE, "Naît en partie du fascia thoraco-lombaire."),
            L("Muscle oblique externe (coupé)", MUSCLE, "Plan le plus superficiel des muscles latéraux de l'abdomen."),
            L("Fascia thoraco-lombaire", FASCIA, "Enveloppe l'érecteur du rachis, transmet les forces entre bassin et tronc."),
            L("Ligne nuchale supérieure", REPERE, "Limite supérieure des insertions nuchales."),
            L("Tubercule postérieur de l'atlas (C1)", REPERE, "Remplace l'épineuse sur C1."),
            L("Processus épineux de la vertèbre C7", REPERE, "Vertèbre proéminente."),
            L("Processus épineux de la vertèbre T12", REPERE, "Repère de la charnière thoraco-lombaire."),
            L("Crête iliaque", REPERE, "Origine de la masse commune de l'érecteur du rachis."),
            L("Érigne", REPERE, "Instrument de dissection qui écarte les plans — pas une structure anatomique."),
        ],
    },
    "dos_profond": {
        "titre": "Dos — plan profond (transversaires épineux)",
        "sous_titre": "Multifides, rotateurs, intertransversaires",
        "image": "images/dos_profond.png",
        "region": "Dos",
        "labels": [
            L("Muscles multifides", MUSCLE, "Transverse → épineuse en sautant 2-4 vertèbres. Stabilisateur segmentaire majeur du rachis."),
            L("Muscles rotateurs du cou (long et court)", MUSCLE, "Court : 1 vertèbre ; long : 2 vertèbres. Rotation controlatérale, proprioception."),
            L("Muscles rotateurs du thorax (long et court)", MUSCLE, "Les plus profonds des transversaires épineux, surtout thoraciques."),
            L("Muscle semi-épineux du thorax", MUSCLE, "Transverses T6-T10 → épineuses C6-T4, saute ~5 vertèbres."),
            L("Muscle semi-épineux de la tête", MUSCLE, "Le plus superficiel des transversaires épineux, extenseur de la tête."),
            L("Muscle interépineux du cou", MUSCLE, "Entre deux épineuses voisines, extension segmentaire."),
            L("Muscle interépineux des lombes", MUSCLE, "Entre épineuses lombaires adjacentes."),
            L("Muscle intertransversaire latéral", MUSCLE, "Entre processus transverses, inclinaison latérale."),
            L("Muscle élévateur de la côte", MUSCLE, "Transverse → côte sous-jacente, élève la côte (inspiration)."),
            L("Muscles élévateurs des côtes (long et court)", MUSCLE, "Court : côte suivante ; long : saute une côte."),
            L("Muscles intercostaux externes", MUSCLE, "Fibres obliques en bas et en avant, inspirateurs."),
            L("Muscle carré des lombes", MUSCLE, "Crête iliaque → 12e côte et transverses lombaires. Inclinaison latérale, fixe la 12e côte."),
            L("Muscle petit droit postérieur de la tête", MUSCLE, "Tubercule postérieur de C1 → occipital."),
            L("Muscle grand droit postérieur de la tête", MUSCLE, "Épineuse de C2 → occipital."),
            L("Muscle oblique supérieur de la tête", MUSCLE, "Transverse de C1 → occipital."),
            L("Muscle oblique inférieur de la tête", MUSCLE, "Épineuse de C2 → transverse de C1."),
            L("Muscle érecteur du rachis (coupé)", MUSCLE, "Sectionné pour dégager le plan des transversaires épineux."),
            L("Muscle transverse de l'abdomen et son aponévrose d'origine", MUSCLE, "S'attache au fascia thoraco-lombaire."),
            L("Fascia thoraco-lombaire (lame antérieure)", FASCIA, "En avant de l'érecteur, entre transverses lombaires et carré des lombes."),
            L("Fascia thoraco-lombaire (lame postérieure)", FASCIA, "En arrière de l'érecteur du rachis, très épaisse en lombaire."),
            L("Processus mastoïde", REPERE, "Insertion du longissimus de la tête et du splénius."),
            L("Tubercule postérieur de l'atlas (C1)", REPERE, "Insertion du petit droit postérieur."),
            L("Processus transverse de l'atlas (C1)", REPERE, "Le plus latéral des transverses cervicaux, palpable sous la mastoïde."),
            L("Processus épineux de l'axis (C2)", REPERE, "Insertion du grand droit postérieur et de l'oblique inférieur."),
            L("Processus épineux de la vertèbre C7", REPERE, "Vertèbre proéminente."),
            L("Crête iliaque", REPERE, "Insertion du carré des lombes et de la masse commune."),
        ],
    },
}


# ------------------------------------------------------------- QUIZ VISUEL --

import json
import random
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import streamlit as st
from PIL import Image, ImageDraw

try:
    from streamlit_image_coordinates import streamlit_image_coordinates as clic_image
except ImportError:
    st.error("Il manque une bibliothèque. Lance :  pip install streamlit-image-coordinates")
    st.stop()

RACINE = Path(__file__).parent
F_REPERES = RACINE / "reperes.json"
LARGEUR = 760          # largeur d'affichage des planches
TOLERANCE = 0.045      # rayon accepté autour du bon point, en fraction de largeur

st.set_page_config(page_title="Quiz anatomie", page_icon="🦴", layout="wide")


# ------------------------------------------------------------------ outillage
def charger_reperes():
    if F_REPERES.exists():
        try:
            return json.loads(F_REPERES.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def sauver_reperes():
    try:
        F_REPERES.write_text(json.dumps(st.session_state.reperes, ensure_ascii=False, indent=1),
                             encoding="utf-8")
    except OSError:
        st.session_state.hors_ligne = True


def simplifier(texte):
    """Compare les réponses sans tenir compte des accents, tirets et mots vides."""
    texte = unicodedata.normalize("NFD", texte.lower())
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    for mot in ("muscle ", "muscles ", "os ", "suture ", "foramen ", "processus ", "le ", "la ",
                "l'", "du ", "de ", "des ", "d'"):
        texte = texte.replace(mot, " ")
    for signe in "-–—,.()'":
        texte = texte.replace(signe, " ")
    return " ".join(texte.split())


def proximite(saisie, attendu):
    """Score de ressemblance, tolérant sur les compléments du type « , écaille »."""
    variantes = {attendu, attendu.split(",")[0], attendu.split("(")[0]}
    saisie_simple = simplifier(saisie)
    return max(SequenceMatcher(None, saisie_simple, simplifier(v)).ratio() for v in variantes)


@st.cache_data
def planche_affichee(chemin, largeur):
    image = Image.open(chemin).convert("RGB")
    hauteur = int(image.height * largeur / image.width)
    return image.resize((largeur, hauteur))


def avec_marqueur(image, x_rel, y_rel, couleur=(200, 30, 40)):
    """Copie de la planche avec une cible dessinée au point voulu."""
    copie = image.copy()
    d = ImageDraw.Draw(copie)
    x, y = x_rel * copie.width, y_rel * copie.height
    for r, ep in ((26, 4), (13, 3)):
        d.ellipse([x - r, y - r, x + r, y + r], outline=couleur, width=ep)
    d.line([x - 40, y, x - 32, y], fill=couleur, width=4)
    d.line([x + 32, y, x + 40, y], fill=couleur, width=4)
    d.line([x, y - 40, x, y - 32], fill=couleur, width=4)
    d.line([x, y + 32, x, y + 40], fill=couleur, width=4)
    return copie


def clic_neuf(cle_widget, resultat):
    """Vrai une seule fois par clic : évite qu'un rerun rejoue la même réponse."""
    if not resultat:
        return False
    signature = (cle_widget, resultat["x"], resultat["y"])
    if st.session_state.get("dernier_clic") == signature:
        return False
    st.session_state.dernier_clic = signature
    return True


# ------------------------------------------------------------------- démarrage
if "reperes" not in st.session_state:
    st.session_state.reperes = charger_reperes()
    st.session_state.score = [0, 0]
    st.session_state.erreurs = []

with st.sidebar:
    sombre = st.toggle("Mode sombre", value=True)
    st.divider()
    titres = {pid: p["titre"] for pid, p in PLANCHES.items()}
    pid = st.radio("Planche", list(PLANCHES), format_func=lambda i: titres[i])
    mode = st.radio("Mode", ["Placer les repères", "Nommer la structure", "Montrer la structure"])
    st.divider()
    places = sum(1 for k in st.session_state.reperes if k.startswith(pid + "::"))
    total_planche = len(PLANCHES[pid]["labels"])
    st.caption(f"Repères placés : {places} / {total_planche}")
    st.progress(places / total_planche)
    r, t = st.session_state.score
    st.caption(f"Score de la session : {r} / {t}")
    if st.button("Remettre le score à zéro"):
        st.session_state.score = [0, 0]
        st.session_state.erreurs = []
        st.rerun()
    st.download_button("Exporter mes repères",
                       data=json.dumps(st.session_state.reperes, ensure_ascii=False, indent=1),
                       file_name="reperes.json", mime="application/json")
    reprise = st.file_uploader("Importer des repères", type=["json"], label_visibility="collapsed")
    if reprise is not None:
        try:
            st.session_state.reperes.update(json.loads(reprise.getvalue().decode("utf-8")))
            sauver_reperes()
            st.success("Repères importés.")
        except (ValueError, UnicodeDecodeError):
            st.error("Fichier illisible.")

fond, texte = ("#111318", "#ffffff") if sombre else ("#ffffff", "#000000")
st.markdown(
    f"""<style>
    .stApp {{ background: {fond}; }}
    .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div,
    .stApp h1, .stApp h2, .stApp h3, .stMarkdown {{ color: {texte}; }}
    .stButton button, .stTextInput input {{ color: {texte}; }}
    </style>""",
    unsafe_allow_html=True,
)

planche = PLANCHES[pid]
image = planche_affichee(str(RACINE / planche["image"]), LARGEUR)
noms = [l["nom"] for l in planche["labels"]]
notes = {l["nom"]: l["note"] for l in planche["labels"]}
poses = [n for n in noms if f"{pid}::{n}" in st.session_state.reperes]


def point(nom):
    return st.session_state.reperes[f"{pid}::{nom}"]


def tirer(exclure=None):
    """Choisit la prochaine structure : les erreurs d'abord, une fois sur trois."""
    candidats = [n for n in poses if n != exclure] or poses
    ratees = [n for n in st.session_state.erreurs if n in candidats]
    if ratees and random.random() < 0.34:
        return random.choice(ratees)
    return random.choice(candidats)


def noter(nom, juste):
    st.session_state.score[1] += 1
    if juste:
        st.session_state.score[0] += 1
        st.session_state.erreurs = [e for e in st.session_state.erreurs if e != nom]
    elif nom not in st.session_state.erreurs:
        st.session_state.erreurs.append(nom)


# --------------------------------------------------------- 1. placer une fois
if mode == "Placer les repères":
    st.markdown(f"### {planche['titre']}")
    st.caption("Clique sur la structure demandée, à l'endroit où pointe sa ligne de rappel. "
               "Une fois placée, elle devient interrogeable dans les deux autres modes.")

    manquants = [n for n in noms if n not in poses]
    gauche, droite = st.columns([3, 2])
    with droite:
        if manquants:
            defaut = st.session_state.get("a_placer")
            index = manquants.index(defaut) if defaut in manquants else 0
            a_placer = st.selectbox("Structure à situer", manquants, index=index)
            st.session_state.a_placer = a_placer
            st.info(notes[a_placer])
        else:
            a_placer = None
            st.success("Toutes les structures de cette planche sont placées.")
        if poses:
            with st.expander(f"Repères déjà placés ({len(poses)})"):
                a_refaire = st.selectbox("Déplacer un repère", ["—"] + poses)
                if a_refaire != "—":
                    a_placer = a_refaire
                    st.caption(f"Clique pour repositionner : {a_refaire}")

    with gauche:
        vue = avec_marqueur(image, *point(a_placer)) if a_placer in poses else image
        resultat = clic_image(vue, key=f"pose_{pid}")
        if a_placer and clic_neuf(f"pose_{pid}", resultat):
            st.session_state.reperes[f"{pid}::{a_placer}"] = [resultat["x"] / image.width,
                                                              resultat["y"] / image.height]
            sauver_reperes()
            suivants = [n for n in noms if n not in poses and n != a_placer]
            st.session_state.a_placer = suivants[0] if suivants else None
            st.rerun()


# ------------------------------------- 2. on montre, tu écris le nom
elif mode == "Nommer la structure":
    if len(poses) < 1:
        st.warning("Place d'abord au moins une structure sur cette planche (mode « Placer les repères »).")
        st.stop()

    if st.session_state.get("cible_pid") != pid or "cible" not in st.session_state:
        st.session_state.cible_pid = pid
        st.session_state.cible = tirer()
        st.session_state.repondu = None

    cible = st.session_state.cible
    gauche, droite = st.columns([3, 2])
    with gauche:
        st.image(avec_marqueur(image, *point(cible)))
    with droite:
        st.markdown("### Quelle est cette structure ?")
        reponse = st.text_input("Ta réponse", key=f"saisie_{cible}",
                                placeholder="écris le nom…", label_visibility="collapsed")
        a, b = st.columns(2)
        if a.button("Valider", type="primary", disabled=not reponse or bool(st.session_state.get("repondu"))):
            score = proximite(reponse, cible)
            st.session_state.repondu = ("juste" if score >= 0.86 else
                                        "presque" if score >= 0.72 else "faux")
            noter(cible, score >= 0.86)
            st.rerun()
        if b.button("Je ne sais pas", disabled=bool(st.session_state.get("repondu"))):
            st.session_state.repondu = "abandon"
            noter(cible, False)
            st.rerun()

        verdict = st.session_state.get("repondu")
        if verdict == "juste":
            st.success(f"Correct — {cible}")
        elif verdict == "presque":
            st.warning(f"Presque : la formulation exacte est **{cible}**")
        elif verdict == "faux":
            st.error(f"C'était : **{cible}**")
        elif verdict == "abandon":
            st.info(f"C'est : **{cible}**")
        if verdict:
            st.caption(notes[cible])
            if st.button("Structure suivante", type="primary"):
                st.session_state.cible = tirer(exclure=cible)
                st.session_state.repondu = None
                st.rerun()


# ------------------------------------- 3. on donne le nom, tu montres où
else:
    if len(poses) < 1:
        st.warning("Place d'abord au moins une structure sur cette planche (mode « Placer les repères »).")
        st.stop()

    if st.session_state.get("cible2_pid") != pid or "cible2" not in st.session_state:
        st.session_state.cible2_pid = pid
        st.session_state.cible2 = tirer()
        st.session_state.verdict2 = None

    cible = st.session_state.cible2
    gauche, droite = st.columns([3, 2])
    with droite:
        st.markdown("### Montre-moi :")
        st.markdown(f"## {cible}")
        if st.session_state.get("verdict2") is None:
            st.caption("Clique sur la planche à l'endroit exact de cette structure.")
        else:
            juste, x, y = st.session_state.verdict2
            if juste:
                st.success("Bien placé.")
            elif juste is None:
                st.info("La cible rouge indique l'emplacement.")
            else:
                st.error("À côté — la cible rouge indique le bon endroit.")
            st.caption(notes[cible])
            if st.button("Structure suivante", type="primary"):
                st.session_state.cible2 = tirer(exclure=cible)
                st.session_state.verdict2 = None
                st.rerun()
        if st.button("Je ne sais pas", disabled=st.session_state.get("verdict2") is not None):
            bx, by = point(cible)
            st.session_state.verdict2 = (None, bx, by)
            noter(cible, False)
            st.rerun()

    with gauche:
        if st.session_state.get("verdict2") is None:
            resultat = clic_image(image, key=f"situe_{pid}")
            if clic_neuf(f"situe_{pid}", resultat):
                bx, by = point(cible)
                dx = resultat["x"] / image.width - bx
                dy = resultat["y"] / image.height - by
                juste = (dx * dx + dy * dy) ** 0.5 < TOLERANCE
                noter(cible, juste)
                st.session_state.verdict2 = (juste, bx, by)
                st.rerun()
        else:
            juste, bx, by = st.session_state.verdict2
            st.image(avec_marqueur(image, bx, by, (40, 150, 70) if juste else (200, 30, 40)))

if st.session_state.get("hors_ligne"):
    st.caption("Disque en lecture seule : pense à exporter tes repères depuis la barre latérale.")
