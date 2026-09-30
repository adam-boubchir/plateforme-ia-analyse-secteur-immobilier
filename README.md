Oui. Pour ton projet, je te conseille un README **professionnel mais réaliste**, qui présente l'architecture actuelle sans prétendre que les fonctionnalités encore en développement sont terminées.

Tu peux copier directement le contenu ci-dessous dans `README.md`.

````markdown
# 🏠 Plateforme IA d'Analyse du Secteur Immobilier

> Plateforme intelligente d'analyse des données du secteur immobilier et des matériaux de construction, basée sur l'IA générative, le Text-to-SQL, l'analyse de données et la prédiction temporelle.

---

## 📌 Présentation

La **Plateforme IA d'Analyse du Secteur Immobilier** est une solution développée dans le cadre d'un projet académique et d'un stage au sein du **Ministère**.

L'objectif principal est de permettre aux utilisateurs d'interroger et d'analyser des données du secteur immobilier et des matériaux de construction en utilisant le **langage naturel**, sans avoir besoin d'écrire directement des requêtes SQL.

L'utilisateur peut poser une question telle que :

> « Quels sont les matériaux de construction dont l'indice était supérieur à 150 en 2022 ? »

ou :

> « Prédis la valeur de cet indicateur pour les 3 prochaines années. »

La plateforme interprète la demande, sélectionne l'agent IA approprié, génère si nécessaire une requête SQL, récupère les données depuis la base du Ministère et retourne un résultat compréhensible par l'utilisateur.

---

# 🎯 Objectifs du projet

La plateforme vise principalement à :

- Simplifier l'accès aux données du secteur immobilier.
- Permettre l'interrogation des bases de données en langage naturel.
- Automatiser la génération de requêtes SQL.
- Exploiter plusieurs agents IA spécialisés.
- Analyser les données historiques.
- Effectuer des prévisions temporelles.
- Présenter les résultats sous une forme compréhensible.
- Préparer l'intégration future de tableaux de bord et d'analyses avancées.

---

# 🧠 Fonctionnement général

Le fonctionnement de la plateforme repose sur une architecture multi-agents.

Le flux général est le suivant :

```text
                         ┌─────────────────────┐
                         │       Utilisateur   │
                         └──────────┬──────────┘
                                    │
                                    │ Question en langage naturel
                                    ▼
                         ┌─────────────────────┐
                         │    Frontend React   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Orchestrator Agent  │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐  ┌─────────────┐  ┌─────────────┐
             │ SQL Agent  │  │ Prediction  │  │ Report Agent│
             │            │  │    Agent    │  │             │
             └─────┬──────┘  └──────┬──────┘  └──────┬──────┘
                   │                │                 │
                   ▼                ▼                 ▼
             SQL Server       Prophet / IA      Analyse / Rapport
                   │
                   ▼
          ┌───────────────────┐
          │ Données Ministère │
          │ SQL Server        │
          └───────────────────┘
````

---

# 🤖 Architecture multi-agents

La plateforme utilise plusieurs agents spécialisés.

## 1. Orchestrator Agent

L'**Orchestrator Agent** constitue le point d'entrée intelligent du système.

Il analyse la question de l'utilisateur et détermine quel agent doit traiter la demande.

Les catégories principales sont :

* `SQL`
* `CHAT`
* `PREDICTION`
* `REPORT`
* `DASHBOARD`
* `BENCHMARK`

Exemples :

| Question                                          | Agent            |
| ------------------------------------------------- | ---------------- |
| « Quel était le prix moyen en 2022 ? »            | SQL Agent        |
| « Prédit la valeur pour les 3 prochaines années » | Prediction Agent |
| « Génère un rapport sur ces résultats »           | Report Agent     |
| Question générale / conversation                  | Chat Agent       |

---

# 🗄️ SQL Agent

Le **SQL Agent** est responsable de l'interaction avec les données.

Son rôle est de :

1. Comprendre la question utilisateur.
2. Identifier les informations nécessaires.
3. Exploiter le contexte du schéma de la base.
4. Générer une requête SQL.
5. Valider la requête.
6. Exécuter la requête.
7. Transformer les résultats en réponse compréhensible.

### Exemple

Question :

```text
Quels sont les matériaux dont l'indice était supérieur à 150 en 2022 ?
```

Le SQL Agent peut générer une requête de ce type :

```sql
SELECT DISTINCT
    nm.nom AS material_name
FROM FACT_PRIX_INDICES f
INNER JOIN NIVEAU_MATERIAU nm
    ON f.id_niveau_mat = nm.id
WHERE f.annee = 2022
  AND f.indice > 150
ORDER BY material_name;
```

Le SQL est ensuite exécuté sur la base de données du Ministère.

---

# 🔮 Prediction Agent

Le **Prediction Agent** est dédié aux demandes de prévision.

Il intervient lorsqu'une question demande une estimation de valeurs futures.

Exemples :

```text
Prédit la valeur pour les 3 prochaines années.
```

```text
Quelle sera l'évolution de cet indicateur dans les prochaines années ?
```

## Pipeline de prédiction

```text
Question utilisateur
        │
        ▼
Orchestrator Agent
        │
        ▼
Prediction Agent
        │
        ▼
SQL Agent
        │
        ▼
Données historiques
        │
        ▼
PredictionRequestBuilder
        │
        ▼
FeatureBuilder
        │
        ▼
ModelSelector
        │
        ▼
PredictionEngine
        │
        ▼
Prophet
        │
        ▼
PredictionAnalyzer
        │
        ▼
PredictionFormatter
        │
        ▼
Résultat final
```

Le Prediction Agent utilise les données historiques récupérées depuis la base de données.

Le modèle de séries temporelles actuellement utilisé est :

* **Prophet**

Le système calcule également des informations d'analyse telles que :

* tendance ;
* variation absolue ;
* variation en pourcentage ;
* intervalles de confiance.

---

# 📊 Report Agent

Le **Report Agent** est destiné à produire des synthèses et rapports à partir des résultats obtenus par la plateforme.

Il peut exploiter les résultats des analyses SQL afin de produire une présentation structurée des informations.

Le système applique notamment une règle importante :

> Les informations utilisées pour générer le rapport doivent provenir des données fournies au système et ne doivent pas être inventées.

---

# 💬 Chat Agent

Le **Chat Agent** permet de gérer les interactions conversationnelles qui ne nécessitent pas directement une interrogation de la base de données.

Il peut notamment traiter :

* les salutations ;
* les demandes d'aide ;
* les questions générales liées à l'utilisation de la plateforme.

---

# 🗃️ Sources de données

Les données exploitées par la plateforme proviennent principalement des données mises à disposition par le Ministère.

La base utilisée pour l'exécution des requêtes SQL est une base **SQL Server**.

Le système exploite notamment des données relatives à :

* prix et indices ;
* matériaux de construction ;
* ciment ;
* données territoriales ;
* données immobilières ;
* loyers ;
* cautions ;
* honoraires ;
* consommation de ciment.

> Les données réelles et les informations d'accès à la base ne sont pas incluses dans ce dépôt.

---

# 🏗️ Architecture technique

## Backend

Le backend est développé avec :

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **SQL Server**
* **Azure OpenAI**
* **Prophet**

## Frontend

Le frontend utilise notamment :

* **React**
* **TypeScript**
* **Axios**
* **Leaflet / OpenStreetMap**

## Intelligence artificielle

Les composants IA utilisent notamment :

* Azure OpenAI
* LLM pour le routage et le Text-to-SQL
* Prophet pour les prévisions temporelles

---

# 📁 Structure du projet

```text
plateforme-ia-analyse-secteur-immobilier/
│
├── agents/
│
├── backend/
│   │
│   ├── app/
│   │   ├── agents/
│   │   │   ├── sql_agent/
│   │   │   ├── prediction_agent/
│   │   │   ├── report_agent/
│   │   │   ├── chat_agent/
│   │   │   └── orchestrator/
│   │   │
│   │   ├── database/
│   │   ├── routers/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── requirements.txt
│   └── .env
│
├── database/
│
├── docs/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── storage/
│
├── .gitignore
├── package.json
├── package-lock.json
└── README.md
```

> Les fichiers générés automatiquement dans `backend/storage/` ne sont pas destinés à être versionnés.

---

# 🔐 Configuration

Les informations sensibles ne doivent pas être intégrées directement dans le code source.

Le backend utilise un fichier d'environnement :

```text
backend/.env
```

Exemple de variables utilisées :

```env
IMMO_AI_SERVER=localhost
IMMO_AI_DATABASE=IMMO_AI

MINISTRY_SERVER=localhost
MINISTRY_DATABASE=OBSERVATOIRE_STAGIAIRE

SQL_USERNAME=
SQL_PASSWORD=

AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_DEPLOYMENT=

PORT=8001
```

⚠️ **Les valeurs réelles des mots de passe, clés API et informations d'accès ne doivent pas être publiées dans un dépôt GitHub public.**

---

# ⚙️ Installation

## Prérequis

Avant de lancer le projet, installer :

* Python 3.10+
* Node.js
* npm
* SQL Server
* Git

Un accès aux bases de données nécessaires est également requis.

---

# 🚀 Installation du backend

Se placer dans le dossier backend :

```bash
cd backend
```

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer l'environnement sous Windows :

```powershell
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Configurer ensuite :

```text
backend/.env
```

avec les paramètres correspondant à l'environnement d'exécution.

---

# ▶️ Lancer le backend

Depuis le dossier `backend` :

```bash
uvicorn app.main:app --reload --port 8001
```

Le backend sera alors accessible sur :

```text
http://localhost:8001
```

La documentation interactive FastAPI est disponible sur :

```text
http://localhost:8001/docs
```

---

# 💻 Installation du frontend

Se placer dans le dossier frontend :

```bash
cd frontend
```

Installer les dépendances :

```bash
npm install
```

Lancer l'application :

```bash
npm run dev
```

---

# 🔄 Exemple de fonctionnement

### Question utilisateur

```text
Quels sont les matériaux dont l'indice était supérieur à 150 en 2022 ?
```

### Étape 1 — Orchestrator

Le système identifie une demande d'analyse de données historiques.

```text
SQL_AGENT
```

### Étape 2 — SQL Agent

Le SQL Agent génère une requête SQL adaptée au schéma de la base.

### Étape 3 — SQL Server

La requête est exécutée sur la base de données du Ministère.

### Étape 4 — Résultats

Les données retournées sont analysées et formatées.

### Étape 5 — Interface

Le frontend affiche le résultat à l'utilisateur.

---

# 🔮 Exemple de prédiction

Question :

```text
Prédit la valeur pour les 3 prochaines années.
```

Le système :

```text
Utilisateur
   ↓
Orchestrator
   ↓
Prediction Agent
   ↓
SQL Agent
   ↓
Données historiques
   ↓
Prophet
   ↓
Prévisions
   ↓
Analyse
   ↓
Réponse
```

---

# 🗺️ Analyse géographique

La plateforme prévoit également des fonctionnalités d'analyse territoriale permettant d'explorer les données selon différentes dimensions géographiques.

La visualisation cartographique utilise notamment :

* Leaflet
* OpenStreetMap
* données géographiques du Maroc

Les analyses peuvent être effectuées selon différents niveaux territoriaux disponibles dans les données.

---

# 📈 Visualisation

La plateforme est conçue pour présenter les résultats sous différentes formes :

* tableaux ;
* graphiques ;
* indicateurs ;
* cartes ;
* résultats de prédiction ;
* rapports.

Les graphiques générés automatiquement sont stockés localement dans :

```text
backend/storage/charts/
```

Les rapports générés sont stockés dans :

```text
backend/storage/reports/
```

Ces fichiers sont exclus du versionnement Git.

---

# 🧪 Tests

Les différents composants du système peuvent être testés indépendamment.

Exemples :

```bash
python test_prediction.py
```

Les tests permettent notamment de vérifier :

* le routage de l'Orchestrator ;
* la génération SQL ;
* l'exécution SQL ;
* le fonctionnement du Prediction Agent ;
* le fonctionnement de Prophet ;
* l'intégration entre les agents.

---

# 🛡️ Sécurité

Les informations sensibles doivent rester hors du dépôt Git.

Le projet utilise notamment :

```text
.env
```

pour les paramètres de configuration sensibles.

Le `.gitignore` exclut notamment :

```text
.env
*.zip
.vscode/
backend/storage/
```

Il est recommandé de ne jamais publier :

* clés API ;
* mots de passe ;
* tokens ;
* identifiants de bases de données ;
* fichiers de configuration contenant des secrets ;
* données confidentielles du Ministère.

---

# 📌 État actuel du projet

## Fonctionnalités disponibles

* [x] Architecture FastAPI
* [x] Architecture multi-agents
* [x] Orchestrator Agent
* [x] SQL Agent
* [x] Génération de requêtes SQL
* [x] Validation et exécution SQL
* [x] Connexion à SQL Server
* [x] Prediction Agent
* [x] Intégration de Prophet
* [x] Analyse des prévisions
* [x] Formatting des résultats
* [x] Chat Agent
* [x] Report Agent
* [x] Interface React
* [x] Visualisation cartographique
* [x] Gestion des graphiques et rapports

## Fonctionnalités en évolution

* [ ] Dashboard Agent
* [ ] Benchmarking Agent
* [ ] Amélioration de la précision du Text-to-SQL
* [ ] Optimisation des performances
* [ ] Amélioration des validations des données
* [ ] Enrichissement des visualisations
* [ ] Amélioration des fonctionnalités de prédiction

---

# 🛠️ Technologies utilisées

| Technologie   | Utilisation                     |
| ------------- | ------------------------------- |
| Python        | Backend et IA                   |
| FastAPI       | API backend                     |
| SQLAlchemy    | Accès aux bases de données      |
| SQL Server    | Données du Ministère            |
| Azure OpenAI  | Intelligence artificielle / LLM |
| Prophet       | Prévisions temporelles          |
| React         | Interface utilisateur           |
| TypeScript    | Développement frontend          |
| Axios         | Communication frontend/backend  |
| Leaflet       | Cartographie                    |
| OpenStreetMap | Données cartographiques         |
| Git           | Versionnement                   |
| GitHub        | Hébergement du code             |

---

# 🧩 Principes d'architecture

Le projet suit plusieurs principes :

### Séparation des responsabilités

Chaque agent possède une responsabilité spécifique.

```text
Orchestrator
     │
     ├── SQL Agent
     ├── Prediction Agent
     ├── Report Agent
     └── Chat Agent
```

### Séparation données / IA

Le LLM ne constitue pas la source de données.

Les données métier sont récupérées depuis les bases de données configurées.

### Séparation historique / prédiction

Le SQL Agent récupère les données historiques.

Le Prediction Agent utilise ensuite ces données pour construire la prévision.

Le SQL Agent n'effectue pas lui-même les calculs de prévision.

---

# 📚 Documentation

La documentation complémentaire du projet se trouve dans :

```text
docs/
```

Elle peut contenir notamment :

* architecture ;
* conception ;
* documentation technique ;
* diagrammes ;
* rapports ;
* documentation des agents ;
* procédures d'installation.

---

# 👥 Équipe

Projet réalisé dans le cadre du cycle ingénieur **Big Data & Intelligence Artificielle**.

### Membres

* Safaa Bouhouch
* Adam Boubchir

---

# 🏢 Contexte du projet

Projet réalisé dans le cadre d'un stage et d'un projet académique en collaboration avec le **Ministère**.

Le système est conçu pour faciliter l'exploitation et l'analyse des données liées au secteur immobilier et aux matériaux de construction.

---

# 📄 Licence

Ce projet est développé dans un cadre académique et professionnel.

Les données et ressources fournies par le Ministère peuvent être soumises à des restrictions d'utilisation et de diffusion.

La redistribution des données métier ou des informations confidentielles n'est pas autorisée sans l'accord des parties concernées.

---

# 📬 Contact

Pour toute information concernant le projet :

**Équipe Plateforme IA d'Analyse du Secteur Immobilier**

* Safaa Bouhouch
* Adam Boubchir

```

### ⚠️ Une chose que je modifierais avant de le mettre

Dans la section **État actuel**, j'ai volontairement mis certaines fonctionnalités comme « en évolution », parce que d'après l'état de votre projet, **Dashboard Agent et Benchmarking ne sont pas encore finalisés**. Il vaut mieux que le README GitHub reflète exactement ce qui est réellement disponible.

Et surtout, **ne mets pas dans le README les vraies valeurs de `SQL_PASSWORD`, `AZURE_OPENAI_*` ou autres secrets**. Le Ministère peut recevoir ces informations séparément dans son environnement de configuration.
```
