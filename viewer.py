# -*- coding: utf-8 -*-
"""Visionneuse 3D (three.js) intégrée à Streamlit.

Charge un modèle .glb / .gltf dont les maillages portent le nom des structures
(export Z-Anatomy, BodyParts3D, Sketchfab...) et permet de :
  - tourner / zoomer / déplacer la vue,
  - cliquer une structure pour l'identifier,
  - isoler ou masquer des structures,
  - lancer un test « trouve la structure X » chronométré.
"""

HTML = r"""
<div id="racine">
  <div id="scene"></div>

  <aside id="panneau">
    <div class="bloc">
      <input id="recherche" type="text" placeholder="Rechercher une structure" autocomplete="off">
      <div id="compteur" class="discret">Aucun modèle chargé</div>
    </div>
    <ul id="liste"></ul>
    <div class="bloc bas">
      <button id="btn-test" class="primaire">Lancer un test</button>
      <button id="btn-reset">Recentrer la vue</button>
      <label class="ligne"><input id="opt-xray" type="checkbox"> Transparence</label>
    </div>
  </aside>

  <div id="etiquette"></div>
  <div id="consigne" class="cache"></div>
  <div id="vide">
    <h3>Aucun modèle 3D chargé</h3>
    <p>Dépose un fichier <code>.glb</code> dans le dossier <code>static/</code> de l'application,
       puis indique son nom dans la barre latérale. Le mode d'emploi est dans <code>LISEZMOI.md</code>.</p>
  </div>
</div>

<style>
  * { box-sizing: border-box; }
  #racine {
    position: relative; display: flex; height: __HAUTEUR__px; width: 100%;
    background: __FOND__; color: __TEXTE__; border: 1px solid __BORDURE__;
    border-radius: 10px; overflow: hidden;
    font-family: "IBM Plex Sans", -apple-system, Segoe UI, sans-serif;
  }
  #scene { flex: 1; position: relative; cursor: grab; }
  #scene:active { cursor: grabbing; }
  #panneau {
    width: 290px; border-left: 1px solid __BORDURE__; display: flex; flex-direction: column;
    background: __PANNEAU__;
  }
  .bloc { padding: 12px; border-bottom: 1px solid __BORDURE__; }
  .bloc.bas { border-bottom: none; border-top: 1px solid __BORDURE__; margin-top: auto; }
  #recherche {
    width: 100%; padding: 8px 10px; border-radius: 6px; border: 1px solid __BORDURE__;
    background: __FOND__; color: __TEXTE__; font-size: 13px;
  }
  #recherche:focus { outline: 2px solid __ACCENT__; outline-offset: 1px; }
  .discret { font-size: 11px; opacity: .65; margin-top: 8px; letter-spacing: .04em; text-transform: uppercase; }
  #liste { list-style: none; margin: 0; padding: 4px 0; overflow-y: auto; flex: 1; }
  #liste li {
    padding: 7px 12px; font-size: 13px; cursor: pointer; display: flex; gap: 8px; align-items: center;
    border-left: 3px solid transparent;
  }
  #liste li:hover { background: __SURVOL__; }
  #liste li.actif { border-left-color: __ACCENT__; background: __SURVOL__; font-weight: 600; }
  #liste li.masque { opacity: .35; text-decoration: line-through; }
  button {
    width: 100%; padding: 9px; margin-bottom: 8px; border-radius: 6px; cursor: pointer;
    border: 1px solid __BORDURE__; background: __FOND__; color: __TEXTE__; font-size: 13px;
    font-family: inherit;
  }
  button:hover { border-color: __ACCENT__; }
  button.primaire { background: __ACCENT__; color: #fff; border-color: __ACCENT__; }
  .ligne { display: flex; gap: 8px; align-items: center; font-size: 12px; opacity: .85; }
  #etiquette {
    position: absolute; pointer-events: none; padding: 5px 9px; border-radius: 5px;
    background: __ACCENT__; color: #fff; font-size: 12px; opacity: 0; transition: opacity .12s;
    max-width: 320px; z-index: 5;
  }
  #consigne {
    position: absolute; top: 14px; left: 14px; right: 304px; padding: 10px 14px; z-index: 4;
    background: __PANNEAU__; border: 1px solid __ACCENT__; border-radius: 8px; font-size: 14px;
  }
  #consigne b { color: __ACCENT__; }
  .cache { display: none !important; }
  #vide {
    position: absolute; inset: 0; margin-right: 290px; display: flex; flex-direction: column;
    align-items: center; justify-content: center; text-align: center; padding: 40px; gap: 4px;
  }
  #vide h3 { margin: 0; font-size: 16px; font-weight: 600; }
  #vide p { margin: 0; font-size: 13px; opacity: .7; max-width: 380px; line-height: 1.6; }
  code { background: __SURVOL__; padding: 1px 5px; border-radius: 4px; font-size: 12px; }
  @media (max-width: 700px) { #panneau { width: 190px; } #consigne { right: 204px; } }
</style>

<script type="importmap">
{ "imports": {
    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
} }
</script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const URL_MODELE = "__MODELE__";
const ACCENT = new THREE.Color("__ACCENT__");

const conteneur = document.getElementById('scene');
const etiquette = document.getElementById('etiquette');
const consigne  = document.getElementById('consigne');
const liste     = document.getElementById('liste');
const compteur  = document.getElementById('compteur');
const vide      = document.getElementById('vide');

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.01, 5000);
const rendu = new THREE.WebGLRenderer({ antialias: true, alpha: true });
rendu.setPixelRatio(Math.min(devicePixelRatio, 2));
conteneur.appendChild(rendu.domElement);

const controles = new OrbitControls(camera, rendu.domElement);
controles.enableDamping = true;
controles.dampingFactor = 0.08;

scene.add(new THREE.HemisphereLight(0xffffff, 0x404050, 2.2));
const lumiere = new THREE.DirectionalLight(0xffffff, 1.6);
lumiere.position.set(2, 4, 3);
scene.add(lumiere);
const contre = new THREE.DirectionalLight(0xffffff, 0.7);
contre.position.set(-3, -1, -2);
scene.add(contre);

function dimensionner() {
  const l = conteneur.clientWidth, h = conteneur.clientHeight;
  camera.aspect = l / h; camera.updateProjectionMatrix(); rendu.setSize(l, h);
}
new ResizeObserver(dimensionner).observe(conteneur);

let pieces = [], selection = null, vueInitiale = null;
let test = null; // { cible, score, essais }

function nettoyer(nom) {
  return (nom || 'Sans nom')
    .replace(/[_\.]/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/^(mesh|node|object)\s*/i, '')
    .trim();
}

if (URL_MODELE) {
  vide.classList.add('cache');
  compteur.textContent = 'Chargement…';
  new GLTFLoader().load(URL_MODELE, (gltf) => {
    scene.add(gltf.scene);
    gltf.scene.traverse((o) => {
      if (!o.isMesh) return;
      o.material = o.material.clone();
      o.userData.couleur = o.material.color ? o.material.color.clone() : new THREE.Color(0xcccccc);
      o.userData.libelle = nettoyer(o.name || (o.parent && o.parent.name));
      pieces.push(o);
    });
    cadrer(gltf.scene);
    construireListe();
    compteur.textContent = pieces.length + ' structures détectées';
  }, (p) => {
    if (p.total) compteur.textContent = 'Chargement ' + Math.round(p.loaded / p.total * 100) + ' %';
  }, () => {
    vide.classList.remove('cache');
    vide.querySelector('h3').textContent = 'Modèle introuvable';
    vide.querySelector('p').innerHTML = 'Vérifie le chemin du fichier : <code>' + URL_MODELE + '</code>';
    compteur.textContent = 'Échec du chargement';
  });
}

function cadrer(objet) {
  const boite = new THREE.Box3().setFromObject(objet);
  const taille = boite.getSize(new THREE.Vector3()).length();
  const centre = boite.getCenter(new THREE.Vector3());
  controles.target.copy(centre);
  camera.position.copy(centre).add(new THREE.Vector3(0, taille * 0.12, taille * 1.15));
  camera.near = taille / 500; camera.far = taille * 20; camera.updateProjectionMatrix();
  controles.update();
  vueInitiale = { pos: camera.position.clone(), cible: centre.clone() };
}

function construireListe(filtre = '') {
  const f = filtre.toLowerCase();
  liste.innerHTML = '';
  pieces
    .filter(p => p.userData.libelle.toLowerCase().includes(f))
    .slice(0, 800)
    .forEach(p => {
      const li = document.createElement('li');
      li.textContent = p.userData.libelle;
      li.className = (p === selection ? 'actif ' : '') + (p.visible ? '' : 'masque');
      li.onclick = () => { selectionner(p); viser(p); };
      li.oncontextmenu = (e) => { e.preventDefault(); p.visible = !p.visible; construireListe(filtre); };
      liste.appendChild(li);
    });
}

function selectionner(piece) {
  if (selection && selection.material.color) selection.material.color.copy(selection.userData.couleur);
  selection = piece;
  if (piece && piece.material.color) piece.material.color.copy(ACCENT);
  construireListe(document.getElementById('recherche').value);
}

function viser(piece) {
  const boite = new THREE.Box3().setFromObject(piece);
  const centre = boite.getCenter(new THREE.Vector3());
  const rayon = Math.max(boite.getSize(new THREE.Vector3()).length(), 0.001);
  controles.target.copy(centre);
  camera.position.copy(centre).add(new THREE.Vector3(rayon * 0.4, rayon * 0.6, rayon * 2.2));
  controles.update();
}

const rayon = new THREE.Raycaster();
const souris = new THREE.Vector2();

function pieceSousCurseur(evt) {
  const r = rendu.domElement.getBoundingClientRect();
  souris.x = ((evt.clientX - r.left) / r.width) * 2 - 1;
  souris.y = -((evt.clientY - r.top) / r.height) * 2 + 1;
  rayon.setFromCamera(souris, camera);
  const touches = rayon.intersectObjects(pieces.filter(p => p.visible), false);
  return touches.length ? touches[0].object : null;
}

rendu.domElement.addEventListener('pointermove', (e) => {
  const p = pieceSousCurseur(e);
  if (p && !test) {
    const r = conteneur.getBoundingClientRect();
    etiquette.style.left = (e.clientX - r.left + 14) + 'px';
    etiquette.style.top = (e.clientY - r.top + 14) + 'px';
    etiquette.textContent = p.userData.libelle;
    etiquette.style.opacity = 1;
  } else { etiquette.style.opacity = 0; }
});

let depart = null;
rendu.domElement.addEventListener('pointerdown', (e) => { depart = { x: e.clientX, y: e.clientY }; });
rendu.domElement.addEventListener('pointerup', (e) => {
  if (!depart || Math.hypot(e.clientX - depart.x, e.clientY - depart.y) > 4) return;
  const p = pieceSousCurseur(e);
  if (!p) return;
  if (test) repondre(p); else selectionner(p);
});

document.getElementById('recherche').oninput = (e) => construireListe(e.target.value);
document.getElementById('btn-reset').onclick = () => {
  if (!vueInitiale) return;
  camera.position.copy(vueInitiale.pos); controles.target.copy(vueInitiale.cible); controles.update();
  pieces.forEach(p => p.visible = true);
  construireListe(document.getElementById('recherche').value);
};
document.getElementById('opt-xray').onchange = (e) => {
  pieces.forEach(p => { p.material.transparent = e.target.checked; p.material.opacity = e.target.checked ? 0.45 : 1; });
};

const btnTest = document.getElementById('btn-test');
btnTest.onclick = () => { test ? arreterTest() : demarrerTest(); };

function demarrerTest() {
  if (!pieces.length) return;
  test = { score: 0, essais: 0, cible: null };
  btnTest.textContent = 'Arrêter le test';
  consigne.classList.remove('cache');
  etiquette.style.opacity = 0;
  question();
}
function arreterTest() {
  test = null; btnTest.textContent = 'Lancer un test'; consigne.classList.add('cache');
}
function question() {
  test.cible = pieces[Math.floor(Math.random() * pieces.length)];
  test.cible.visible = true;
  afficherConsigne('Clique sur : <b>' + test.cible.userData.libelle + '</b>');
}
function afficherConsigne(html) {
  const s = test ? ' &nbsp;·&nbsp; ' + test.score + ' / ' + test.essais : '';
  consigne.innerHTML = html + s;
}
function repondre(piece) {
  test.essais++;
  if (piece === test.cible) {
    test.score++;
    afficherConsigne('Trouvé : <b>' + piece.userData.libelle + '</b>');
    setTimeout(question, 900);
  } else {
    afficherConsigne('Non, c\'était <b>' + piece.userData.libelle + '</b>. Cherche encore : <b>' + test.cible.userData.libelle + '</b>');
  }
}

(function animer() {
  requestAnimationFrame(animer);
  controles.update();
  rendu.render(scene, camera);
})();
dimensionner();
</script>
"""


def html_viewer(modele_url: str, sombre: bool, hauteur: int = 620) -> str:
    palette = {
        "__FOND__": "#12141a" if sombre else "#ffffff",
        "__PANNEAU__": "#191c23" if sombre else "#f6f5f1",
        "__TEXTE__": "#ffffff" if sombre else "#000000",
        "__BORDURE__": "#2b3039" if sombre else "#dcd8ce",
        "__SURVOL__": "#22262f" if sombre else "#ebe8e0",
        "__ACCENT__": "#c2454a",
        "__MODELE__": modele_url or "",
        "__HAUTEUR__": str(hauteur),
    }
    sortie = HTML
    for cle_, valeur in palette.items():
        sortie = sortie.replace(cle_, valeur)
    return sortie
