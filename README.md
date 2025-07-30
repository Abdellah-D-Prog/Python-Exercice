# Scout API - Gestion de Scouts et Camps

Une API REST développée avec FastAPI pour la gestion de scouts et de camps de scoutisme.

## Description

Cette API permet de gérer :
- Scouts : Informations personnelles, âge, groupe
- Camps : Organisation des camps, localisation, participants

## Technologies utilisées

- FastAPI - Framework web moderne pour Python
- PostgreSQL - Base de données relationnelle
- psycopg2 - Connecteur PostgreSQL pour Python
- Uvicorn - Serveur ASGI
- Python-dotenv - Gestion des variables d'environnement

## Structure du projet

```
Python-Exercice/
├── index.py
├── routers/
│   ├── scoots.py
│   └── camps.py
├── database/
│   └── connection.py
├── .env
├── requirements.txt
└── README.md
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur

### Installation de PostgreSQL

Ubuntu/Debian :
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Configuration de la base de données

```bash
sudo -u postgres psql
CREATE DATABASE scoot;
CREATE USER scout WITH ENCRYPTED PASSWORD 'scout123';
GRANT ALL PRIVILEGES ON DATABASE scoot TO scout;
\q
```

### Installation des dépendances Python

```bash
cd Python-Exercice
pip install -r requirements.txt
```

### Configuration

Créer un fichier .env :
```
DB_HOST=localhost
DB_NAME=scoot
DB_USER=scout
DB_PASSWORD=scout123
DB_PORT=5432
```

## Démarrage

```bash
python index.py
```

L'API sera accessible sur http://localhost:8000

## Utilisation

- API : http://localhost:8000
- Documentation : http://localhost:8000/docs

### Endpoints

Scouts :
- GET /scoots/ - Lister tous les scouts
- GET /scoots/{id} - Obtenir un scout par ID
- POST /scoots/ - Créer un nouveau scout
- PUT /scoots/{id} - Modifier un scout
- DELETE /scoots/{id} - Supprimer un scout

Camps :
- GET /camps/ - Lister tous les camps
- GET /camps/{id} - Obtenir un camp par ID
- POST /camps/ - Créer un nouveau camp
- PUT /camps/{id} - Modifier un camp
- DELETE /camps/{id} - Supprimer un camp

## Dépannage

Vérifier PostgreSQL :
```bash
sudo systemctl status postgresql
```

Tester la connexion :
```bash
python database/connection.py
```

Corriger l'erreur de collation :
```bash
psql -h localhost -U scout -d scoot
ALTER DATABASE scoot REFRESH COLLATION VERSION;
```

## Structure de la base de données

Table camps :
- id, name, location, start_date, end_date, max_participants, created_at

Table scoots :
- id, name, firstname, age, group_name, camp_id, created_at