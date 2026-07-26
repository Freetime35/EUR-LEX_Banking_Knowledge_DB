1\. Vision

Objectif



Construire une base de connaissances juridique spécialisée dans la réglementation bancaire européenne à partir des données RDF publiées par EUR-Lex Cellar.



Le projet ne vise pas uniquement à télécharger des documents, mais à reconstruire un graphe de connaissances exploitable en Python.



2\. Principes

Source de vérité



La source unique est Cellar.



Cellar RDF

&#x20;     ↓

Knowledge Graph

&#x20;     ↓

Services

&#x20;     ↓

Applications



Aucune donnée métier n'est inventée.



Le Knowledge Graph est une représentation Python du RDF.



Architecture en couches

CLI

&#x20;│

&#x20;▼

Services

&#x20;│

&#x20;▼

KnowledgeGraph

&#x20;│

&#x20;▼

KnowledgeGraphBuilder

&#x20;│

&#x20;▼

RDF Parser (rdflib)

&#x20;│

&#x20;▼

CellarClient

&#x20;│

&#x20;▼

EUR-Lex Cellar



Chaque couche a une responsabilité unique.



3\. Modules

ekb/



&#x20;   connectors/

&#x20;       cellar.py



&#x20;   parsers/

&#x20;       rdf\_parser.py



&#x20;   builders/

&#x20;       knowledge\_graph\_builder.py



&#x20;   models/

&#x20;       document.py

&#x20;       eurovoc.py

&#x20;       procedure.py

&#x20;       event.py

&#x20;       manifestation.py

&#x20;       expression.py

&#x20;       official\_journal.py

&#x20;       relation.py

&#x20;       knowledge\_graph.py



&#x20;   services/



&#x20;   cli/

4\. Domaine



Le modèle métier est constitué d'entités.



Document



Représente un acte juridique.



Identifiants :



CELEX

Cellar UUID

ELI



Métadonnées :



titre

type

dates

langue

etc.

EuroVocConcept



Concept EuroVoc.



Exemple :



Banking supervision

Procedure



Procédure législative.



Event



Événement juridique.



Exemple :



adoption

publication

entrée en vigueur

modification

OfficialJournal



Publication au Journal officiel.



Manifestation



Version PDF, HTML, XML...



Expression



Version linguistique d'un document.



5\. Les relations



Les relations sont des objets métier.



Document



&#x20;   cites



Document

Document



&#x20;   amended\_by



Document

Document



&#x20;   published\_in



OfficialJournal

Document



&#x20;   has\_topic



EuroVocConcept



Une relation possède :



source

predicate

target



Le projet ne perd jamais cette information.



6\. KnowledgeGraph



Le cœur du projet.



KnowledgeGraph



documents



relations



procedures



events



concepts



official\_journals



expressions



manifestations



Toutes les recherches passent par cette structure.



7\. Builder



Le KnowledgeGraphBuilder transforme un rdflib.Graph en objets Python.



RDF



↓



rdflib.Graph



↓



KnowledgeGraphBuilder



↓



KnowledgeGraph



Le Builder est responsable de :



créer les objets

éviter les doublons

créer les relations

relier les objets

8\. Services



Les services ne lisent jamais directement le RDF.



Ils interrogent le KnowledgeGraph.



Exemple :



get\_document()



related\_documents()



documents\_about()



timeline()



dependencies()

9\. Roadmap

Phase 1

✅ HTTP

✅ Client Cellar

✅ Téléchargement RDF

Phase 2

RDF Parser (rdflib)

KnowledgeGraphBuilder

Documents

Relations

EuroVoc

Journaux officiels

Procédures

Événements

Expressions

Manifestations

Phase 3

Requêtes

Recherche

Navigation

Analyse d'impact

Visualisation du graphe

10\. Principes de développement



Quelques règles simples pour guider le projet :



Une responsabilité par classe (principe SRP).

Les modèles sont indépendants du RDF : ils représentent le domaine métier, pas la syntaxe XML.

Le Builder est le seul composant qui connaît la structure RDF.

Les identifiants CELEX, Cellar UUID et ELI sont conservés pour assurer la traçabilité avec la source.

Les relations sont des objets de premier niveau, au même titre que les documents.

Chaque ticket EKB enrichit le graphe, sans casser l'architecture existante.

Les tests unitaires s'appuient sur de vraies notices RDF, afin de garantir la compatibilité avec les données Cellar.

