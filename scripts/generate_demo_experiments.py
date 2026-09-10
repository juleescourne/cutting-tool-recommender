# -*- coding: utf-8 -*-
"""Génère un jeu d'expériences d'usinage synthétiques.

Les mesures expérimentales d'origine proviennent d'un partenariat de recherche et
ne sont pas redistribuables. Ce script produit un jeu de substitution qui respecte
la **structure** de la base et, surtout, les **relations physiques** entre
paramètres de coupe et mesures — sans quoi l'ACP et la recommandation par
similarité n'auraient aucun sens à démontrer.

Modèle physique simplifié
-------------------------
- Effort de coupe, loi de Kienzle :        Fc = kc1 · ap · fz^(1-mc)
- Rugosité théorique en tournage :        Ra ≈ fz² / (32 · r_eps)   (×1000 pour µm)
- Température : croît avec la vitesse de coupe et la dureté matière,
  atténuée par la lubrification (émulsion / MQL / cryogénie).
- Usure en dépouille VB, loi de Taylor :  VB ∝ (Vc/Vc_ref)^n · t^0.35,
  réduite par les revêtements.
- Vibration : amplifiée par l'élancement de l'outil et l'engagement radial.

Un bruit multiplicatif de 5 % est appliqué à chaque mesure, pour que les points ne
soient pas parfaitement alignés sur les lois — sinon l'ACP produirait une variance
concentrée à 100 % sur le premier axe.

Sorties
-------
- ``db/demo_data.sql``    : jeu chargeable dans MySQL
- ``demo/data.json``      : même jeu, consommé par la démo web autonome

Usage :
    python scripts/generate_demo_experiments.py [--experiments 60] [--seed 42]
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Référentiel matière -----------------------------------------------------
# kc1 : effort spécifique de coupe (N/mm²) ; durete : HB ; usinabilite : 1 = facile
MATERIAUX = {
    "42CrMo4":   {"kc1": 2100, "durete": 280, "usinabilite": 1.00, "type": "Acier"},
    "C45":       {"kc1": 1700, "durete": 200, "usinabilite": 1.25, "type": "Acier"},
    "316L":      {"kc1": 2350, "durete": 220, "usinabilite": 0.55, "type": "Inox"},
    "Ti6Al4V":   {"kc1": 1950, "durete": 340, "usinabilite": 0.30, "type": "Titane"},
    "AlSi7Mg":   {"kc1": 800,  "durete": 90,  "usinabilite": 2.60, "type": "Aluminium"},
    "Inconel718": {"kc1": 2700, "durete": 380, "usinabilite": 0.22, "type": "Superalliage"},
}

# Facteur de résistance à l'usure apporté par le revêtement
REVETEMENTS = {"Non revetu": 1.00, "TiN": 0.78, "TiAlN": 0.62, "AlCrN": 0.55, "Diamant": 0.40}

# Facteur d'évacuation thermique de l'assistance
ASSISTANCES = {"Sec": 1.00, "MQL": 0.84, "Emulsion": 0.72, "Cryogenie": 0.58}

PROCEDES = ["Fraisage", "Tournage", "Percage"]
TYPES_OUTIL = {"Fraisage": "Fraise", "Tournage": "Plaquette", "Percage": "Foret"}

MC = 0.25          # exposant de Kienzle
VC_REF = 120.0     # vitesse de coupe de référence (m/min)


def jitter(rng: random.Random, value: float, pct: float = 0.05) -> float:
    """Bruit multiplicatif, pour éviter des relations parfaitement déterministes."""
    return value * (1.0 + rng.gauss(0.0, pct))


def build_experiments(count: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    experiments = []

    for index in range(1, count + 1):
        procede = rng.choice(PROCEDES)
        materiau = rng.choice(list(MATERIAUX))
        props = MATERIAUX[materiau]
        revetement = rng.choice(list(REVETEMENTS))
        assistance = rng.choice(list(ASSISTANCES))

        # --- Paramètres de coupe, plage adaptée à l'usinabilité de la matière
        vc = rng.uniform(40, 320) * (0.45 + 0.55 * props["usinabilite"])
        vc = max(25.0, min(400.0, vc))
        fz = rng.uniform(0.04, 0.28)                 # avance par dent (mm/dent)
        ap = rng.uniform(0.3, 4.0)                   # profondeur de passe (mm)
        ae = rng.uniform(0.2, 1.0)                   # engagement radial (ratio)
        diametre = rng.choice([6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 25.0])
        nb_dents = rng.choice([2, 3, 4, 5, 6])
        rayon_arrete = rng.choice([0.2, 0.4, 0.8, 1.2])
        longueur_usinee = rng.uniform(20, 300)

        frequence_rotation = (vc * 1000.0) / (math.pi * diametre)   # tr/min
        vitesse_avance_min = fz * nb_dents * frequence_rotation      # mm/min
        temps_usinage = longueur_usinee / max(vitesse_avance_min, 1e-6)  # min

        # --- Effort de coupe : loi de Kienzle
        kc = props["kc1"] * (fz ** -MC)
        fc = kc * ap * fz * nb_dents * ae
        fx = jitter(rng, fc * 0.42)
        fy = jitter(rng, fc * 0.38)
        fz_force = jitter(rng, fc * 0.85)

        # --- Température : vitesse et dureté font monter, la lubrification fait baisser
        temperature = 90.0 + 1.35 * vc * (props["durete"] / 250.0) ** 0.6
        temperature *= ASSISTANCES[assistance]
        temperature = jitter(rng, temperature)

        # --- Usure en dépouille : Taylor, atténuée par le revêtement
        vb = 0.09 * (vc / VC_REF) ** 1.7 * (temps_usinage ** 0.35)
        vb *= REVETEMENTS[revetement] / max(props["usinabilite"], 0.2) ** 0.5
        vb = jitter(rng, vb)

        # --- Rugosité théorique, dégradée par l'usure de l'outil
        ra = (fz ** 2) / (32.0 * rayon_arrete) * 1000.0
        ra *= 1.0 + 2.2 * vb
        ra = jitter(rng, max(ra, 0.15))

        # --- Vibration : élancement outil et engagement radial
        amplitude = 0.6 + 3.4 * ae * (diametre / 20.0) ** -0.5 * (vc / VC_REF) ** 0.5
        amplitude = jitter(rng, amplitude)
        frequence_vib = jitter(rng, frequence_rotation * nb_dents / 60.0)

        # --- Sorties pièce
        durete_finale = jitter(rng, props["durete"] * (1.0 + 0.18 * vb))
        contrainte_residuelle = jitter(rng, -180.0 + 0.9 * temperature)
        limite_endurance = jitter(rng, 420.0 - 55.0 * ra)
        epaisseur_copeau = jitter(rng, fz * 1.35)

        experiments.append({
            "id": index,
            "nom": f"EXP-{index:03d} {procede[:4].upper()}-{materiau}",
            "procede": procede,
            "type_outil": TYPES_OUTIL[procede],
            "materiau": materiau,
            "type_matiere": props["type"],
            "revetement": revetement,
            "assistance": assistance,
            "vitesse_coupe": round(vc, 1),
            "avance_dent": round(fz, 4),
            "profondeur_passe": round(ap, 2),
            "engagement": round(ae, 3),
            "diametre": diametre,
            "nb_dents": nb_dents,
            "rayon_arrete": rayon_arrete,
            "longueur_usinee": round(longueur_usinee, 1),
            "frequence_rotation": round(frequence_rotation, 1),
            "vitesse_avance_min": round(vitesse_avance_min, 1),
            "temps_usinage": round(temps_usinage, 3),
            "fx": round(fx, 1),
            "fy": round(fy, 1),
            "fz": round(fz_force, 1),
            "effort_resultant": round(math.sqrt(fx * fx + fy * fy + fz_force * fz_force), 1),
            "temperature": round(temperature, 1),
            "vb": round(vb, 4),
            "rugosite": round(ra, 3),
            "amplitude": round(amplitude, 3),
            "frequence_vibration": round(frequence_vib, 1),
            "durete": round(durete_finale, 1),
            "contrainte_residuelle": round(contrainte_residuelle, 1),
            "limite_endurance": round(limite_endurance, 1),
            "epaisseur_copeau": round(epaisseur_copeau, 4),
        })

    return experiments


def sql_escape(value: str) -> str:
    return value.replace("'", "''")


def write_sql(experiments: list[dict], path: Path) -> None:
    lines: list[str] = []
    add = lines.append

    add("-- ============================================================================")
    add("-- demo_data.sql - jeu d'experiences d'usinage synthetiques")
    add("--")
    add(f"-- {len(experiments)} experiences generees par scripts/generate_demo_experiments.py")
    add("-- Les mesures respectent les lois physiques de la coupe (Kienzle, Taylor,")
    add("-- rugosite theorique) : l'ACP et la recommandation par similarite produisent")
    add("-- donc des resultats interpretables, contrairement a du bruit aleatoire.")
    add("--")
    add("-- Aucune mesure reelle du partenariat de recherche n'est redistribuee ici.")
    add("--")
    add("-- Usage :")
    add("--   mysql -u root -p < db/schema.sql")
    add("--   mysql -u root -p cutting < db/demo_data.sql")
    add("-- ============================================================================")
    add("")
    add("USE cutting;")
    add("")
    add("SET FOREIGN_KEY_CHECKS = 0;")
    for table in ("vibration", "usure_outil", "temperature_outil", "effort_outil",
                  "effort_piece", "temperature_piece", "sortie_piece", "copeaux",
                  "entree_outil", "entree_piece", "procede", "experience"):
        add(f"TRUNCATE TABLE {table};")
    add("SET FOREIGN_KEY_CHECKS = 1;")
    add("")

    add("INSERT INTO experience (id_experience, nom) VALUES")
    add(",\n".join(f"    ({e['id']}, '{sql_escape(e['nom'])}')" for e in experiments) + ";")
    add("")

    add("INSERT INTO procede (id_procede, type_procede, type_operation, assistance, "
        "vitesse_coupe, vitesse_avance_dent, vitesse_avance_min, profondeur_passe, "
        "engagement, frequence_rotation, id_experience) VALUES")
    add(",\n".join(
        f"    ({e['id']}, '{e['procede']}', 'Ebauche', '{e['assistance']}', "
        f"{e['vitesse_coupe']}, {e['avance_dent']}, {e['vitesse_avance_min']}, "
        f"{e['profondeur_passe']}, {e['engagement']}, {e['frequence_rotation']}, {e['id']})"
        for e in experiments) + ";")
    add("")

    add("INSERT INTO entree_piece (id_entree_piece, type_matiere, materiaux, "
        "procede_elaboration, longueur_usinee, num_passe, id_experience) VALUES")
    add(",\n".join(
        f"    ({e['id']}, '{e['type_matiere']}', '{e['materiau']}', 'Lamine', "
        f"{e['longueur_usinee']}, 1, {e['id']})" for e in experiments) + ";")
    add("")

    add("INSERT INTO entree_outil (id_entree_outil, type_outil, matiere, diametre, "
        "nb_dents_util, revetement, rayon_arrete, id_experience) VALUES")
    add(",\n".join(
        f"    ({e['id']}, '{e['type_outil']}', 'Carbure', {e['diametre']}, "
        f"{e['nb_dents']}, '{e['revetement']}', {e['rayon_arrete']}, {e['id']})"
        for e in experiments) + ";")
    add("")

    add("INSERT INTO sortie_piece (id_sortie_piece, rugosite, durete, limite_endurance, "
        "contrainte_residuelle, id_entree_piece) VALUES")
    add(",\n".join(
        f"    ({e['id']}, {e['rugosite']}, {e['durete']}, {e['limite_endurance']}, "
        f"{e['contrainte_residuelle']}, {e['id']})" for e in experiments) + ";")
    add("")

    add("INSERT INTO copeaux (id_copeaux, epaisseur, id_experience) VALUES")
    add(",\n".join(f"    ({e['id']}, {e['epaisseur_copeau']}, {e['id']})" for e in experiments) + ";")
    add("")

    # Séries temporelles : 3 points par expérience, suffisant pour les agrégats max
    add("-- Series temporelles : 3 releves par experience. L'application n'exploite")
    add("-- que les extrema, trois points suffisent donc a la demonstration.")
    add("INSERT INTO effort_outil (temps_effort_outil, fx, fy, fz, id_entree_outil) VALUES")
    rows = []
    for e in experiments:
        for k, factor in enumerate((0.82, 1.0, 0.91), start=1):
            rows.append(f"    ({k * 0.5}, {round(e['fx'] * factor, 1)}, "
                        f"{round(e['fy'] * factor, 1)}, {round(e['fz'] * factor, 1)}, {e['id']})")
    add(",\n".join(rows) + ";")
    add("")

    add("INSERT INTO temperature_outil (temps_temperature_outil, temperature_outil, id_entree_outil) VALUES")
    rows = []
    for e in experiments:
        for k, factor in enumerate((0.75, 1.0, 0.94), start=1):
            rows.append(f"    ({k * 0.5}, {round(e['temperature'] * factor, 1)}, {e['id']})")
    add(",\n".join(rows) + ";")
    add("")

    add("INSERT INTO usure_outil (temps_usinage, vb, Er, Kt, id_entree_outil) VALUES")
    rows = []
    for e in experiments:
        for k, factor in enumerate((0.35, 0.72, 1.0), start=1):
            rows.append(f"    ({round(e['temps_usinage'] * factor, 3)}, "
                        f"{round(e['vb'] * factor, 4)}, {round(e['vb'] * factor * 0.6, 4)}, "
                        f"{round(e['vb'] * factor * 0.4, 4)}, {e['id']})")
    add(",\n".join(rows) + ";")
    add("")

    add("INSERT INTO vibration (temps_vibration, frequence, amplitude, id_entree_piece, id_entree_outil) VALUES")
    rows = []
    for e in experiments:
        for k, factor in enumerate((0.88, 1.0, 0.79), start=1):
            rows.append(f"    ({k * 0.5}, {e['frequence_vibration']}, "
                        f"{round(e['amplitude'] * factor, 3)}, {e['id']}, {e['id']})")
    add(",\n".join(rows) + ";")
    add("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiments", type=int, default=60, help="nombre d'expériences (défaut : 60)")
    parser.add_argument("--seed", type=int, default=42, help="graine aléatoire (défaut : 42)")
    parser.add_argument("--sql", type=Path, default=Path("db/demo_data.sql"))
    parser.add_argument("--json", type=Path, default=Path("demo/data.json"))
    args = parser.parse_args()

    experiments = build_experiments(args.experiments, args.seed)

    write_sql(experiments, args.sql)
    print(f"{len(experiments)} expériences écrites dans {args.sql}")

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(experiments, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"Même jeu exporté pour la démo web dans {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
