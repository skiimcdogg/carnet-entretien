# Carnet d'entretien auto

Ce projet permet de suivre les entretiens d'un véhicule via son historique.
Il permet aussi de savoir quand un entretien est à faire, tout au même endroit.

## Pourquoi ce projet
Ce projet existe aujourd'hui car, en tant qu'ancien mécanicien, je reconnais la valeur d'une application qui permet de se rappeler des entretiens à venir. Sans avoir à regarder sur un bout de papier, ses factures ou bien à devoir appeler son garage.

## Fonctionnalités

- Ajout des entretiens passés
- Vérification des entretiens à faire
- Un plan des entretiens disponibles pour un véhicule en fonction d'un type
- L'historique des entretiens est protégé par une règle qui empêche les entretiens erronés
- Récupération du dernier entretien effectué en fonction d'un type de maintenance
- 28 tests

## Règles métier

- Chaque type d'entretien a une règle : une limite en km, une limite en mois, ou les deux (ex : révision tous les 15 000 km ou 12 mois).
- Un entretien est dû quand les km parcourus **ou** le temps écoulé depuis le dernier entretien de ce type atteignent la limite. C'est le premier des deux qui compte.
- Si un entretien n'a jamais été fait, on compte depuis 0 km et la date de mise en circulation. Une voiture neuve n'est donc pas signalée trop tôt.
- Un entretien est refusé si ses km dépassent ceux du véhicule, ou si sa date est dans le futur.

## Stack technique
Python 3.15, pytest, ruff, uv

## Installation et tests
installer uv: docs.astral.sh/uv 
```bash
git clone https://github.com/skiimcdogg/carnet-entretien
cd carnet-entretien
uv sync
uv run pytest -vv
uv run uvicorn carnet_entretien.api.main:app --reload
```

## Prochaines étapes
Le but va être maintenant de mettre en place une base de données, permettre aussi de prévenir quand un entretien va arriver à échéance, l'API, le déploiement.