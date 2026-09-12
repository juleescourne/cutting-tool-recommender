# Installation

Deux parcours possibles selon ce que vous voulez voir.

| Objectif | Temps | Prérequis |
| --- | --- | --- |
| **Voir la démonstration analytique** | 1 minute | Python seul |
| **Lancer l'application complète** | 15 minutes | Python + MySQL |

---

## Parcours rapide — la démonstration analytique

La démonstration reproduit le cœur du logiciel (ACP + recommandation par
similarité) dans une page web autonome, sans base de données ni interface bureau.

```bash
git clone https://github.com/juleescourne/cutting-tool-recommender.git
cd cutting-tool-recommender
pip install numpy scikit-learn

python scripts/generate_demo_experiments.py
python scripts/build_demo.py
```

Ouvrez ensuite `demo/index.html` dans un navigateur. Aucun serveur n'est requis.

---

## Parcours complet — l'application

### Prérequis

| Outil | Version | Vérifier |
| --- | --- | --- |
| Python | 3.10 ou supérieur | `python --version` |
| MySQL | 5.7 ou supérieur | `mysql --version` |
| Tkinter | fourni avec Python sous Windows et macOS | `python -c "import tkinter"` |

Sous Debian/Ubuntu, Tkinter s'installe séparément :

```bash
sudo apt install python3-tk
```

### 1. Environnement virtuel et dépendances

```bash
python -m venv .venv
source .venv/bin/activate          # .\.venv\Scripts\Activate.ps1 sous Windows
pip install -r requirements.txt
```

### 2. Créer la base

```bash
mysql -u root -p < db/schema.sql
```

Créez ensuite un utilisateur applicatif dédié — n'utilisez pas `root` :

```sql
CREATE USER 'cutting_user'@'localhost' IDENTIFIED BY 'votre-mot-de-passe';
GRANT ALL PRIVILEGES ON cutting.* TO 'cutting_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Configurer les identifiants

```bash
cp .env.example .env
```

Puis éditez `.env` :

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=cutting_user
DB_PASSWORD=votre-mot-de-passe
DB_NAME=cutting
SQLALCHEMY_ECHO=false
```

`.env` est exclu de Git et ne doit jamais être versionné.

### 4. Charger les expériences de démonstration

```bash
python scripts/generate_demo_experiments.py
mysql -u cutting_user -p cutting < db/demo_data.sql
```

360 expériences synthétiques, réparties sur 3 procédés et 6 matériaux.

### 5. Lancer

```bash
python main.py
```

---

## Vérifier l'installation

```bash
pip install -r requirements-dev.txt
pytest -q
```

Les tests couvrent la distance pondérée, la transformation d'efforts et
l'évaluateur d'expressions restreint — dont le refus d'exécuter du code arbitraire.

---

## Problèmes courants

**`ModuleNotFoundError: No module named 'tkinter'`**
Sous Linux, Tkinter n'est pas fourni par défaut : `sudo apt install python3-tk`.

**`Access denied for user`**
Les identifiants de `.env` ne correspondent pas à l'utilisateur MySQL créé à
l'étape 2. Vérifiez aussi que l'hôte est bien `localhost` et non `%`.

**`Unknown database 'cutting'`**
Le schéma n'a pas été chargé. Reprenez l'étape 2.

**« Aucune expérience correspondant au couple (procédé/matériau) »**
Message normal si la base est vide, ou si aucune expérience ne combine ce procédé
et ce matériau. Chargez les données de démonstration (étape 4).

**La fenêtre ne s'ouvre pas en session distante**
Tkinter a besoin d'un serveur graphique. En SSH, activez le déport X11 (`ssh -X`),
ou utilisez la démonstration web qui n'a aucune dépendance graphique.
