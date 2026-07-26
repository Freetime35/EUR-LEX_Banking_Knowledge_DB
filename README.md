# EURLEX Knowledge DB

Base de connaissances réglementaire européenne spécialisée **Banque & Finance**.

Le projet construit un **Knowledge Graph** à partir des données RDF publiées par EUR-Lex Cellar afin de modéliser les documents juridiques, leurs relations, les concepts EuroVoc, les procédures, les événements et les publications officielles.

## Sprint 0

Cette version installe les fondations :

- CLI `ekb` ;
- configuration TOML ;
- SQLite + SQLAlchemy ;
- schéma initial des documents et identifiants ;
- diagnostic local avec `ekb doctor` ;
- initialisation de la base avec `ekb db init` ;
- premiers tests automatisés.

## Installation Windows (CMD)

```cmd
cd C:\chemin\vers\EURLEX_Knowledge_DB
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
copy config\settings.example.toml config\settings.toml
ekb --version
ekb doctor
ekb db init
pytest
```

## Commandes disponibles

```cmd
ekb --help
ekb --version
ekb doctor
ekb db init
ekb db status
ekb collection list
ekb collection seed
```

## Formats cibles

Pour chaque document, le projet cherchera à conserver, lorsqu'ils existent :

- HTML ;
- JSON de métadonnées ;
- PDF ;
- XML / Formex ;
- RDF.

Les sources brutes ne seront jamais modifiées.

## Documentation

- [Architecture](docs/architecture.md)
