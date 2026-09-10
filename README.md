# Cutting Tool Recommender

[![Python checks](https://github.com/juleescourne/cutting-tool-recommender/actions/workflows/python-tests.yml/badge.svg)](https://github.com/juleescourne/cutting-tool-recommender/actions/workflows/python-tests.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-4479A1)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-lightgrey)](LICENSE)

Aide à la décision sur données d'usinage : archivage de campagnes d'essais dans une
base relationnelle, puis recherche des essais historiques les plus proches d'une
configuration de coupe visée, par analyse en composantes principales.

Développé avec le département Génie mécanique de l'**université de Tours**.

> Projet issu de mon portfolio Data — [juleescourne.github.io/portfolio-data-analyst](https://juleescourne.github.io/portfolio-data-analyst/)

![Démonstration interactive](docs/images/demo-acp.webp)

---

## Essayer sans rien installer

L'application est un logiciel de bureau Python/Tkinter adossé à MySQL : elle ne peut
pas tourner dans un navigateur. Son **cœur analytique** a donc été reproduit dans une
page autonome, embarquable et interactive.

```bash
pip install numpy scikit-learn
python scripts/generate_demo_experiments.py
python scripts/build_demo.py
```

Puis ouvrez `demo/index.html`. Les curseurs recalculent en direct la projection du
point cible et le classement des essais les plus proches.

---

## Le problème résolu

Une campagne d'essais d'usinage produit des centaines de relevés — efforts,
températures, usure, vibrations — pour chaque combinaison de matériau, d'outil et de
paramètres de coupe. Ces mesures finissent en classeurs Excel dispersés, et
l'expérience acquise n'est pas réexploitable.

L'application structure ces essais dans une base relationnelle, puis permet de
poser la question inverse : *pour cette configuration visée, quels essais déjà
réalisés s'en approchent le plus, et avec quel outil ont-ils été menés ?*

---

## Ce que le projet démontre

| Domaine | Éléments concrets |
| --- | --- |
| Modélisation relationnelle | 12 entités, séparation conditions d'essai / séries temporelles / résultats, clé composite sur les vibrations |
| Analyse de données | standardisation de grandeurs physiques hétérogènes, ACP, distance euclidienne pondérée par la variance expliquée |
| Rigueur méthodologique | ACP ajustée sur l'historique seul, point cible seulement projeté — jamais inclus dans l'ajustement |
| Ingénierie Python | architecture MVC, SQLAlchemy, requêtes paramétrées, `eval()` remplacé par un évaluateur restreint |
| Données physiques | générateur d'essais synthétiques respectant Kienzle, Taylor et la rugosité théorique |

---

## L'algorithme en bref

```mermaid
flowchart LR
    A[Filtrage<br/>procede + materiau] --> B[Agregation<br/>des series]
    B --> C[Standardisation]
    C --> D[ACP sur<br/>historique seul]
    D --> E[Projection<br/>du point cible]
    E --> F[Distance ponderee]
    F --> G[10 essais<br/>les plus proches]
```

Deux choix méthodologiques structurent le résultat :

**L'ACP est ajustée sur les seules expériences historiques.** Le point cible est
ensuite projeté dans cet espace figé. L'inclure dans l'ajustement le laisserait
influencer les axes servant à le comparer — le même principe qu'un `fit` réservé au
jeu d'entraînement.

**La distance est pondérée par la variance expliquée.** Un écart sur un axe
structurant pèse plus qu'un écart sur un axe résiduel, sans quoi les dernières
composantes — essentiellement du bruit — compteraient autant que la première.

Détail complet : [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Documentation

| Document | Contenu |
| --- | --- |
| [INSTALLATION.md](INSTALLATION.md) | démonstration en 1 minute, ou application complète avec MySQL |
| [UTILISATION.md](UTILISATION.md) | import des essais, tableau de bord, aide à la décision |
| [ARCHITECTURE.md](ARCHITECTURE.md) | modèle de données, chaîne analytique, interprétation des axes |

---

## Stack

`Python 3.10+` · `MySQL` · `SQLAlchemy 2` · `pandas` · `NumPy` · `scikit-learn`
· `Plotly` · `Dash` · `Tkinter` · `openpyxl` · `pytest` · `GitHub Actions`

---

## Données

Les mesures d'origine proviennent d'un partenariat de recherche et **ne sont pas
redistribuées**. Le dépôt fournit à la place un générateur d'essais synthétiques
respectant les lois physiques de la coupe :

| Grandeur | Loi |
| --- | --- |
| Effort de coupe | Kienzle |
| Usure en dépouille | Taylor, atténuée par le revêtement |
| Rugosité | rugosité théorique, dégradée par l'usure |
| Température | croissante avec Vc et la dureté, atténuée par la lubrification |

Sur ce jeu, les deux premiers axes de l'ACP portent **61,6 %** de la variance et
s'interprètent physiquement — ce que du bruit aléatoire n'aurait pas permis.

---

## Limites assumées

- **La qualité des recommandations n'est pas évaluée** : sans jeu de référence
  annoté, impossible de mesurer si les essais proposés sont les plus pertinents.
- Il s'agit d'une **recherche par similarité, pas d'un modèle prédictif** : aucune
  métrique de généralisation n'est à rapporter.
- Les mesures manquantes sont remplacées par une valeur neutre, ce qui rapproche
  artificiellement du centre les expériences incomplètes.
- Couverture de tests faible sur le moteur de recommandation.

---

## Licence

[MIT](LICENSE) — Jules Courné. Les données d'essai d'origine ne sont pas couvertes
par cette licence et ne sont pas incluses.
