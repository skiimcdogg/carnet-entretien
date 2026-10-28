# Carnet d'entretien auto : cahier des besoins

> Ce document décrit **ce que l'application doit faire**, pas **comment** la coder.
> Les noms des fichiers, classes, fonctions et variables, c'est **toi** qui les choisis.

---

## 1. Le besoin en une phrase

Quelqu'un qui entretient sa voiture veut savoir, à une date donnée, **quels entretiens il doit faire maintenant**.

## 2. L'histoire

Paul a une Dacia Sandero. Il fait ses vidanges et ses changements de pièces lui-même.
Il note tout dans un carnet papier, mais il oublie de le regarder.
Il voudrait une application qui lui dise : « Ta vidange est à faire. La courroie, c'est bon. »

## 3. Le vocabulaire métier

| Mot | Ce que ça veut dire | Exemple |
|---|---|---|
| **Véhicule** | La voiture suivie. Elle a une marque, un modèle et un kilométrage actuel. | Dacia Sandero, 70 000 km |
| **Intervention** | Un entretien **déjà fait**. On note le type, la date et le kilométrage du jour. | Vidange faite le 28/08/2026 à 50 000 km |
| **Historique** | La liste de toutes les interventions d'un véhicule. C'est le carnet papier. | — |
| **Plan d'entretien** | Les règles du constructeur : pour chaque type d'entretien, une limite en km **et** une limite en temps. | Vidange : tous les 15 000 km **ou** tous les 12 mois |
| **Entretien dû** | Un entretien qu'il faut faire maintenant, parce qu'une limite est dépassée. | — |

**Point clé :** l'historique, c'est le **passé** (ce qui a été fait). Le plan, ce sont les **règles** (ce qui doit être fait). L'application compare les deux.

## 4. Les règles métier

- **R1.** Un véhicule commence avec un historique vide.
- **R2.** On peut ajouter une intervention à l'historique d'un véhicule.
- **R3.** On refuse une intervention dont le kilométrage est **plus grand** que le kilométrage actuel du véhicule. C'est impossible : on ne peut pas avoir fait une vidange dans le futur.
- **R4.** Pour un type d'entretien, seule la **dernière** intervention compte, celle avec le plus grand kilométrage.
- **R5.** Un entretien est **dû** s'il n'a **jamais** été fait.
- **R6.** Un entretien est **dû** si les km parcourus depuis la dernière intervention **atteignent ou dépassent** la limite en km.
- **R7.** Un entretien est **dû** si le temps passé depuis la dernière intervention **atteint ou dépasse** la limite en temps. On compte 1 mois = 30 jours.
- **R8.** R6 et R7 fonctionnent en « **le premier des deux** » : une seule limite dépassée suffit.
- **R9.** Le résultat est la liste des **types** d'entretien dus, par exemple « vidange », « courroie ». La liste peut être vide.
- **R10.** La date du jour est **fournie** au calcul. On ne la lit pas dans l'horloge de l'ordinateur, pour que les tests donnent toujours le même résultat.

## 5. Exemples chiffrés (ce seront tes tests)

Pour tous les exemples, sauf indication contraire :
- Plan : **vidange tous les 15 000 km ou 12 mois**.
- Date du jour : **28/10/2026**.

| # | Km actuels | Dernière vidange | Résultat attendu | Règle testée |
|---|---|---|---|---|
| A | 70 000 | 28/08/2026 à 50 000 km | vidange **due** (20 000 km parcourus) | R6 |
| B | 52 000 | 01/09/2025 à 50 000 km | vidange **due** (plus de 12 mois) | R7 |
| C | 55 000 | 28/08/2026 à 50 000 km | **rien** à faire | R6 + R7 |
| D | 55 000 | jamais faite | vidange **due** | R5 |
| E | 65 000 | 28/08/2026 à 50 000 km | vidange **due** (pile 15 000 km) | R6, cas limite |
| F | 70 000 | une à 40 000 km **et** une à 60 000 km | **rien** à faire (seule celle de 60 000 compte) | R4 |
| G | 50 000 | on essaie d'ajouter une vidange à 60 000 km | **refusé** (erreur) | R3 |

Exemple avec deux types d'entretien :

| # | Plan | Situation | Résultat attendu |
|---|---|---|---|
| H | vidange 15 000 km / 12 mois **+** courroie 120 000 km / 60 mois | 70 000 km, vidange à 50 000 km, courroie à 20 000 km il y a 2 ans | **vidange** due seulement |

## 6. Hors périmètre (pour l'instant)

- Pas de base de données : tout est en mémoire.
- Pas d'API, pas d'interface : juste du Python et des tests.
- Pas de plan automatique selon le modèle de voiture : on donne le plan à la main.
- Pas d'alerte « bientôt dû ». Ça viendra en bonus.

---

# Exercices, étape par étape

Fais-les **dans l'ordre**. Ne passe à l'étape suivante que quand les tests de l'étape sont **au vert**.
Pour chaque étape, commence par écrire en **français**, en commentaire, ce que ton code doit faire.

### Étape 0 : Le terrain
- Crée le projet avec uv, avec un dossier pour le code et un dossier pour les tests.
- Ajoute pytest en dépendance de développement.
- Écris un test qui vérifie juste que `1 + 1 == 2` et fais-le passer.
- ✅ **Réussi si :** la commande de test affiche un test vert.

### Étape 1 : Représenter un véhicule
- Crée une structure pour un véhicule : marque, modèle, kilométrage, historique.
- ❓ *Question :* quelle est la bonne valeur de départ pour l'historique, et quel piège faut-il éviter ?
- 🧪 **Test :** R1.

### Étape 2 : Représenter une intervention
- Crée une structure pour une intervention : type, date, kilométrage.
- ❓ *Question :* une intervention déjà faite, est-ce qu'elle doit pouvoir être modifiée ensuite ?
- 🧪 **Test :** créer une intervention et vérifier ses valeurs.

### Étape 3 : Ajouter une intervention
- Permets d'ajouter une intervention à un véhicule.
- Applique la règle R3 en levant une erreur.
- 🧪 **Tests :** un ajout normal (R2), puis l'exemple **G**.
- 💡 Cherche comment vérifier avec pytest qu'une erreur est bien levée.

### Étape 4 : Retrouver la dernière intervention d'un type
- Pour un type donné, retrouve la dernière intervention, ou « rien » s'il n'y en a pas.
- ❓ *Question :* comment représenter « rien » en Python ?
- 🧪 **Tests :** un type jamais fait, un type fait une fois, un type fait deux fois (exemple **F**).

### Étape 5 : Représenter une règle du plan
- Crée une structure pour une règle : limite en km et limite en mois.
- Choisis comment représenter un plan complet, c'est-à-dire plusieurs règles, chacune liée à un type d'entretien.
- ❓ *Question :* quelle structure Python associe un nom à une valeur ?

### Étape 6 : Calculer les entretiens dus
- À partir d'un véhicule, d'un plan et d'une date du jour, renvoie la liste des types dus.
- Écris d'abord l'algorithme en français, puis code-le ligne par ligne.
- 🧪 **Tests :** exemples **A, B, C, D, E, H**, un test par exemple.

### Étape 7 : Relecture
- Passe le formateur et le vérificateur de code (ruff).
- Relis tes noms : est-ce qu'un inconnu comprendrait ton code sans commentaire ?
- Fais un commit propre, puis pousse sur GitHub.

### Bonus
- Pour chaque entretien **pas encore dû**, calcule combien de km et de jours il reste.
- Ajoute une règle « bientôt dû » quand il reste moins de 10 % de la limite.

---

## Rappel pytest
- Le fichier de test commence par `test_`.
- Chaque fonction de test commence par `test_`.
- On vérifie avec `assert`.
- Chaque test suit 3 étapes : **Préparer → Agir → Vérifier**.
- Lancer les tests : `uv run pytest -v`.
