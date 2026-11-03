# Carnet d'entretien auto : cahier des besoins

> Ce document décrit **ce que l'application doit faire**, pas **comment** la coder.
> Les noms des fichiers, classes, fonctions et variables, c'est **toi** qui les choisis.
>
> Dernière mise à jour : 3 novembre 2026, Sprint 1, étape 5 terminée.

---

## 1. Le besoin en une phrase

Quelqu'un qui entretient sa voiture veut savoir, à une date donnée, **quels entretiens il doit faire maintenant**, pour anticiper au lieu d'attendre la panne ou l'usure.

## 2. L'histoire

Paul a une Dacia Sandero. Il fait son entretien lui-même et note tout dans un carnet papier, mais il oublie de le regarder.
Il voudrait une application qui lui dise : « Ta révision annuelle est à faire. La courroie, c'est bon. Tes plaquettes approchent de leur fin de vie. »

## 3. Le vocabulaire métier

| Mot | Ce que ça veut dire | Exemple |
|---|---|---|
| **Véhicule** | La voiture suivie : marque, modèle, kilométrage actuel. | Dacia Sandero, 70 000 km |
| **Entretien** | Une opération **prévisible**, qui revient à un rythme connu (km et/ou temps). | Révision annuelle, courroie de distribution |
| **Réparation** | Une intervention **imprévisible**, suite à une casse ou une panne. Hors périmètre. | Alternateur HS |
| **Type d'entretien** | La nature d'un entretien, choisie dans une **liste fermée**. | Révision annuelle |
| **Intervention** | Un entretien **déjà fait** : type, date et kilométrage du jour. | Révision faite le 28/08/2026 à 50 000 km |
| **Historique** | La liste de toutes les interventions d'un véhicule. C'est le carnet papier. | — |
| **Règle** | Le rythme d'un type d'entretien : une limite en km, une limite en temps, ou les deux. | Tous les 15 000 km ou 12 mois |
| **Plan d'entretien** | L'ensemble des règles : à chaque type d'entretien correspond une règle. | — |
| **Entretien dû** | Un entretien à faire maintenant, parce qu'une limite est atteinte. | — |

**Point clé :** l'historique, c'est le **passé** (ce qui a été fait). Le plan, ce sont les **règles** (ce qui doit être fait). L'application compare les deux.

## 4. Les types d'entretien

### Règle de conception
> **Un type = un ensemble d'opérations qui se font toujours ensemble, au même rythme.**

C'est pourquoi le changement des filtres ne forme pas un type à part : il fait partie de la révision annuelle.

### Liste actuelle

| Type | Contenu | Règle du plan par défaut |
|---|---|---|
| Révision annuelle | Vidange + tous les filtres | 15 000 km **ou** 12 mois |
| Courroie de distribution | Kit de distribution | 100 000 km **ou** 60 mois |
| Transmission | Huile de boîte de vitesses | 60 000 km **ou** 60 mois |
| Plaquettes de frein | Remplacement des plaquettes | 40 000 km, **pas de limite en temps** |
| Recharge de climatisation | Recharge du circuit | 24 mois, **pas de limite en km** |
| Pneus | Remplacement des pneus | 40 000 km **ou** 60 mois |

> Ce tableau est le **plan par défaut** du programme. Les **tests** n'utilisent pas ce plan : chacun crée le sien (voir section 6), pour ne pas casser quand ces valeurs changent. Les vraies valeurs dépendent du constructeur et de la motorisation (voir section 7).

Pneus et plaquettes s'usent selon la conduite, mais on leur donne une durée de vie **estimée** en km. Le but est d'avoir de la visibilité, pas d'attendre que le garagiste annonce qu'ils sont à changer.

## 5. Les règles métier

### Le véhicule et son historique
- **R1.** Un véhicule commence avec un historique vide.
- **R2.** On peut ajouter une intervention à l'historique. Les interventions déjà présentes sont conservées.
- **R3.** On refuse une intervention dont le kilométrage est **plus grand** que le kilométrage actuel du véhicule. Un kilométrage **égal** est accepté.
- **R3 bis.** On refuse une intervention dont la date est **après** la date du jour.
- **R4.** Une intervention enregistrée ne peut plus être modifiée.

### Le plan
- **R5.** Chaque règle a une limite en **km** et une limite en **mois**. Les deux sont **optionnelles**, mais une règle doit en avoir **au moins une**. Une règle sans aucune limite est refusée à la création.
- **R6.** « Pas de limite » et « limite à 0 » sont **deux choses différentes**. La première veut dire « on ne regarde pas ce critère ». La seconde voudrait dire « toujours dû ».

### Le calcul des entretiens dus
- **R7.** Pour un type d'entretien, seule la **dernière** intervention compte : celle avec le **plus grand kilométrage**.
- **R8.** Un entretien est **dû** s'il n'a **jamais** été fait.
- **R9.** Un entretien est **dû** si les km parcourus depuis la dernière intervention **atteignent ou dépassent** la limite en km, quand il y en a une.
- **R10.** Un entretien est **dû** si le temps passé depuis la dernière intervention **atteint ou dépasse** la limite en temps, quand il y en a une. On compte 1 mois = 30 jours.
- **R11.** C'est **le premier des deux** qui compte : une seule limite atteinte suffit.
- **R12.** Le résultat est la liste des **types** d'entretien dus. Elle peut être vide.
- **R13.** La date du jour est **fournie** au calcul. On ne la lit jamais dans l'horloge de l'ordinateur, pour que les tests donnent toujours le même résultat.

## 6. Exemples chiffrés (ce sont tes tests)

Pour tous les exemples, sauf indication contraire :
- Plan : **révision annuelle tous les 15 000 km ou 12 mois**.
- Date du jour : **30/10/2026**.

### Ajout d'interventions

| # | Situation | Résultat attendu | Règle |
|---|---|---|---|
| G1 | Véhicule à 50 000 km, on ajoute une intervention à 60 000 km | **refusé** (erreur km) | R3 |
| G2 | Véhicule à 50 000 km, on ajoute une intervention à 50 000 km | **accepté** | R3, cas limite |
| G3 | On ajoute une intervention datée du 01/11/2026 | **refusé** (erreur date) | R3 bis |
| G4 | On ajoute une 2e intervention à un véhicule qui en a déjà une | les **deux** sont dans l'historique | R2 |

### Recherche de la dernière intervention

| # | Historique | On cherche | Résultat attendu | Règle |
|---|---|---|---|---|
| L1 | une révision | la courroie | **rien** | R8 |
| L2 | une révision à 24 000 km | la révision | **cette** révision | R7 |
| L3 | révision à **60 000** km ajoutée **en premier**, puis révision à 40 000 km, plus une courroie | la révision | celle à **60 000 km** | R7, piège sur l'ordre |

### Calcul des entretiens dus

| # | Km actuels | Dernière révision | Résultat attendu | Règle |
|---|---|---|---|---|
| A | 70 000 | 28/08/2026 à 50 000 km | révision **due** (20 000 km parcourus) | R9 |
| B | 52 000 | 01/09/2025 à 50 000 km | révision **due** (plus de 12 mois) | R10 |
| C | 55 000 | 28/08/2026 à 50 000 km | **rien** à faire | R9 + R10 |
| D | 55 000 | jamais faite | révision **due** | R8 |
| E | 65 000 | 28/08/2026 à 50 000 km | révision **due** (pile 15 000 km) | R9, cas limite |
| F | 70 000 | 01/03/2025 à 40 000 km **et** 28/08/2026 à 60 000 km | **rien** à faire (seule celle de 60 000 compte) | R7 |

### Plusieurs types et règle sans limite en temps

| # | Plan | Situation | Résultat attendu |
|---|---|---|---|
| H | révision 15 000 km / 12 mois **+** courroie 120 000 km / 60 mois | 70 000 km ; révision à 50 000 km le 28/08/2026 ; courroie à 20 000 km le 30/10/2024 | **révision** due seulement |
| I | plaquettes 40 000 km, **pas de limite en temps** | 50 000 km ; plaquettes changées à 20 000 km le 01/01/2020 | **rien** à faire : 30 000 km parcourus, et le temps n'est pas regardé |
| J | clim 24 mois, **pas de limite en km** | 200 000 km ; recharge à 20 000 km le 01/06/2026 | **rien** à faire : 5 mois passés, et les km ne sont pas regardés |
| K | clim 24 mois, **pas de limite en km** | 50 000 km ; recharge à 48 000 km le 01/06/2024 | clim **due** : plus de 24 mois |

### Création d'une règle

| # | Situation | Résultat attendu | Règle |
|---|---|---|---|
| R-a | Règle avec km seulement | **acceptée** | R5 |
| R-b | Règle avec mois seulement | **acceptée** | R5 |
| R-c | Règle sans km ni mois | **refusée** (erreur) | R5 |

## 7. Hors périmètre (pour l'instant)

- **Réparations :** on ne gère que les entretiens prévisibles. Un historique des réparations pourra venir plus tard.
- **Plan selon la motorisation :** les échéances dépendent du moteur. Par exemple, une courroie de distribution n'a pas le même intervalle sur un diesel et sur un essence. Pour l'instant, **un seul plan** est fourni à la main. Au Sprint 2, les plans viendront de la base de données, par modèle et motorisation.
- **Base de données, API, interface :** Sprint 2 et suivants.
- **Alerte « bientôt dû » :** en bonus.

## 8. Architecture des fichiers

Les imports vont dans **un seul sens**, du bas vers le haut :

```
enums      → n'importe rien du projet (le socle)
models     → importe les enums
plan       → importe les enums et les models
calcul     → importe tout ce dont il a besoin
```

Si un fichier du bas importe un fichier du haut, on obtient un **import circulaire**.

## 9. Conventions du projet

- Le code est en **anglais**. Les commentaires et la doc peuvent être en français.
- Les classes s'écrivent en `PascalCase`, les fonctions et variables en `snake_case`, les constantes en `MAJUSCULES`.
- L'**unité** apparaît dans le nom quand il y en a une (`..._km`, `..._months`).
- Pas de nom qui masque un nom de Python : pas de champ `type`, `date`, `list`…
- Les **arguments sont nommés** quand on crée un objet avec plusieurs valeurs.
- Les grands nombres utilisent le séparateur : `50_000`.
- Les imports sont rangés : librairie standard d'abord, puis le projet.
- Un test = un comportement, avec la structure **Préparer → Agir → Vérifier**.
- Avant chaque commit : `uv run ruff format`, `uv run ruff check`, `uv run pytest`.

---

# Avancement et exercices

| Étape | Sujet | Statut |
|---|---|---|
| 0 | Mise en place du projet | ✅ |
| 1 | Représenter un véhicule | ✅ |
| 2 | Représenter une intervention | ✅ |
| 3 | Ajouter une intervention (R2, R3, R3 bis) | ✅ |
| 4 | Retrouver la dernière intervention d'un type | ✅ |
| 5 | Représenter une règle et un plan | ✅ (tests R-a à R-c à écrire) |
| 6 | Calculer les entretiens dus | 🔄 prochaine |
| 7 | Relecture et publication | ⏳ |

### Étape 5 : Représenter une règle et un plan ✅
- Règle avec deux limites optionnelles, dont au moins une obligatoire, vérifiée à la création (R5).
- Plan par défaut dans son propre fichier (voir section 8).
- 🧪 **Reste à faire :** tests **R-a, R-b, R-c**.

### Étape 6 : Calculer les entretiens dus
- À partir d'un véhicule, d'un plan et d'une date du jour, renvoie la liste des types dus.
- Écris d'abord l'algorithme en **français**, puis code-le ligne par ligne.
- Réutilise ta recherche de la dernière intervention.
- Attention à R9 et R10 : ne regarde un critère **que** s'il a une limite.
- 🧪 **Tests :** exemples **A à F, H, I, J et K**, un test par exemple.

### Étape 7 : Relecture et publication
- Lance le formateur, le vérificateur de code et le vérificateur de types (`mypy`).
- Relis tes noms : un inconnu comprendrait-il ton code sans commentaire ?
- Corrige les fautes de frappe (noms de marques, messages d'erreur).
- Rédige un `README.md` : ce que fait le projet, comment l'installer, comment lancer les tests.
- Commit propre, puis push sur GitHub.

### Bonus
- Pour chaque entretien **pas encore dû**, calcule combien de km et de jours il reste.
- Ajoute un statut « bientôt dû » quand il reste moins de 10 % de la limite.

---

## Rappel pytest
- Le fichier de test commence par `test_`, et chaque fonction de test aussi.
- On vérifie avec `assert`. On vérifie `None` avec `is None`.
- Une erreur attendue se vérifie avec `pytest.raises(TypeErreur, match="...")`.
- Un bon test est construit pour **piéger** les mauvaises solutions (exemple L3).
- Lancer les tests : `uv run pytest -v`.