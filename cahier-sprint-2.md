# Carnet d'entretien auto : Sprint 2, l'API

> Ce document décrit **ce que l'API doit faire**, pas **comment** la coder.
> Les noms des fichiers, classes, fonctions et variables, c'est **toi** qui les choisis.
> Les **URL** de l'API, en revanche, font partie du besoin : ce sont elles que les autres utiliseront.
>
> Prérequis : Sprint 1 terminé (logique métier + 28 tests).

---

## 1. Le besoin en une phrase

Aujourd'hui, ton carnet d'entretien n'existe que dans du code Python. Le but du Sprint 2 : le rendre **utilisable depuis l'extérieur**, par une application mobile, un site web ou un autre programme, grâce à une **API**.

## 2. L'histoire

Paul veut une petite app sur son téléphone pour suivre sa Sandero.
Le développeur de l'app ne connaît pas Python. Tout ce qu'il veut, c'est des **URL** à appeler :
- « Voici ma voiture, enregistre-la. »
- « J'ai fait ma révision, note-la. »
- « Qu'est-ce que je dois faire en ce moment ? »

Ton API est ce **guichet** entre l'app et ta logique métier.

## 3. Le vocabulaire

| Mot | Ce que ça veut dire, simplement |
|---|---|
| **API** | Un guichet : on envoie une demande à une URL, on reçoit une réponse. |
| **Endpoint** | Une URL précise du guichet, associée à une action. |
| **Méthode HTTP** | Le type de demande : `GET` = lire, `POST` = créer, `DELETE` = supprimer… |
| **JSON** | Le format de texte qu'on échange. Ressemble à un dictionnaire Python. |
| **Code de statut** | Le nombre qui dit comment ça s'est passé : `200` OK, `201` créé, `404` introuvable, `422` données refusées. |
| **Schéma** | La forme attendue des données qui **entrent** et qui **sortent** de l'API. |
| **Identifiant (id)** | Un numéro ou code unique pour retrouver un véhicule précis. |
| **Persistance** | Garder les données même quand le programme s'arrête, dans une base de données. |

## 4. Le principe d'architecture : on ne touche pas au métier

Ton code du Sprint 1 est **le cœur**. L'API vient **autour**, comme une carrosserie autour d'un moteur.

```
[ App mobile / navigateur ]
          │  JSON
          ▼
┌─────────────────────┐
│   API (FastAPI)     │  ← reçoit les demandes, vérifie la forme, répond
├─────────────────────┤
│   Métier (Sprint 1) │  ← Vehicle, Maintenance, calcul… ON N'Y TOUCHE PAS
├─────────────────────┤
│   Stockage          │  ← garde les véhicules (mémoire, puis base de données)
└─────────────────────┘
```

**Règle d'or :** le métier ne connaît **ni** FastAPI, **ni** la base de données. Si demain on remplace l'API par une app en ligne de commande, le métier ne change pas d'une ligne.

**Conséquence :** tes 28 tests du Sprint 1 doivent rester verts **pendant tout le sprint**, sans modification.

## 5. Les endpoints

| # | Méthode | URL | Ce que ça fait | Réponse si OK |
|---|---|---|---|---|
| E1 | `GET` | `/health` | Vérifie que l'API tourne. | `200` |
| E2 | `POST` | `/vehicles` | Enregistre un nouveau véhicule. | `201` + le véhicule avec son id |
| E3 | `GET` | `/vehicles/{id}` | Renvoie un véhicule et son historique. | `200` |
| E4 | `GET` | `/vehicles` | Renvoie la liste des véhicules. | `200` |
| E5 | `POST` | `/vehicles/{id}/maintenances` | Ajoute un entretien à l'historique. | `201` |
| E6 | `PATCH` | `/vehicles/{id}/mileage` | Met à jour le kilométrage du véhicule. | `200` |
| E7 | `GET` | `/vehicles/{id}/due-maintenances` | Renvoie les types d'entretien dus. | `200` + liste |
| E8 | `DELETE` | `/vehicles/{id}` | Supprime un véhicule. | `204` |

## 6. Les règles de l'API

### Données
- **A1.** Un véhicule créé reçoit un **identifiant unique**, généré par l'API, jamais choisi par l'utilisateur.
- **A2.** Les données reçues sont vérifiées **avant** d'arriver au métier : champs manquants, mauvais type, type d'entretien inconnu… → `422`.
- **A3.** Le kilométrage ne peut pas être négatif → `422`.

### Erreurs
- **A4.** Un véhicule introuvable → `404`, avec un message clair.
- **A5.** Une règle métier refusée (R3, R3 bis du Sprint 1) → `422`, avec le message d'erreur du métier.
- **A6.** On ne renvoie **jamais** une erreur Python brute (une « stack trace ») à l'utilisateur.

### Date du jour
- **A7.** Rappel de R13 : le métier ne lit jamais l'horloge. C'est donc **l'API** qui lit la date du jour et la donne au métier.
- **A8.** E7 accepte une **date optionnelle** en paramètre. Sans date, on prend aujourd'hui. Avec une date, on peut demander « qu'est-ce qui sera dû au 1er janvier ? ». Bonus : ça rend l'endpoint facile à tester.

### Kilométrage
- **A9.** Le kilométrage d'un véhicule ne peut que **monter**. Une mise à jour vers un kilométrage plus bas est refusée → `422`. (Nouvelle règle métier : elle va dans le **métier**, pas dans l'API.)

### Plan d'entretien
- **A10.** Pour ce sprint, E7 utilise le **plan par défaut** du Sprint 1.

## 7. Exemples chiffrés (ce seront tes tests d'API)

| # | Demande | Réponse attendue |
|---|---|---|
| T1 | `GET /health` | `200` |
| T2 | `POST /vehicles` avec une Sandero valide | `201`, la réponse contient un id |
| T3 | `POST /vehicles` sans le champ kilométrage | `422` |
| T4 | `POST /vehicles` avec un kilométrage de -10 | `422` |
| T5 | `GET /vehicles/{id}` après T2 | `200`, on retrouve la Sandero |
| T6 | `GET /vehicles/{id}` avec un id qui n'existe pas | `404` |
| T7 | `POST .../maintenances` avec un entretien valide | `201`, l'entretien apparaît dans l'historique |
| T8 | `POST .../maintenances` avec des km supérieurs au véhicule | `422`, message du métier |
| T9 | `POST .../maintenances` avec un type d'entretien inventé | `422` |
| T10 | `PATCH .../mileage` de 50 000 à 60 000 | `200` |
| T11 | `PATCH .../mileage` de 50 000 à 40 000 | `422` (A9) |
| T12 | `GET .../due-maintenances?date=2026-10-30`, véhicule à 70 000 km, révision à 50 000 km | `200`, la révision annuelle est dans la liste |
| T13 | `DELETE /vehicles/{id}` puis `GET` du même id | `204` puis `404` |

## 8. Hors périmètre (pour ce sprint)

- **Authentification** (comptes, mots de passe, tokens) : Sprint 3.
- **Docker et PostgreSQL** : Sprint 3. Ce sprint utilise SQLite, une base de données dans un simple fichier.
- **Déploiement en ligne** : Sprint 4.
- **Interface graphique** : l'API se teste avec sa documentation automatique et avec les tests.
- **Plans par motorisation** : bonus en fin de sprint.

---

# Exercices, étape par étape

Même méthode qu'au Sprint 1 : **dans l'ordre**, logique en **français** avant le code, tests **verts** avant de passer à la suite.

### Étape 0 : Le terrain
- Ajoute FastAPI et un serveur pour le lancer.
- Crée une application avec l'endpoint **E1**.
- Lance le serveur et ouvre la **documentation automatique** dans ton navigateur (cherche `/docs`).
- ✅ **Réussi si :** tu peux appeler E1 depuis la page de documentation.

### Étape 1 : Tester une API
- Écris le test **T1**, sans lancer le serveur à la main.
- 💡 Cherche le client de test fourni par FastAPI.
- ✅ **Réussi si :** `uv run pytest` lance tes 28 anciens tests **et** le nouveau.

### Étape 2 : Les schémas
- Crée les schémas d'**entrée** et de **sortie** d'un véhicule, avec Pydantic.
- ❓ *Question :* pourquoi ne pas réutiliser directement tes dataclasses du Sprint 1 ? Pense à l'id, aux règles comme A3, et à la règle d'or de la section 4.
- ❓ *Question :* le schéma d'entrée doit-il contenir l'id ? Et celui de sortie ?

### Étape 3 : Créer et lire un véhicule (stockage en mémoire)
- Implémente **E2, E3, E4**, avec un stockage **en mémoire** pour l'instant (un simple dictionnaire).
- ❓ *Question :* comment générer un identifiant unique ?
- 🧪 **Tests :** T2, T3, T4, T5, T6.

### Étape 4 : Ajouter un entretien
- Implémente **E5**.
- Les erreurs du métier doivent devenir des réponses `422` propres (A5, A6).
- 🧪 **Tests :** T7, T8, T9.

### Étape 5 : Le kilométrage
- Ajoute la règle **A9** dans le **métier**, avec ses tests **métier**.
- Implémente **E6**.
- 🧪 **Tests :** T10, T11.

### Étape 6 : Les entretiens dus
- Implémente **E7**, avec la date optionnelle (A7, A8).
- 🧪 **Tests :** T12, plus un test avec une date où rien n'est dû.

### Étape 7 : Supprimer
- Implémente **E8**.
- 🧪 **Tests :** T13.

### Étape 8 : La persistance
- Remplace le stockage en mémoire par une base **SQLite** avec SQLAlchemy.
- ❓ *Question :* combien de fichiers devrais-tu modifier ? Si la réponse est « beaucoup », ton stockage n'était pas assez séparé. Cherche le principe du « repository ».
- ✅ **Réussi si :** tu arrêtes le serveur, tu le relances, et tes véhicules sont toujours là.
- 🧪 **Tests :** tous les tests d'API restent verts, avec une base de test séparée.

### Étape 9 : Relecture et publication
- Ruff, mypy, tests verts (anciens + nouveaux).
- Mets le README à jour : les endpoints, comment lancer l'API, comment ouvrir la documentation.
- Commit propre, puis push.

### Bonus
- Plans d'entretien par **motorisation** (voir le hors périmètre du Sprint 1).
- Endpoint « bientôt dû » : il reste moins de 10 % de la limite.
- Pagination de E4 quand il y a beaucoup de véhicules.

---

## Rappels utiles

- Lancer l'API : cherche comment démarrer le serveur avec `uv run`.
- Documentation automatique : `/docs` une fois le serveur lancé.
- Codes à retenir : `200` OK · `201` créé · `204` supprimé, rien à renvoyer · `404` introuvable · `422` données refusées.
- Le **métier** ne doit jamais importer FastAPI, Pydantic ou SQLAlchemy. Si c'est le cas, c'est que quelque chose est au mauvais endroit.