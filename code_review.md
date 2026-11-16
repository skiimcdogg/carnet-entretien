# Code review : carnet-entretien

> Review du commit `4688700` du 16 novembre 2026, faite comme une Pull Request.
> Sprint 1 terminé, Sprint 2 aux étapes 0 et 1.

## Verdict

**Base solide, prête pour la suite du Sprint 2.** La logique métier est juste et bien testée. Avant d'ouvrir l'API au monde, il reste deux corrections importantes : le métier doit se protéger lui-même, et une valeur d'enum est incohérente.

## Ce que j'ai vérifié

| Commande | Résultat |
|---|---|
| `uv run pytest` | ✅ 28 tests verts |
| `uv run ruff check` et `ruff format --check` | ✅ rien à signaler |
| `uv run mypy src` | ✅ aucune erreur |
| `uv run mypy tests` | ❌ 3 erreurs (voir le point 4) |
| `uv run mypy --strict src` | ❌ 1 erreur (voir le point 5) |
| Essais à la main sur le métier | ❌ des valeurs absurdes sont acceptées (voir le point 1) |

## ✅ Points forts

- **La logique de calcul est correcte** et couvre tous les exemples du cahier des besoins.
- **Un vrai filet de sécurité** : 28 tests, ruff, mypy et pre-commit, tous dans le repo.
- **Une architecture propre** : les imports vont dans un seul sens, et l'API est rangée dans le paquet.
- **Le métier ne dépend d'aucun framework** : ni FastAPI ni Pydantic dans `models.py`.
- **Les types sont justes** : `int | None`, `Maintenance | None`, `-> None`.
- **Les tests sont à la racine**, séparés entre métier et API.
- **Le ménage des tests est fait** : une seule date `TODAY`, l'enum dans les `assert`.
- **Tu as corrigé une règle fausse de la spécification** (R8) avant même de coder.

---

## 🚨 Priorité 1 : à corriger avant d'écrire les endpoints

### 1. Le métier ne se protège pas tout seul

**Où :** `src/carnet_entretien/models.py`, classes `Vehicle` (ligne 25) et `MaintenanceRule` (ligne 15).

**Le constat :** tout ceci est accepté sans erreur.

| Ce que j'ai essayé | Résultat |
|---|---|
| Un véhicule à **-5 km** | accepté |
| Une règle à **-10 km** | acceptée |
| Une règle à **0 km et 0 mois** | acceptée, donc un entretien « toujours dû » |
| Un entretien daté **avant** la mise en circulation | accepté |

**Pourquoi c'est important :** jusqu'ici, toi seul créais les objets. Avec une API, n'importe qui peut envoyer n'importe quoi. Les schémas Pydantic vérifieront la forme des données à l'entrée, mais le métier doit rester correct **même sans l'API**. On appelle ça la défense en profondeur : chaque couche fait sa part.

**Indices :**
- Tu connais déjà l'outil : `__post_init__`.
- Relis R6 dans le cahier : que veut dire une limite à 0 ? Faut-il l'accepter ?
- Une mise en circulation **dans le futur** ne peut pas être vérifiée ici, puisqu'il n'y a pas de `today`. Qui a accès à la date du jour ? C'est à cette couche de le vérifier.
- Un test par cas refusé, comme tu l'as fait pour l'historique invalide.

### 2. Une valeur d'enum incohérente

**Où :** `src/carnet_entretien/enums.py`, ligne 7.

**Le constat :** `TRANSMISSION = "Transmission"`, avec une majuscule. Les cinq autres valeurs sont en minuscules.

**Pourquoi c'est important :** avec un `StrEnum`, c'est cette valeur qui apparaîtra dans le JSON de ton API et dans la base de données. Une app qui enverra `"transmission"` recevra une erreur `422`, et personne ne comprendra pourquoi.

---

## 🔧 Priorité 2 : à améliorer pendant le Sprint 2

### 3. Une condition difficile à relire

**Où :** `src/carnet_entretien/models.py`, lignes 69 à 74.

**Le constat :** la condition a la forme `A and B or C and D`, sans parenthèses.

**Pourquoi c'est important :** elle est juste, mais seulement parce que Python évalue `and` avant `or`. Le prochain lecteur devra s'en souvenir pour la comprendre. Et une modification maladroite peut casser la logique sans que ça se voie.

**Indice :** donne un nom à chaque moitié, avec deux variables qui se lisent comme une phrase. Ta ligne finale devient alors évidente.

### 4. mypy n'est pas dans pre-commit, et il échoue sur les tests

**Où :** `.pre-commit-config.yaml`, et le dossier `src/carnet_entretien/`.

**Le constat :**
- pre-commit lance ruff et pytest, mais pas mypy. Il est installé, mais jamais lancé automatiquement.
- `uv run mypy tests` affiche 3 erreurs du type « module is installed, but missing library stubs or py.typed marker ».

**Pourquoi :** par défaut, mypy ne fait pas confiance aux types d'un paquet installé. Un fichier **vide** nommé `py.typed`, placé dans `src/carnet_entretien/`, lui dit : « ce paquet est typé, tu peux lire ses types ». J'ai vérifié : avec ce fichier, les 3 erreurs disparaissent.

**À faire :** ajouter le fichier `py.typed`, puis un hook mypy sur le modèle des trois autres.

### 5. Une fonction sans type de retour

**Où :** `src/carnet_entretien/api/routers/health.py`, ligne 7.

**Le constat :** `get_health` n'a pas de type de retour. Tout le reste du projet est typé.

**Pour aller plus loin :** par défaut, mypy ignore les fonctions sans types. Le mode strict les signale. Tu peux l'activer dans `pyproject.toml` pour qu'aucune fonction non typée ne passe.

### 6. Des tests longs et répétitifs

**Où :** `tests/test_vehicles.py`, 366 lignes.

**Le constat :**
- Le même véhicule est recréé à la main dans presque chaque test.
- Les arguments de `Vehicle(...)` et `Maintenance(...)` ne sont pas nommés. `Vehicle("Volkswagen", "Polo", 50_000, REGISTRATION_DATE)` ne dit pas ce qu'est le 50 000. C'est la quatrième fois que ce point revient.

**Indice :** cherche les **fixtures** de pytest. Une fixture prépare un objet une seule fois, et chaque test la reçoit en paramètre. C'est une notion très demandée en entretien.

---

## 🧹 Priorité 3 : le ménage (15 minutes)

| Où | Quoi |
|---|---|
| `.idea/` | Toujours suivi par git. À ajouter au `.gitignore`, puis à retirer avec `git rm -r --cached .idea` |
| `.gitignore` | Ajouter `.pytest_cache`, `.ruff_cache`, `.mypy_cache` |
| `src/carnet_entretien/api/routers/vehicles.py` | Ne contient que du code commenté. On ne commite pas de code commenté : git garde l'historique pour toi |
| `pyproject.toml`, ligne 4 | La description est encore « Add your description here » |
| `pyproject.toml`, lignes 14 et 15 | Le bloc `[project.scripts]` pointe vers une fonction `main` de démonstration. Supprimer les deux |
| `README.md`, lignes 18 et 20 | Le titre « Règles métier » est en double |
| `README.md`, ligne 28 | La stack oublie FastAPI, mypy et pre-commit |
| `README.md`, fin | Les « prochaines étapes » ne sont plus à jour |

## 📌 Limites connues (rien à faire maintenant)

- **« 1 mois = 30 jours »** : sur 60 mois, l'échéance tombe environ 26 jours trop tôt. C'est un choix assumé du cahier, à remplacer par un vrai calcul de mois au Sprint 5.
- **`requires-python = ">=3.15"`** : très récent. Au moment du déploiement (Sprint 4), vérifie que l'hébergeur propose cette version.
- **Entretiens au même kilométrage** : si deux entretiens du même type ont le même kilométrage, `find_last_maintenance` en prend un sans regarder la date. Cas rare, à garder en tête.

---

## Checklist

**Priorité 1**
- [ ] Refuser un kilométrage négatif sur le véhicule et sur l'entretien
- [ ] Refuser une règle avec une limite négative ou nulle
- [ ] Refuser un entretien daté avant la mise en circulation
- [ ] Un test pour chaque refus
- [ ] Corriger la valeur de `TRANSMISSION`

**Priorité 2**
- [ ] Nommer les deux moitiés de la condition du calcul
- [ ] Ajouter `py.typed` et le hook mypy dans pre-commit
- [ ] Typer le retour de `get_health`
- [ ] Découvrir les fixtures pytest et nommer les arguments

**Priorité 3**
- [ ] Faire le ménage du tableau ci-dessus

## Journal de progression

| | |
|---|---|
| **Acquis** | dataclasses, enums, typage, exceptions, pytest, `pytest.raises`, list comprehensions, `__post_init__`, uv, ruff, mypy, pre-commit, premier endpoint FastAPI, `TestClient` |
| **Erreurs récurrentes** | arguments non nommés ; fautes de frappe ; commandes lancées sans `uv run` |
| **Points forts** | le sens métier ; tu remets en cause la spécification quand elle est fausse ; tu corriges vite après une review |
| **Prochaines notions** | schémas Pydantic, codes HTTP, fixtures pytest, base de données |