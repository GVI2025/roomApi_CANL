# roomAPI

A WebAPI REST application to reserve rooms built with FastAPI and SQLAlchemy.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/roomapi.git
cd roomAPI
```

### 2. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Ensure `poetry` is available in your terminal:

```bash
poetry --version
```

### 3. Install dependencies

```bash
poetry install
```

### 4. Activate the virtual environment

```bash
poetry shell
```

### 5. Set up the database

The application uses SQLite by default (configured in `app/database/database.py`).

To create the schema, run:

```bash
alembic upgrade head
```

If needed, you can generate migrations using:

```bash
alembic revision --autogenerate -m "Initial schema"
```

### 6. Seed the database with test data

```bash
python -m app.seed.seed_data
```

### 7. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at: [http://localhost:8000](http://localhost:8000)
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Tests

```bash
poetry run test
```

---

## 📁 Project Structure

```
app/
├── api/               # API routers
├── models/            # SQLAlchemy models
├── database/          # DB session and engine
├── seed/              # Initial data seeding
├── main.py            # FastAPI app
alembic/               # Alembic migrations
```

---

## 🔧 Scripts

These scripts are defined in `pyproject.toml`:
* `poetry run test`: Run tests
* `poetry run migrate`: Apply Alembic migrations

---

## Mettre à jour la base de données après ajout du champ `commentaire`

Si vous avez ajouté le champ `commentaire` dans le modèle `Reservation`, vous devez mettre à jour la base de données.  
Voici comment faire avec Alembic :

1. Générez une nouvelle migration :
   ```bash
   alembic revision --autogenerate -m "Ajout du champ commentaire dans reservations"
   ```

2. Vérifiez le fichier de migration généré dans le dossier `alembic/versions/` et assurez-vous qu'il contient une ligne similaire à :
   ```python
   op.add_column('reservations', sa.Column('commentaire', sa.String(), nullable=True))
   ```

3. Appliquez la migration :
   ```bash
   alembic upgrade head
   ```

Votre base de données est maintenant à jour avec le champ `commentaire` dans la table `reservations`.