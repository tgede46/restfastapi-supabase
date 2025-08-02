# FastAPI Supabase TODO Application

## Configuration Supabase

### 1. Création du projet Supabase

1. Allez sur [supabase.com](https://supabase.com) et créez un compte
2. Créez un nouveau projet
3. Notez les informations suivantes :
   - **Project URL** : `https://your_project_ref.supabase.co`
   - **Anon key** : Clé publique pour l'authentification côté client
   - **Service role key** : Clé privée pour les opérations administrateur
   - **Database URL** : `postgresql://postgres:[YOUR-PASSWORD]@db.your_project_ref.supabase.co:5432/postgres`

### 2. Configuration des variables d'environnement

Copiez le fichier `.env.example` vers `.env` et remplacez les valeurs :

```bash
cp .env.example .env
```

Éditez `.env` avec vos vraies clés Supabase :

```env
# Configuration Supabase
SUPABASE_DB_URL=postgresql://postgres:your_real_password@db.your_project_ref.supabase.co:5432/postgres
SUPABASE_URL=https://your_project_ref.supabase.co
SUPABASE_ANON_KEY=your_real_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_real_service_role_key

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 4. Création des tables

Les tables seront créées automatiquement au démarrage de l'application grâce à SQLModel.

### 5. Démarrage de l'application

```bash
uvicorn app.main:app --reload
```

## Endpoints disponibles

### Authentification
- `POST /api/v1/users` - Créer un utilisateur
- `POST /api/v1/auth/token` - Se connecter et obtenir un token
- `POST /api/v1/auth/forgot-password` - Demander une réinitialisation de mot de passe
- `POST /api/v1/auth/reset-password` - Réinitialiser le mot de passe

### Todos
- `POST /api/v1/todolists` - Créer une todo
- `GET /api/v1/todolists` - Obtenir toutes les todos
- `GET /api/v1/todolists/{user_id}` - Obtenir les todos d'un utilisateur
- `PUT /api/v1/todolists/{todo_id}` - Mettre à jour une todo
- `DELETE /api/v1/todolists/{todo_id}` - Supprimer une todo

## Structure du projet

```
app/
├── main.py                          # Point d'entrée de l'application
├── core/
│   ├── database.py                  # Configuration de la base de données
│   └── supabase_config.py          # Configuration Supabase
├── db/
│   └── models/
│       ├── models.py               # Modèles SQLModel
│       └── controllers/
│           ├── authentification_controllers.py
│           └── todolist_controllers.py
├── routes/
│   └── router.py                   # Routage principal
└── utils/
    └── init_db.py                  # Initialisation de la base de données
```
