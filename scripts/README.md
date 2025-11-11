# 🛠️ Utility Scripts

Collection of utility scripts for project maintenance and database management.

---

## 📋 Available Scripts

### Database Migration Scripts

#### `migrate_db.py`
Main database migration script.

**Usage:**
```bash
python scripts/migrate_db.py
```

**Purpose:** Migrates existing database schema to add new fields (language, mode, etc.)

---

#### `migrate_documents.py`
Migrate document data structure.

**Usage:**
```bash
python scripts/migrate_documents.py
```

---

#### `migrate_language.py`
Migrate language preferences.

**Usage:**
```bash
python scripts/migrate_language.py
```

---

#### `migrate_user_preferences.py`
Migrate user preference settings.

**Usage:**
```bash
python scripts/migrate_user_preferences.py
```

---

#### `migrate_web_users.py`
Migrate web application users.

**Usage:**
```bash
python scripts/migrate_web_users.py
```

---

#### `upgrade_db.py`
Upgrade database schema to latest version using Alembic.

**Usage:**
```bash
python scripts/upgrade_db.py
```

**Purpose:** Runs Alembic migrations to update database schema

---

#### `migrate.py`
Generic migration utility.

**Usage:**
```bash
python scripts/migrate.py
```

---

### Setup & Validation Scripts

#### `check_setup.py`
Validate project setup and configuration.

**Usage:**
```bash
python scripts/check_setup.py
```

**Checks:**
- Environment variables
- Database connectivity
- Redis connectivity
- Required Python packages
- API keys validity
- File permissions

---

#### `check_dependencies.py`
Check and validate Python dependencies.

**Usage:**
```bash
python scripts/check_dependencies.py
```

**Purpose:** Verifies all required packages are installed with correct versions

---

#### `check_models.py`
Validate database models and relationships.

**Usage:**
```bash
python scripts/check_models.py
```

**Purpose:** Tests database models integrity and relationships

---

### Maintenance Scripts

#### `cleanup_project.py`
Clean up temporary files and caches.

**Usage:**
```bash
python scripts/cleanup_project.py
```

**Cleans:**
- `__pycache__` directories
- `.pyc` files
- Temporary download files
- Old log files
- Redis cache (optional)

---

#### `apply_improvements.py`
Apply code improvements and refactoring.

**Usage:**
```bash
python scripts/apply_improvements.py
```

**Purpose:** Automated code quality improvements and refactoring

---

## 🚀 Common Workflows

### Initial Setup
```bash
# 1. Check setup
python scripts/check_setup.py

# 2. Check dependencies
python scripts/check_dependencies.py

# 3. Initialize or migrate database
python scripts/migrate_db.py
```

### Database Migration
```bash
# Run main migration
python scripts/migrate_db.py

# Or use Alembic for version control
python scripts/upgrade_db.py
```

### Maintenance
```bash
# Clean project
python scripts/cleanup_project.py

# Check models
python scripts/check_models.py
```

---

## ⚠️ Important Notes

### Before Running Migration Scripts

1. **Backup your database** before running any migration scripts
2. Stop the bot and Celery workers
3. Verify configuration in `.env` file
4. Test migrations on a development database first

### Migration Order

If running multiple migrations, follow this order:

1. `migrate_db.py` - Base schema migration
2. `migrate_language.py` - Language preferences
3. `migrate_user_preferences.py` - User preferences
4. `migrate_documents.py` - Document data
5. `migrate_web_users.py` - Web users

---

## 🐛 Troubleshooting

### Script Import Errors

If you get import errors, run scripts from project root:
```bash
cd /path/to/ai-business-asistant
python scripts/script_name.py
```

### Database Connection Errors

Check your `.env` file:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=ai_bot_user
DB_PASS=your_password
DB_NAME=ai_bot_db
```

### Permission Errors

Ensure proper file permissions:
```bash
chmod +x scripts/*.py
```

---

## 📖 Documentation

For more information, see:
- [DEPLOYMENT.md](../docs/DEPLOYMENT.md) - Production deployment guide
- [MIGRATION_GUIDE.md](../docs/MIGRATION_GUIDE.md) - Detailed migration instructions
- [COMMANDS.md](../docs/COMMANDS.md) - All available commands

---

**Last Updated:** 2025-11-11
