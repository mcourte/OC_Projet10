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

Pour vous connecter à l'API depuis le serveur.
En haut à droite utiliser le bouton Login et choisissez l'un des comptes utilisateurs ci-dessous : 


#### Liste des utilisateurs existants :

| *ID* | *Identifiant* | *Mot de passe* |
|------|---------------|----------------|
| 1    | magali_c      | S3cretadmin!   |
| 5    | florine_g     | S3cret!!!      |
| 8    | micki_courte  | S3cret!!!      |

Concernant l'utilisation de POSTMAN, 3 environnements ont été créés, un pour chacun des utilisateurs du tableau précédent.  


#### Liste des points de terminaison de l'API (détaillés dans [POSTMAN](https://elements.getpostman.com/redirect?entityId=31959558-afa076dd-400c-48a3-bc19-424a35a94270&entityType=collection)):  


| #   | *Point de terminaison de l'API*                                           | *Méthode HTTP* | *URL (base: http://127.0.0.1:8000)*                               |
|-----|---------------------------------------------------------------------------|----------------|-------------------------------------------------------------------|
| 00  | Endpoint pour les administrateurs                                         | GET            | /api/admin/                                                       |
| 1   | Inscription de l'utilisateur                                              | POST           | /api/register/   
| 2   | Obtain Token de l'utilisateur                                             | POST           | /api/token/                                                           |
| 3   | Connexion de l'utilisateur                                                | POST           | /api/login/                                                       |
| 4   | Refresh Token de l'utilisateur                                            | POST           | /api/token/refresh/
| 5   | Déconnexion de l'utilisateur                                              | POST           | /api/logout/                             |
| 6   | Récupérer la liste de tous les projets                                    | GET            | /api/projects/                                                    |
| 7   | Créer un projet                                                           | POST           | /api/projects/                                                    |
| 8   | Récupérer les détails d'un projet via son ID                              | GET            | /api/projects/:project_id/                                        |
| 9   | Mettre à jour un projet                                                   | PATCH          | /api/projects/:project_id/                                        |
| 10   | Supprimer un projet et ses issues associées                               | DELETE         | /api/projects/:project_id/                                        |
| 11   | Ajouter un utilisateur (contributor) à un projet                          | POST           | /api/projects/:project_id/contributors/                           |
| 12  | Récupérer la liste de tous les contributeurs attachés à un projet         | GET            | /api/projects/:project_id/contributors/                           |
| 13  | Détails d'un (collaborator) utilisateur d'un projet                       | GET            | /api/projects/:project_id/contributors/:id_contributor/           |
| 14  | Supprimer un (collaborator) utilisateur d'un projet                       | DELETE         | /api/projects/:project_id/contributors/:id_contributor/           |
| 15  | Récupérer la liste des Issues liés à un projet                            | GET            | /api/projects/:project_id/issues/                                 |
| 16  | Créer une Issue dans un projet                                            | POST           | /api/projects/:project_id/issues/                                 |
| 17  | Mettre à jour une Issue dans un projet                                    | PATCH          | /api/projects/:project_id/issues/:issue_id/                       |
| 18  | Supprimer une Issue d'un projet                                           | DELETE         | /api/projects/:project_id/issues/:issue_id/                       |
| 19  | Recupérer la liste des Comments associée à une Issue                      | GET            | /api/projects/:project_id/issues/:issue_id/comments/              |
| 20  | Créer un Comment dans une Issue                                           | POST           | /api/projects/:project_id/issues/:issue_id/comments/              |
| 21  | Mettre à jour un Comment associée à une Issue                             | PATCH          | /api/projects/:project_id/issues/:issue_id/comments/:comment_id/  |
| 22  | Supprimer un Comment associée à une Issue                                 | DELETE         | /api/projects/:project_id/issues/:issue_id/comments/:comment_id/  |
| 23  | Liste de tout les utilsateurs pour les administrateurs                    | GET            | /api/users/                                                       |
| 24  | Details d'un utilisateur.(seulement le sien sauf pour les administrateurs)| GET            | /api/users/:id/                                                   |
| 25  | Modifier un utilisateur.(seulement le sien sauf pour les administrateurs) | PATCH          | /api/users/:id/                                                   |
| 26  | Supprimer un utilisateur.(seulement le sien sauf pour les administrateurs)| DELETE         | /api/users/:id/                                                   |