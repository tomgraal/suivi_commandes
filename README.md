# Application de suivi des commandes

Une application Web de suivi des commandes pour le processus interne du GHT ADS.

## Fonctionnalités

- Authentification des utilisateurs
- Rôles : ingénieur, fournisseur, acheteur
- Création d’affaires par l’ingénieur
- Téléversement de devis, bon de commande et bon de réception en PDF
- Visualisation des documents PDF dans l’interface
- Signature numérique par l’ingénieur via un bouton dans l’interface
- Notifications par email (stub configurable avec SMTP)
- Stockage des fichiers PDF et données dans SQLite

## Structure du projet

```
.
├── data/                # Base de données SQLite
├── docker/              # Configuration Nginx
├── uploads/             # Fichiers PDF uploadés
├── src/                 # Application Flask
│   ├── app.py
│   ├── static/
│   └── templates/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .dockerignore
├── README.md
└── .github/copilot-instructions.md
```

## Installation locale

1. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   ```
2. Activez l’environnement :
   ```bash
   source venv/bin/activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancez l’application :
   ```bash
   python src/app.py
   ```
5. Ouvrez `http://127.0.0.1:8000`

## Exécution avec Docker

1. Construisez les conteneurs :
   ```bash
   docker compose build
   ```
2. Démarrez les services :
   ```bash
   docker compose up
   ```
3. Ouvrez `http://localhost:8080`

## Comptes de démonstration

Au premier démarrage, l’application génère trois comptes de démonstration :

- `engineer` / `password` (ingénieur)
- `buyer` / `password` (acheteur)
- `supplier` / `password` (fournisseur)

Les fournisseurs peuvent aussi s’inscrire via la page d’inscription.

## Configuration des emails

Ajoutez un fichier `.env` avec les variables suivantes si vous souhaitez envoyer de vrais emails :

```env
SECRET_KEY=change_me
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=vincentfluchere@gmail.com
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=vincentfluchere@gmail.com
```

Pour Gmail, utilisez un mot de passe d’application (App Password) avec la validation en deux étapes activée sur votre compte. Si votre fournisseur utilise SSL direct sur le port 465, mettez `MAIL_USE_SSL=true` et `MAIL_USE_TLS=false`.

Sans configuration SMTP, les notifications sont enregistrées dans les logs de l’application.

## Notes

- Les fichiers PDF sont stockés dans `uploads/`.
- La base de données SQLite est stockée dans `data/app.db`.
- Le service Nginx est accessible sur le port `8080` lorsque vous utilisez Docker.
