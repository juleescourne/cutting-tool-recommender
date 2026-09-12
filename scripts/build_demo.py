# -*- coding: utf-8 -*-
"""Construit la démonstration web autonome à partir du jeu synthétique.

L'application réelle est une interface Tkinter couplée à MySQL : elle ne peut pas
tourner dans un navigateur. Cette démonstration reproduit fidèlement son **cœur
analytique** — standardisation, ACP, distance euclidienne pondérée par la variance
expliquée — dans une page HTML autonome, embarquable dans un portfolio.

Ce qui est calculé ici, en Python, une fois pour toutes :
    - la standardisation (moyenne, écart-type) ajustée sur les expériences ;
    - l'ACP et ses composantes, ajustées sur les expériences seules ;
    - les corrélations entre mesures et les six axes de projection.

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

TEMPLATE = (Path(__file__).parent / 'demo_template.html').read_text(encoding='utf-8')


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

    pca = PCA(n_components=len(FEATURES))
    coords = pca.fit_transform(scaled)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    for experiment, coord in zip(experiments, coords):
        experiment["pc"] = [float(v) for v in coord]

    decimals = {"vb": 3, "avance_dent": 3, "temps_usinage": 3, "rugosite": 2, "amplitude": 2}
    model = {
        "mean": [float(v) for v in scaler.mean_],
        "scale": [float(v) for v in scaler.scale_],
        "components": [[float(v) for v in comp] for comp in pca.components_],
        "explained": [float(v) for v in pca.explained_variance_ratio_],
        "loadings": np.corrcoef(scaled.T, coords.T)[:len(FEATURES),len(FEATURES):].tolist(),
        "correlation": np.corrcoef(matrix.T).tolist(),
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

    total = sum(pca.explained_variance_ratio_[:2]) * 100
    print(f"Démonstration écrite dans {args.out} ({args.out.stat().st_size / 1024:.0f} Ko)")
    print(f"Variance expliquée par les 2 premiers axes : {total:.1f} %")
    for (key, label, _), row in zip(FEATURES, loadings):
        print(f"  {label:24} PC1 {row[0]:+.2f}   PC2 {row[1]:+.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
