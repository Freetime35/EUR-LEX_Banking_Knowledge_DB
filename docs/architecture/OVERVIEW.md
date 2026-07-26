# Architecture générale

```text
CLI
  -> services applicatifs
    -> domaine
      -> dépôts / SQLAlchemy
        -> SQLite

connecteurs officiels
  -> Cellar / EUR-Lex metadata / ELI
  -> services de découverte et de collecte
```

## Flux prévu

1. Découverte des actes racines et classifications.
2. Résolution CELEX ↔ ELI ↔ Cellar.
3. Persistance du catalogue et des relations.
4. Téléchargement des manifestations disponibles.
5. Création des manifests et hashes.
6. Production d'une représentation canonique JSON.
