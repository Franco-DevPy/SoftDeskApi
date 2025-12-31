# SoftDesk API

SoftDesk API est une API REST permettant de gérer des projets collaboratifs, leurs contributeurs, des issues (tickets) et des commentaires.  
Le projet est développé avec Django et Django REST Framework et utilise l’authentification JWT pour sécuriser l’accès aux ressources.

## Fonctionnalités
- Création et gestion des utilisateurs.
- Authentification sécurisée via JSON Web Tokens (JWT).
- Création et gestion de projets.
- Gestion des contributeurs par projet (auteur, contributeurs).
- Création, consultation, modification et suppression d’issues.
- Ajout de commentaires sur les issues.
- Interface d’administration Django pour la gestion avancée.

## Prérequis
- Python 3.10+
- pip
- Git

## Installation (Windows)
1. Cloner le dépôt :
   ```powershell
   git clone https://github.com/Franco-DevPy/SoftDeskApi.git
   cd SoftDeskApi
   ```
Créer et activer un environnement virtuel :

```
powershell
Copier le code
python -m venv .venv
.\.venv\Scripts\Activate
```
Installer les dépendances :

```
powershell
Copier le code
pip install -r requirements.txt
```
Appliquer les migrations :

```
powershell
Copier le code
python manage.py migrate
```
(Optionnel) Créer un superutilisateur :

```
powershell
Copier le code
python manage.py createsuperuser
```
Lancer le serveur de développement :

```
powershell
Copier le code
python manage.py runserver
```
## Authentification
L’API utilise une authentification JWT.

Obtenir un token :

```
bash
Copier le code
POST /api/token/
```
Rafraîchir le token :

```
swift
Copier le code
POST /api/token/refresh/
```
Le token doit être transmis dans le header :

```
makefile
Copier le code
Authorization: Bearer <access_token>
```
## Tests de l’API
L’API peut être testée à l’aide d’outils tels que Bruno ou Postman en envoyant des requêtes HTTP avec un token JWT valide.

## Qualité du code
Le projet respecte les conventions PEP8 afin d’assurer la lisibilité, la maintenabilité et la cohérence du code.

## Auteur
Projet réalisé dans le cadre du parcours OpenClassrooms – Développeur d’application Python.