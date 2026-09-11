# -*- coding: utf-8 -*-
"""Construit la démonstration web autonome à partir du jeu synthétique.

L'application réelle est une interface Tkinter couplée à MySQL : elle ne peut pas
tourner dans un navigateur. Cette démonstration reproduit fidèlement son **cœur
analytique** — standardisation, ACP, distance euclidienne pondérée par la variance
expliquée — dans une page HTML autonome, embarquable dans un portfolio.

Ce qui est calculé ici, en Python, une fois pour toutes :
    - la standardisation (moyenne, écart-type) ajustée sur les expériences ;
    - l'ACP et ses composantes, ajustées sur les expériences seules ;
    - les charges factorielles du cercle des corrélations.

Ce qui est calculé dans le navigateur, à chaque déplacement d'un curseur :
    - la projection du point cible dans l'espace ACP déjà ajusté ;
    - la distance pondérée à chaque expérience, et le classement.

C'est exactement la séparation du logiciel : l'historique définit l'espace, le point
utilisateur y est projeté sans jamais l'influencer.

Usage :
    python scripts/generate_demo_experiments.py
    python scripts/build_demo.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Variables soumises à l'ACP, avec leur libellé et leur unité.
FEATURES = [
    ("effort_resultant", "Effort de coupe", "N"),
    ("temperature", "Température outil", "°C"),
    ("vb", "Usure en dépouille VB", "mm"),
    ("rugosite", "Rugosité Ra", "µm"),
    ("amplitude", "Amplitude vibratoire", "-"),
    ("temps_usinage", "Temps d'usinage", "min"),
]

TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aide à la décision — choix d'outil coupant</title>
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"></script>
<style>
  :root {
    --ink: #16201f; --muted: #5f6a68; --line: #d8ded9; --paper: #f6f7f4;
    --surface: #fff; --accent: #0d5e63; --accent-soft: #e2eeed; --target: #b4462f;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--paper); color: var(--ink);
    font: 15px/1.55 "Segoe UI", system-ui, -apple-system, Helvetica, Arial, sans-serif;
  }
  .wrap { max-width: 1240px; margin: 0 auto; padding: 22px 20px 40px; }
  header { border-bottom: 1.5px solid var(--ink); padding-bottom: 14px; margin-bottom: 20px; }
  h1 { font-size: clamp(20px, 3vw, 27px); margin: 0 0 6px; letter-spacing: -.01em; }
  .sub { color: var(--muted); max-width: 74ch; margin: 0; font-size: 14.5px; }
  .note {
    background: var(--accent-soft); border-left: 3px solid var(--accent);
    padding: 11px 14px; margin: 16px 0 22px; font-size: 13.5px; border-radius: 0 4px 4px 0;
  }
  .grid { display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 22px; align-items: start; }
  @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
  .panel { background: var(--surface); border: 1px solid var(--line); border-radius: 7px; padding: 16px 18px; }
  .panel h2 { font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 0 0 14px; }
  .field { margin-bottom: 15px; }
  .field label { display: flex; justify-content: space-between; font-size: 13.5px; margin-bottom: 5px; gap: 10px; }
  .field .val { font-variant-numeric: tabular-nums; font-weight: 600; color: var(--accent); white-space: nowrap; }
  input[type=range] { width: 100%; accent-color: var(--accent); }
  select { width: 100%; padding: 7px 9px; border: 1px solid var(--line); border-radius: 5px; background: #fff; font: inherit; }
  table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
  th { text-align: left; font-size: 11px; letter-spacing: .07em; text-transform: uppercase; color: var(--muted);
       padding: 8px 9px; border-bottom: 1px solid var(--line); white-space: nowrap; }
  td { padding: 8px 9px; border-bottom: 1px solid #eef1ee; }
  td.num { font-variant-numeric: tabular-nums; text-align: right; white-space: nowrap; }
  tr.top td { background: #f3f8f7; }
  .rank { display: inline-flex; width: 21px; height: 21px; align-items: center; justify-content: center;
          background: var(--accent); color: #fff; border-radius: 50%; font-size: 11.5px; font-weight: 700; }
  .charts { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 18px; }
  @media (max-width: 1050px) { .charts { grid-template-columns: 1fr; } }
  .tblwrap { overflow-x: auto; margin-top: 18px; }
  footer { margin-top: 26px; padding-top: 14px; border-top: 1px solid var(--line); color: var(--muted); font-size: 12.5px; }
  a { color: var(--accent); }
</style>
</head>
<body>
<div class="wrap">
  <header id="page-header">
    <h1>Aide à la décision — choix d'un outil coupant</h1>
    <p class="sub">Définissez une configuration d'usinage cible : l'application la projette dans
    l'espace des expériences historiques et classe les essais les plus proches.</p>
  </header>

  <p class="note" id="page-note">
    <strong>Démonstration sur données synthétiques.</strong> Les mesures du partenariat de recherche
    ne sont pas redistribuables. Les __N__ expériences utilisées ici sont générées selon les lois
    physiques de la coupe (Kienzle pour l'effort, Taylor pour l'usure, rugosité théorique).
    L'algorithme — standardisation, ACP, distance pondérée — est celui de l'application réelle.
  </p>

  <div class="grid">
    <div class="panel">
      <h2>Configuration cible</h2>
      <div class="field">
        <label for="procede">Procédé</label>
        <select id="procede"></select>
      </div>
      <div class="field">
        <label for="materiau">Matériau</label>
        <select id="materiau"></select>
      </div>
      <div id="sliders"></div>
    </div>

    <div>
      <div class="charts">
        <div class="panel"><div id="scatter" style="height:400px"></div></div>
        <div class="panel"><div id="circle" style="height:400px"></div></div>
      </div>

      <div class="panel tblwrap" style="margin-top:18px">
        <h2>Expériences les plus proches</h2>
        <table>
          <thead><tr>
            <th>#</th><th>Expérience</th><th>Procédé</th><th>Matériau</th><th>Revêtement</th>
            <th class="num">Vc</th><th class="num">fz</th><th class="num">Effort</th>
            <th class="num">T°</th><th class="num">Ra</th><th class="num">Distance</th>
          </tr></thead>
          <tbody id="ranking"></tbody>
        </table>
      </div>
    </div>
  </div>

  <footer>
    Cœur analytique de <a href="https://github.com/juleescourne/cutting-tool-recommender">cutting-tool-recommender</a>,
    reproduit dans le navigateur. L'application complète est un logiciel de bureau Python/Tkinter adossé à MySQL.
  </footer>
</div>

<script>
// Embarquée dans une iframe, la page est déjà présentée par son conteneur :
// on masque l'en-tête et l'avertissement pour ne pas les afficher deux fois.
if (window.self !== window.top) {
  document.documentElement.classList.add('embedded');
}
</script>
<style>
  .embedded #page-header, .embedded #page-note, .embedded footer { display: none; }
  .embedded .wrap { padding-top: 8px; }
</style>
<script>
const DATA = __DATA__;
const MODEL = __MODEL__;
const FEATURES = __FEATURES__;

const fmt = (v, d = 1) => Number(v).toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });

// --- Contrôles ---------------------------------------------------------------
const uniq = (k) => [...new Set(DATA.map(e => e[k]))].sort();
for (const [id, key] of [['procede', 'procede'], ['materiau', 'materiau']]) {
  const sel = document.getElementById(id);
  sel.innerHTML = '<option value="">Tous</option>' + uniq(key).map(v => `<option>${v}</option>`).join('');
  sel.addEventListener('change', update);
}

const slidersHost = document.getElementById('sliders');
FEATURES.forEach((f, i) => {
  const values = DATA.map(e => e[f.key]);
  const min = Math.min(...values), max = Math.max(...values);
  const step = (max - min) / 100;
  const div = document.createElement('div');
  div.className = 'field';
  div.innerHTML = `<label for="s${i}">${f.label}<span class="val" id="v${i}"></span></label>
                   <input type="range" id="s${i}" min="${min}" max="${max}" step="${step}" value="${MODEL.mean[i]}">`;
  slidersHost.appendChild(div);
  div.querySelector('input').addEventListener('input', update);
});

const target = () => FEATURES.map((f, i) => parseFloat(document.getElementById('s' + i).value));

// --- Algorithme : standardisation -> projection ACP -> distance ponderee ------
function project(vector) {
  const scaled = vector.map((v, i) => (v - MODEL.mean[i]) / MODEL.scale[i]);
  return MODEL.components.map(comp => comp.reduce((s, c, i) => s + c * scaled[i], 0));
}

function weightedDistance(a, b) {
  // Meme formule que utils.get_distance : ponderation par la variance expliquee.
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += MODEL.explained[i] * (a[i] - b[i]) ** 2;
  return Math.sqrt(sum);
}

function update() {
  const procede = document.getElementById('procede').value;
  const materiau = document.getElementById('materiau').value;
  const values = target();
  FEATURES.forEach((f, i) => {
    document.getElementById('v' + i).textContent = `${fmt(values[i], f.decimals)} ${f.unit}`;
  });

  const userPoint = project(values);
  const kept = DATA.filter(e => (!procede || e.procede === procede) && (!materiau || e.materiau === materiau));

  const ranked = kept
    .map(e => ({ e, d: weightedDistance(userPoint, e.pc) }))
    .sort((a, b) => a.d - b.d);

  // Nuage ACP
  Plotly.react('scatter', [
    {
      x: kept.map(e => e.pc[0]), y: kept.map(e => e.pc[1]),
      mode: 'markers', type: 'scatter', name: 'Expériences',
      marker: { size: 9, color: '#0d5e63', opacity: 0.45, line: { width: 0 } },
      text: kept.map(e => `${e.nom}<br>Vc ${e.vitesse_coupe} m/min · Ra ${e.rugosite} µm`),
      hovertemplate: '%{text}<extra></extra>'
    },
    {
      x: ranked.slice(0, 5).map(r => r.e.pc[0]), y: ranked.slice(0, 5).map(r => r.e.pc[1]),
      mode: 'markers', type: 'scatter', name: '5 plus proches',
      marker: { size: 14, color: '#0d5e63', line: { width: 2, color: '#fff' } },
      text: ranked.slice(0, 5).map(r => r.e.nom),
      hovertemplate: '%{text}<extra></extra>'
    },
    {
      x: [userPoint[0]], y: [userPoint[1]], mode: 'markers', type: 'scatter', name: 'Cible',
      marker: { size: 17, color: '#b4462f', symbol: 'x', line: { width: 3 } },
      hovertemplate: 'Configuration cible<extra></extra>'
    }
  ], {
    margin: { l: 52, r: 12, t: 42, b: 46 },
    title: { text: `Plan factoriel — ${fmt(MODEL.explained[0] * 100)} % + ${fmt(MODEL.explained[1] * 100)} % de variance`, font: { size: 13.5 } },
    xaxis: { title: `PC1 (${fmt(MODEL.explained[0] * 100)} %)`, zeroline: true, zerolinecolor: '#d8ded9', gridcolor: '#eef1ee' },
    yaxis: { title: `PC2 (${fmt(MODEL.explained[1] * 100)} %)`, zeroline: true, zerolinecolor: '#d8ded9', gridcolor: '#eef1ee' },
    paper_bgcolor: '#fff', plot_bgcolor: '#fff',
    legend: { orientation: 'h', y: -0.2, font: { size: 11.5 } }
  }, { displayModeBar: false, responsive: true });

  // Cercle des correlations
  const circleX = [], circleY = [];
  for (let a = 0; a <= 360; a += 4) { circleX.push(Math.cos(a * Math.PI / 180)); circleY.push(Math.sin(a * Math.PI / 180)); }
  const arrows = MODEL.loadings.map((l, i) => ({
    x: [0, l[0]], y: [0, l[1]], mode: 'lines+markers', type: 'scatter',
    name: FEATURES[i].label, line: { width: 2 },
    marker: { size: [0, 8] }, hovertemplate: `${FEATURES[i].label}<extra></extra>`
  }));
  Plotly.react('circle', [
    { x: circleX, y: circleY, mode: 'lines', type: 'scatter', line: { color: '#c9cec7', width: 1 }, hoverinfo: 'skip', showlegend: false },
    ...arrows
  ], {
    margin: { l: 52, r: 12, t: 42, b: 92 },
    title: { text: 'Cercle des corrélations', font: { size: 13.5 } },
    // constrain:'domain' empêche Plotly d'élargir la plage pour respecter le ratio :
    // sans cela le cercle unité est écrasé par la place prise par la légende.
    xaxis: { range: [-1.15, 1.15], constrain: 'domain', zeroline: true, zerolinecolor: '#d8ded9', gridcolor: '#eef1ee', title: 'PC1' },
    yaxis: { range: [-1.15, 1.15], constrain: 'domain', scaleanchor: 'x', zeroline: true, zerolinecolor: '#d8ded9', gridcolor: '#eef1ee', title: 'PC2' },
    paper_bgcolor: '#fff', plot_bgcolor: '#fff',
    legend: { orientation: 'h', y: -0.22, font: { size: 10.5 } }
  }, { displayModeBar: false, responsive: true });

  // Classement
  document.getElementById('ranking').innerHTML = ranked.slice(0, 8).map((r, i) => `
    <tr class="${i < 3 ? 'top' : ''}">
      <td><span class="rank">${i + 1}</span></td>
      <td>${r.e.nom}</td>
      <td>${r.e.procede}</td>
      <td>${r.e.materiau}</td>
      <td>${r.e.revetement}</td>
      <td class="num">${fmt(r.e.vitesse_coupe)}</td>
      <td class="num">${fmt(r.e.avance_dent, 3)}</td>
      <td class="num">${fmt(r.e.effort_resultant, 0)}</td>
      <td class="num">${fmt(r.e.temperature, 0)}</td>
      <td class="num">${fmt(r.e.rugosite, 2)}</td>
      <td class="num">${fmt(r.d, 3)}</td>
    </tr>`).join('') || '<tr><td colspan="11">Aucune expérience pour ce couple procédé / matériau.</td></tr>';
}

update();
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("demo/data.json"))
    parser.add_argument("--out", type=Path, default=Path("demo/index.html"))
    args = parser.parse_args()

    if not args.data.exists():
        parser.error(f"{args.data} introuvable — lancez d'abord scripts/generate_demo_experiments.py")

    experiments = json.loads(args.data.read_text(encoding="utf-8"))
    keys = [k for k, _, _ in FEATURES]
    matrix = np.array([[e[k] for k in keys] for e in experiments], dtype=float)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(matrix)

    pca = PCA(n_components=2)
    coords = pca.fit_transform(scaled)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    for experiment, coord in zip(experiments, coords):
        experiment["pc"] = [round(float(coord[0]), 4), round(float(coord[1]), 4)]

    decimals = {"vb": 3, "avance_dent": 3, "temps_usinage": 3, "rugosite": 2, "amplitude": 2}
    model = {
        "mean": [round(float(v), 6) for v in scaler.mean_],
        "scale": [round(float(v), 6) for v in scaler.scale_],
        "components": [[round(float(v), 6) for v in comp] for comp in pca.components_],
        "explained": [round(float(v), 6) for v in pca.explained_variance_ratio_],
        "loadings": [[round(float(v), 4) for v in row] for row in loadings],
    }
    features = [
        {"key": k, "label": label, "unit": unit, "decimals": decimals.get(k, 1)}
        for k, label, unit in FEATURES
    ]

    html = (TEMPLATE
            .replace("__DATA__", json.dumps(experiments, ensure_ascii=False))
            .replace("__MODEL__", json.dumps(model))
            .replace("__FEATURES__", json.dumps(features, ensure_ascii=False))
            .replace("__N__", str(len(experiments))))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8", newline="\n")

    total = sum(pca.explained_variance_ratio_) * 100
    print(f"Démonstration écrite dans {args.out} ({args.out.stat().st_size / 1024:.0f} Ko)")
    print(f"Variance expliquée par les 2 premiers axes : {total:.1f} %")
    for (key, label, _), row in zip(FEATURES, loadings):
        print(f"  {label:24} PC1 {row[0]:+.2f}   PC2 {row[1]:+.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
