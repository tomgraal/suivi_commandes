# Application de suivi des commandes - GHT ADS

## 📋 Vue d'ensemble

Une application Web complète et sécurisée pour le suivi des commandes et des affaires au sein du processus interne du GHT Alpes du Sud. Cette plateforme collaborative permet aux ingénieurs, acheteurs et fournisseurs de gérer l'ensemble du cycle de vie des acquisitions : de la création d'une affaire jusqu'à la signature numérique des documents, en passant par le téléversement et la visualisation des devis, bons de commande et bons de réception.

## ✨ Fonctionnalités principales

### 🔐 Authentification et sécurité

- **Authentification robuste** : Système de connexion sécurisé avec hashage des mots de passe
- **Authentification multifacteur (MFA)** : Activation optionnelle de 2FA via code TOTP pour une protection renforcée
- **Gestion des sessions** : Sessions Flask sécurisées avec support de déconnexion
- **Réinitialisation de mot de passe** : Processus sécurisé par email avec jeton temporaire
- **Vérification d'email** : Confirmation du compte par email (stub configurable)

### 👥 Système de rôles avancé

L'application supporte quatre rôles distincts, chacun avec ses permissions et son interface personnalisée :

#### 1. **Ingénieur (engineer)** 👷
L'acteur principal du système, responsable de la création et du pilotage des affaires :
- ✅ **Créer des affaires** : Initialiser de nouveaux dossiers d'acquisition avec tous les détails (titre, description, type de prestation, dates, budget, etc.)
- ✅ **Éditer les affaires** : Modifier les paramètres d'une affaire en cours
- ✅ **Consulter toutes les affaires** : Vue complète des affaires créées
- ✅ **Signature numérique** : Signer numériquement les devis avec un tampon personnalisé
- ✅ **Gestion de la signature** : Configurer son profil de signature (nom, prénom, fonction, tampon personnel)
- ✅ **Historique des modifications** : Suivre les changements apportés aux affaires
- ✅ **Export PDF** : Générer des exports complets des affaires en PDF
- ✅ **Visualisation des documents** : Consulter les documents téléversés par les autres acteurs

#### 2. **Acheteur (buyer)** 🛒
Responsable de l'approvisionnement et de la validation des commandes :
- ✅ **Consulter les affaires** : Accéder à tous les dossiers du système
- ✅ **Téléverser les documents** : Ajouter les bons de commande et bons de réception aux affaires
- ✅ **Suivre le statut** : Visualiser l'avancement de chaque affaire (En attente → En cours → Terminé)
- ✅ **Historique complet** : Consulter l'évolution de chaque dossier

#### 3. **Fournisseur (supplier)** 🏭
Acteur externe participant à la procédure d'acquisition :
- ✅ **Téléverser les devis** : Soumettre les devis correspondant à sa d'email
- ✅ **Consulter ses affaires** : Voir uniquement les affaires le concernant (filtrées par email)
- ✅ **S'inscrire autonomement** : Création de compte via le formulaire d'inscription public
- ✅ **Visualiser les documents** : Consulter les réponses des acheteurs

#### 4. **Administrateur (admin)** 🔧
Gestionnaire du système avec accès complet :
- ✅ **Gestion des utilisateurs** : CRUD complet (créer, éditer, supprimer les comptes)
- ✅ **Gestion des affaires** : Administration complète des dossiers
- ✅ **Gestion des UFs** : Maintenir la liste des unités fonctionnelles du GHT
- ✅ **Gestion des comptes budgétaires** : Configurer les numéros de compte comptables disponibles
- ✅ **Gestion des codes projets** : Administrer les codes projets d'investissement
- ✅ **Tableau de bord admin** : Vue d'ensemble du système

### 📄 Gestion des affaires et documents

#### Cycle de vie des affaires :
1. **Création** : L'ingénieur crée une nouvelle affaire avec tous les paramètres (type, fournisseur, budget, etc.)
2. **Mise à jour** : Modification des détails de l'affaire selon les besoins
3. **Acquisition du devis** : Le fournisseur téléverse son devis
4. **Signature du devis** : L'ingénieur signe numériquement le devis
5. **Bon de commande** : L'acheteur ajoute le bon de commande
6. **Réception** : L'acheteur téléverse le bon de réception signé
7. **Signature réception** : L'ingénieur signe le bon de réception
8. **Conclusion** : L'affaire passe au statut "Terminée"

#### Types de documents gérés :
- **Devis** : Proposition tarifaire du fournisseur, signée numériquement par l'ingénieur
- **Bon de commande** : Document d'engagement téléversé par l'acheteur
- **Bon de réception** : Document de conclusion des services/livraisons

#### Opérations sur les documents :
- 📥 **Téléversement** : Upload sécurisé de fichiers PDF avec validation
- 👁️ **Visualisation** : Aperçu direct des PDFs dans l'interface
- ✍️ **Signature numérique** : Application de tampon et signature de l'ingénieur sur les devis
- 🗑️ **Suppression** : Retrait des documents avec confirmation
- 📊 **Suivi** : Historique complet des modifications

### 🎯 Fonctionnalités avancées

#### Configuration de la signature numérique
- Upload d'un tampon personnel (image PNG, JPG, JPEG)
- Stockage sécurisé des signatures
- Suppression et réinitialisation de la signature
- Historique des modifications de signature

#### Paramétrage des affaires
- **Types de prestation** : Fournitures informatiques, téléphoniques, logiciels, maintenance, liaisons, téléphonie, abonnements, prestations
- **Comptes budgétaires** : Accès à un dictionnaire complet des comptes budgétaires du GHT (budget exploitation et investissement)
- **Codes projets** : Sélection parmi 50+ codes projets d'investissement et d'amélioration qualité
- **Unités fonctionnelles** : Plus de 200 UFs disponibles du GHT ADS
- **Termes de facturation** : Configuration flexible des conditions de paiement (sur livraison, sur commande, etc.)

#### Recherche et tri
- **Recherche textuelle** : Filtrage par titre, type, emails, statut de l'affaire
- **Tri dynamique** : Par titre, date d'ouverture, date de fermeture, statut
- **Navigation fluide** : Interface intuitive avec pagination et alertes

#### Conformité RGPD
- 🔒 **Page de confidentialité** : Information complète sur l'utilisation des données
- 📋 **Gestion des consentements** : Interface de gestion des préférences utilisateur
- 💾 **Export des données** : Les utilisateurs peuvent exporter toutes leurs données personnelles en PDF
- 🗑️ **Droit à l'oubli** : Suppression complète du compte avec confirmation en deux étapes
- ✅ **Audit trail** : Historique d'accès aux données sensibles

### 📧 Notifications par email
- Configuration SMTP flexible pour les notifications d'événements
- Support Gmail, Outlook et autres fournisseurs SMTP
- Mode stub (développement) : Les emails sont enregistrés dans les logs
- Notifications de : réinitialisation de mot de passe, vérification d'email, événements d'affaires

### 💾 Stockage et persistance
- **Base de données SQLite** : Stockage fiable des métadonnées
- **Système de fichiers** : Stockage sécurisé des PDF uploadés
- **Structure organisée** : Dossiers `/uploads` pour les documents, `/data` pour la base de données

## 📊 Flux de travail par rôle

### Workflow pour l'Ingénieur
```
Connexion → Tableau de bord personnel
    ↓
Créer nouvelle affaire (titre, description, type, fournisseur, budget, etc.)
    ↓
Configurer sa signature numérique (nom, prénom, fonction, tampon)
    ↓
Réceptionner les devis du fournisseur
    ↓
Signer numériquement le devis choisi
    ↓
Suivre l'avancement (devis signé → bon de commande → réception)
    ↓
Signer le bon de réception final
    ↓
Affaire terminée !
```

### Workflow pour l'Acheteur
```
Connexion → Tableau de bord de toutes les affaires
    ↓
Consulter les affaires en cours
    ↓
Téléverser un bon de commande (une fois le devis signé)
    ↓
Téléverser le bon de réception (livraison effectuée)
    ↓
Attendre la signature finale de l'ingénieur
```

### Workflow pour le Fournisseur
```
S'inscrire (formulaire public accessible)
    ↓
Connexion avec ses identifiants
    ↓
Consulter les affaires le concernant (filtrées par email)
    ↓
Téléverser le devis pour chaque affaire
    ↓
Suivre l'évolution (attente de signature, etc.)
```

### Workflow pour l'Administrateur
```
Connexion → Tableau de bord admin
    ↓
Gestion des utilisateurs (CRUD, changement de rôles)
    ↓
Gestion des affaires (édition/suppression administrative)
    ↓
Configuration du système :
   • Unités fonctionnelles (UF)
   • Comptes budgétaires comptables
   • Codes projets d'investissement
    ↓
Surveillance du système
```

## 📋 Paramètres configurables

### Comptes budgétaires disponibles
- **Budget Exploitation** : H606253, H606254, H612221, H613251, H6151610, etc. (48 comptes)
- **Budget CFPS** : C61351, C61554, C615261, etc. (7 comptes)
- **Budget GHT** : G6151610, G615254, G6152610, etc. (9 comptes)
- **Budget Investissement** : H2051205, H2051206, H2052000, H21832106, etc. (15 comptes)

### Codes projets (50+)
- Projets SI : Cybersécurité, Infrastructure réseau, PARC info, SSO, GMAO, Pharmacie, etc.
- Projets transversaux : Vaccination HPV, Lieu de Santé Sans Tabac, Pensée Plus
- Dotations et investissements : 2025 HPR Sisteron, HELISTATION, Scanner 2, etc.

### Types de prestations
- Fournitures informatiques
- Fournitures téléphoniques
- Logiciels
- Location informatique
- Maintenance
- Entreposage/réparation matériel
- Liaisons informatiques
- Téléphonie
- Abonnements
- Prestations

## 📁 Structure du projet

```
.
├── data/                           # Base de données SQLite
│   └── app.db                     # Fichier base de données principal
├── docker/                         # Configuration Docker et Nginx
│   └── nginx.conf                 # Configuration serveur Nginx
├── uploads/                        # Stockage sécurisé des fichiers
│   ├── PDF uploadés par les utilisateurs
│   ├── Tampons de signature
│   └── Autres ressources
├── logs/                          # Journaux d'application
├── src/                           # Code source Flask
│   ├── app.py                     # Application principale (1900+ lignes)
│   ├── __init__.py               # Initialisation du package
│   ├── static/                    # Fichiers statiques
│   │   └── style.css             # Styles CSS personnalisés
│   └── templates/                 # 30+ Templates Jinja2
│       ├── Authentification       # login, register, verify, reset password
│       ├── Utilisateur            # dashboard, signature settings
│       ├── Affaires              # case_form, case_detail, case_changelog
│       ├── Documents             # upload, viewer, signature interface
│       ├── RGPD                  # privacy, gdpr_consents, gdpr_export
│       └── Administration        # admin dashboard, gestion users/cases/accounts
├── tests/                         # Suite de tests (à développer)
├── requirements.txt               # Dépendances Python
├── Dockerfile                     # Configuration Docker
├── docker-compose.yml             # Orchestration services
├── .env.example                   # Modèle variables d'environnement
├── .gitignore                     # Exclusions Git
├── .dockerignore                  # Exclusions Docker
├── README.md                      # Ce fichier
└── .github/
    └── copilot-instructions.md   # Instructions de développement Copilot
```

## 🚀 Installation locale

### Prérequis
- Python 3.8+ (recommandé 3.11+)
- pip ou pipenv pour la gestion des dépendances
- Git pour le contrôle de version

### Étapes d'installation

1. **Clonez ou téléchargez le projet** :
   ```bash
   git clone <repository-url>
   cd Documents/dev
   ```

2. **Créez un environnement virtuel Python** :
   ```bash
   python -m venv .venv
   ```

3. **Activez l'environnement virtuel** :
   
   **Sur Linux/macOS** :
   ```bash
   source .venv/bin/activate
   ```
   
   **Sur Windows** :
   ```bash
   .venv\Scripts\activate
   ```

4. **Installez les dépendances du projet** :
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurez les variables d'environnement** (optionnel) :
   
   Créez un fichier `.env` à la racine :
   ```env
   SECRET_KEY=your-secret-key-change-in-production
   DATABASE_PATH=data/app.db
   UPLOAD_FOLDER=uploads
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

6. **Lancez l'application** :
   ```bash
   python src/app.py
   ```
   
   Accédez à : **http://127.0.0.1:8000**

## 🐳 Exécution avec Docker

### Prérequis
- Docker Engine (19.03+)
- Docker Compose (1.25+)

### Démarrage

1. **Construisez les conteneurs** :
   ```bash
   docker compose build
   ```

2. **Démarrez les services** :
   ```bash
   docker compose up -d
   ```

3. **Accédez à l'application** :
   **http://localhost:8080**

4. **Arrêtez les services** :
   ```bash
   docker compose down
   ```

## 👤 Comptes de démonstration

| Rôle | Identifiant | Mot de passe | Accès |
|------|-------------|--------------|-------|
| Ingénieur | `engineer` | `password` | Création affaires, signature |
| Acheteur | `buyer` | `password` | Bons de commande/réception |
| Fournisseur | `supplier` | `password` | Soumission de devis |
| Admin | Créé manuellement | - | Gestion système complète |

Les fournisseurs peuvent aussi s'inscrire librement via `/register`.

## 📧 Configuration des emails

### Mode développement
Les emails sont simulés et enregistrés dans les logs de l'application.

### Mode production - Gmail

1. **Activez 2FA** sur votre compte Google
2. **Générez un App Password** : 
   - Connectez-vous à Google Account
   - Allez dans Security > App Passwords
   - Générez un mot de passe spécifique pour cette application
3. **Configurez le fichier .env** :
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=votre.email@gmail.com
   MAIL_PASSWORD=votre-app-password
   MAIL_DEFAULT_SENDER=votre.email@gmail.com
   ```

### Configuration d'autres fournisseurs

**Outlook** :
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=votre@domaine.com
MAIL_PASSWORD=votre-mot-de-passe
```

**SSL direct (port 465)** :
```env
MAIL_SERVER=smtp.votreprovider.com
MAIL_PORT=465
MAIL_USE_SSL=true
MAIL_USE_TLS=false
```

## 🔒 Sécurité et bonnes pratiques

### ✅ Implémentées
- ✓ Authentification robuste (hashage Werkzeug)
- ✓ Sessions chiffrées Flask
- ✓ Protection CSRF (Flask-WTF)
- ✓ MFA optionnelle (TOTP)
- ✓ Validation fichiers (extensions, noms sécurisés)
- ✓ RGPD complet (export, suppression, consentements)
- ✓ Téléversement sécurisé de fichiers
- ✓ Signatures numériques avec tampons

### ⚠️ Production checklist
- [ ] Changez `SECRET_KEY` dans `.env`
- [ ] Utilisez HTTPS avec un certificat SSL/TLS
- [ ] Configurez une base de données production (PostgreSQL)
- [ ] Activez les logs de sécurité
- [ ] Testez MFA et notifications email
- [ ] Configurez un proxy SMTP fiable
- [ ] Configurez les backups réguliers
- [ ] Limitez les uploads à une taille maximale
- [ ] Activez les rate limiting sur les routes d'authentification

## 📝 Notes techniques

- **Fichiers PDF** : Stockés dans `uploads/` avec noms UUID sécurisés
- **Base de données** : SQLite stockée dans `data/app.db`
- **Nginx** : Accessible sur le port `8080` en Docker
- **Logs** : Disponibles via `docker compose logs -f app`
- **Tampons de signature** : Images PNG/JPG stockées de manière sécurisée
- **Sessions** : Chiffrées et stockées côté serveur
- **Mots de passe** : Hashés avec Werkzeug.security (pbkdf2)

## 🤝 Contribution

Pour contribuer à ce projet :
1. Consultez `.github/copilot-instructions.md` pour les conventions de code
2. Testez vos changements en local avant de pousser
3. Documentez toute nouvelle fonctionnalité
4. Respectez le cycle de vie des affaires et les rôles utilisateurs

## 📄 Licence

Proprietary - GHT Alpes du Sud

## ❓ Support

Pour toute question ou problème, contactez l'équipe de développement du GHT ADS.

---

**Dernière mise à jour** : Avril 2026
**Version** : 1.0
**Statut** : Production-Ready
