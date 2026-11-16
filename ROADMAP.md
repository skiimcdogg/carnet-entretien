# Carnet d'entretien auto : feuille de route

> **Objectif :** faire de ce projet la meilleure pièce de ton CV de développeur backend Python.
> Pas de vente, pas de pression : chaque sprint ajoute une compétence que les recruteurs cherchent, sur un sujet que tu maîtrises.
>
> Mise à jour : 16 novembre 2026. Chaque sprint aura son propre cahier des besoins.

---

## La carte

```
 Sprint 1 ✅    Sprint 2 🔄    Sprint 3       Sprint 4       Sprint 5       Sprint 6       Sprint 7
 Le métier  →   L'API      →   Sécurité   →   En ligne   →   Rappels    →   Brique IA  →   Interface
                               Docker, CI     🎯 CV prêt     automatiques   scan ticket    web
```

| Sprint | Thème | Ce que tu ajoutes à ton CV | Fin estimée |
|---|---|---|---|
| 1 ✅ | Le métier | Python moderne, tests, typage | fait |
| 2 🔄 | L'API | FastAPI, Pydantic, SQLAlchemy | début décembre |
| 3 | Sécurité et industrialisation | JWT, PostgreSQL, Docker, CI/CD | fin décembre |
| 4 | Mise en ligne | Déploiement AWS, surveillance | **fin janvier → tu postules** |
| 5 | Rappels automatiques | Tâches planifiées, e-mails | mi-février |
| 6 | Brique IA | Appel à un modèle d'IA, fichiers | début mars |
| 7 | Interface web | React + TypeScript, fullstack | fin mars |

Les dates comptent **3 semaines par sprint**, ton rythme réel du Sprint 1. Ce sont des repères, pas des échéances.

---

## Sprint 2 : l'API 🔄

**L'idée :** rendre ton carnet utilisable depuis l'extérieur.

- 8 endpoints : créer, lire, lister et supprimer un véhicule, ajouter un entretien, mettre à jour le kilométrage, lire les entretiens dus.
- Des schémas qui vérifient tout ce qui entre.
- Des erreurs propres : `404`, `422`, jamais d'erreur Python brute.
- Les données conservées dans une base SQLite.

**Détail :** voir `cahier-sprint-2.md`. Tu en es à l'étape 2.

**Trois choix à faire maintenant, pour ne rien refaire plus tard :**

| Choix | Pourquoi |
|---|---|
| Des identifiants impossibles à deviner (UUID) plutôt que 1, 2, 3 | Avec des numéros qui se suivent, on peut essayer l'identifiant du voisin. C'est une faille classique |
| Un stockage bien séparé (le principe du « repository ») | Passer de SQLite à PostgreSQL doit toucher un seul fichier |
| Un métier qui se protège tout seul | Voir le point 1 de `CODE_REVIEW.md` |

> 🎤 **En entretien, tu sauras répondre à :** « Comment tu structures une API ? », « Quelle différence entre un schéma et un modèle ? », « Pourquoi séparer le métier du framework ? »

✅ **Terminé quand :** les 13 tests d'API du cahier sont verts, et tes véhicules survivent à un redémarrage.

---

## Sprint 3 : sécurité et industrialisation

**L'idée :** passer d'un exercice à un projet « comme en entreprise ».

- **Comptes utilisateurs** : inscription, connexion, jetons d'accès (JWT).
- **Chaque véhicule a un propriétaire.** On ne voit et on ne modifie que les siens.
- **Mots de passe** stockés de façon sûre (hachés, jamais en clair).
- **PostgreSQL** à la place de SQLite, avec des migrations (Alembic) pour faire évoluer la base sans la casser.
- **Docker** : l'API et la base démarrent avec une seule commande.
- **CI GitHub Actions** : tests, ruff et mypy à chaque push, avec un badge vert sur le README.
- Supprimer un entretien saisi par erreur.

> 💪 **Ton terrain :** JWT, révocation d'accès, Docker et CI/CD, tu les as déjà pratiqués en mission. Ici, tu les construis seul de bout en bout, et tu peux le prouver.

> 🎤 **En entretien :** « Comment tu sécurises une API ? », « Authentification ou autorisation, quelle différence ? », « Comment tu modifies une base en production ? »

✅ **Terminé quand :** un test prouve que l'utilisateur A ne peut ni lire ni modifier le véhicule de l'utilisateur B.

---

## Sprint 4 : mise en ligne

**L'idée :** une vraie adresse, que n'importe qui peut ouvrir.

- **Déploiement sur AWS**, en HTTPS.
- **Déploiement continu** : un push sur `main` met le site à jour tout seul.
- Configuration par variables d'environnement. Aucun secret dans le code.
- **Journaux** lisibles et surveillance de `/health`.
- Sauvegarde automatique de la base.
- Limitation du nombre d'appels, pour éviter les abus.
- README refait : lien vers l'API en ligne, schéma de l'architecture, captures d'écran.

> 🎤 **En entretien :** « Raconte-moi un déploiement de bout en bout », « Comment tu sais que ton appli est en panne ? », « Où tu ranges tes secrets ? »

✅ **Terminé quand :** un recruteur clique sur un lien dans ton CV et voit la documentation de ton API en ligne.

### 🎯 Jalon : ton CV est prêt

À ce stade, tu as un backend Python **complet, testé, sécurisé et en ligne**. C'est le moment de mettre à jour ton CV et ton LinkedIn, et de postuler. **N'attends pas les sprints suivants :** ils se font en parallèle des candidatures, et te donnent du neuf à raconter à chaque entretien.

**La ligne sur ton CV :**

> *Carnet d'entretien auto, projet personnel.* Conception et développement d'une API REST de suivi d'entretien de véhicules : Python, FastAPI, PostgreSQL, authentification JWT, Docker, CI/CD GitHub Actions, déploiement AWS. Plus de 60 tests automatisés, typage vérifié par mypy.

---

## Sprint 5 : les rappels automatiques

**L'idée :** l'application travaille toute seule, même quand personne ne l'ouvre.

- **Motorisation du véhicule** (essence, diesel, hybride, électrique), avec un plan d'entretien par motorisation.
- **Plan personnalisable** : chacun ajuste ses échéances.
- **Statut « bientôt dû »**, et le nombre de kilomètres et de jours restants.
- Un vrai calcul des mois, à la place de « 1 mois = 30 jours ».
- **Une tâche planifiée** vérifie tous les véhicules chaque jour.
- **Un e-mail de rappel** quand un entretien approche.

> 🎤 **En entretien :** « Comment tu lances un traitement tous les jours ? », « Que se passe-t-il si l'envoi d'un e-mail échoue ? », « Comment tu évites d'envoyer deux fois le même rappel ? »

✅ **Terminé quand :** tu reçois un vrai e-mail pour la révision de ta propre voiture.

---

## Sprint 6 : la brique IA

**L'idée :** la compétence la plus recherchée en ce moment, sur un cas concret.

- **Photo d'un ticket ou d'une facture** envoyée à l'API (stockage de fichiers).
- **Un modèle d'IA lit le document** et propose un entretien pré-rempli : date, type, pièces, montant.
- L'utilisateur **vérifie et valide**. L'IA propose, l'humain décide.
- Gestion des cas ratés : photo floue, document qui n'est pas une facture.
- Suivi du **coût** de chaque appel à l'IA.
- Des tests qui ne dépendent pas de l'IA (on la remplace par un faux modèle).

> 🔧 **Pour toi :** tu fais ton entretien toi-même, donc tu as des tickets de pièces. Tu testeras avec les tiens.

> 🎤 **En entretien :** « Comment tu intègres un modèle d'IA dans une application ? », « Comment tu testes du code qui appelle une IA ? », « Que fais-tu quand l'IA se trompe ? »

✅ **Terminé quand :** tu prends en photo un vrai ticket d'huile et de filtres, et l'entretien arrive pré-rempli.

---

## Sprint 7 : l'interface web

**L'idée :** montrer le projet à quelqu'un qui ne lit pas de code, et prouver ton profil fullstack.

- Application **React + TypeScript**, pensée d'abord pour le téléphone.
- Écrans : connexion, mes véhicules, fiche véhicule avec l'historique, entretiens dus, ajout d'un entretien.
- Envoi d'une photo de ticket depuis le téléphone.
- En ligne, avec un **compte de démonstration** pour les recruteurs.

> 🎤 **En entretien :** tu ouvres ton téléphone et tu montres l'application. C'est la meilleure démonstration possible.

✅ **Terminé quand :** tu gères l'entretien de ta voiture depuis ton téléphone.

---

## La boîte à idées

Pour après, ou pour remplacer un sprint qui te tente moins. Chacune ajoute une compétence.

| Idée | Ce que tu apprends |
|---|---|
| Dossier d'entretien en PDF, pour la revente | Génération de documents |
| Coût de chaque entretien, total par an | Requêtes d'agrégation en SQL |
| Fiche pièces : références, huile, couples de serrage | Modélisation de données |
| Mise en cache des calculs (Redis) | Performance |
| Tests de charge : combien d'utilisateurs en même temps ? | Mesure et optimisation |
| Une version Rust du calcul des entretiens dus | Ta curiosité pour Rust |

---

## Les règles du jeu

1. **Tu écris le code.** L'IA répond à tes questions, elle ne tape pas à ta place.
2. **Les tests restent verts.** Ceux du Sprint 1 ne cassent jamais.
3. **On réfléchit en français avant de coder.**
4. **Un sprint à la fois.** On ne commence pas le suivant avant d'avoir fini.
5. **La recherche d'emploi passe avant le projet.** Si un entretien demande de la préparation, le sprint attend.
6. **On a le droit de changer le plan.** Si un sprint t'ennuie, on le remplace par une idée de la boîte.