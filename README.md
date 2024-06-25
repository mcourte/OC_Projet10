# Projet 10 : Créez une API sécurisée RESTful en utilisant Django REST

Lien vers [Model et Permissions](https://lucid.app/lucidchart/378041c3-53f8-4496-8309-5a301613f3b2/edit?viewport_loc=-1672%2C20%2C6502%2C2981%2CHWEp-vi-RSFO&invitationId=inv_c7286fd3-34f0-4863-aeff-c0c3a1318607)
Lien vers [Schéma conceptuel](https://lucid.app/lucidspark/d6c8cb09-ff0c-4db7-9156-109788b2f91c/edit?viewport_loc=853%2C1106%2C3121%2C1465%2C0_0&invitationId=inv_281a3599-9bf7-44d1-9bc1-95479b0af692)  
  

Nota : il est OBLIGATOIRE de créer un compte sur LucidApp pour avoir accès aux différents fichiers.  
  
  
## But du projet :

Développer une API REST avec Django.    


## Etape 1 : Télécharger le code

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.  
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.  


## Etape 2 ; Installer Python et ouvrir le terminal de commande

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :  
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   


## Etape 3 : Création de l'environnement virtuel

Se placer dans le dossier où l'on a extrait l'ensemble des documents grâce à la commande ``cd``  

Exemple :
```
cd home/magali/OpenClassrooms/Formation/Projet_10
```

Installez pipenv pour créer l'environnement virtuel  
```
pip install pipenv
pipenv install
```

Pour l'activer, éxecuter la commande suivante :  
```
pipenv shell
```

## Etape 4 : Télécharger les packages nécessaires au bon fonctionnement du programme

Installez ensuite les packages requis:  
```
pipenv install -r requirements.txt
```

## Etape 5 : Effectuer les migrations

Pour effectuer les migrations nécessaires au fonctionnement du projet, placer vous dans le dossier SoftDesk_Support :  
Exemple :
```
cd home/magali/OpenClassrooms/Formation/Projet_10/SoftDesk_Support

```
Puis, exécuter les commandes suivantes :  

```
python manage.py makemigrations
```
  
```
python3 manage.py migrate
```


## Etape 6 : Lancer le serveur

Pour lancer le serveur, il ne vous reste qu'à exécuter la commande suivante :  

```
python3 manage.py runserver
```
Vous pouvez ensuite utiliser l'applicaton à l'adresse suivante:  
```
http://127.0.0.1:8000
```


## Informations

Pour utiliser et tester l'API, vous avez deux possibilités :  
* Utiliser POSTMAN
* Aller sur la page du serveur Django : [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Connexion

Pour vous connecter à l'API depuis le serveur, utiliser l'un des comptes utilisateurs ci-dessous : 
En haut à droite utiliser le bouton login  et prenez un des utlisateurs de la liste des utilisateurs existant ci dessous.
Utiliser la liste des endpoints ci dessous pour tester L'API.
Pour changer d utilisateur il faut repasser par l'adresse de depart de l API : http://127.0.0.1:8000 , les pages etant protégé contre les utilisateurs non inscrits c est la seule page ou on peut changer d' utilisateur.

#### Liste des utilisateurs existants :

| *ID* | *Identifiant* | *Mot de passe* |
|------|---------------|----------------|
| 1    | magali_c      | S3cretadmin!   |
| 5    | florine_g     | S3cret!!!      |
| 8    | user_two      | S3cret!!!      |


#### Liste des points de terminaison de l'API (détaillés dans la [documentation](https://www.postman.com/mission-technologist-4095363/workspace/softdesk-support-api/collection/31959558-afa076dd-400c-48a3-bc19-424a35a94270?action=share&creator=31959558)) :


| #   | *Point de terminaison de l'API*                                           | *Méthode HTTP* | *URL (base: http://127.0.0.1:8000)*                              |
|-----|---------------------------------------------------------------------------|----------------|------------------------------------------------------------------|
| 1   | Inscription de l'utilisateur                                              | POST           | /api/user/                                                       |
| 2   | Connexion de l'utilisateur                                                | POST           | /api/token/                                                      |
| 3   | Refresh Token de l'utilisateur                                            | POST           | /api/token/refresh/                                              |
| 4   | Récupérer la liste de tous les projets rattachés à l'utilisateur connecté | GET            | /api/projects                                                    |
| 5   | Créer un projet                                                           | POST           | /api/projects/                                                   |
| 6   | Récupérer les détails d'un projet via son id                              | GET            | /api/projects/:project_id/                                        |
| 7   | Mettre à jour un projet                                                   | PATCH          | /api/projects/:project_id/                                        |
| 8   | Supprimer un projet et ses problèmes                                      | DELETE         | /api/projects/:project_id/                                        |
| 9   | Ajouter un utilisateur (contributeur) à un projet                         | POST           | /api/projects/:project_id/contributors/                           |
| 10  | Récupérer la liste de tous les contributeurs attachés à un projet         | GET            | /api/projects/:project_id/contributors/                           |
| 11  | Détails d'un (collaborateur) utilisateur d'un projet                      | GET            | /api/projects/:project_id/contributors/:id_contributor/           |
| 12  | Supprimer un (collaborateur) utilisateur d'un projet                      | DELETE         | /api/projects/:project_id/contributors/:id_contributor/           |
| 13  | Récupérer la liste des Issues liés à un projet                            | GET            | /api/projects/:project_id/issues/                                 |
| 14  | Créer une Issue dans un projet                                            | POST           | /api/projects/:project_id/issues/                                 |
| 15  | Mettre à jour une Issue dans un projet                                    | PATCH          | /api/projects/:project_id/issues/:issue_id/                       |
| 16  | Supprimer une Issue d'un projet                                           | DELETE         | /api/projects/:project_id/issues/:issue_id/                       |
| 17  | Recupérer la listes des Comments d une issu liés a un projet              | GET            | /api/projects/:project_id/issues/:issue_id/comments/              |
| 18  | Créer un Comments dans une Issue                                          | POST           | /api/projects/:project_id/issues/:issue_id/comments/              |
| 19  | Mettre à jour un Comments dans une Issue                                  | PATCH          | /api/projects/:project_id/issues/:issue_id/comments/:comment_id/ |
| 20  | Supprimer un Comments d une issu                                          | DELETE         | /api/projects/:project_id/issues/:issue_id/comments/:comment_id/ |
| 21  | Liste de tout les projets pour les administrateurs                        | GET            | /api/admin/projects/                                             |
| 22  | Liste de tout les utilsateurs pour les administrateurs                    | GET            | /api/users/                                                       |
| 23  | Details d'un utilisateur.(seulement le sien sauf pour les administrateurs)| GET            | /api/users/:id/                                       |
| 24  | Modifier un utilisateur.(seulement le sien sauf pour les administrateurs) | PATCH          | /api/users/:id/                                       |
| 25  | Supprimer un utilisateur.(seulement le sien sauf pour les administrateurs)| DELETE         | /api/users/:id/                                       |