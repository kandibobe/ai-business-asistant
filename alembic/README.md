# Database Migrations with Alembic

This directory contains Alembic database migration scripts for the AI Business Assistant.

## Quick Start

### Initial Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database:**
   - Copy `.env.example` to `.env`
   - Set your database credentials (DB_HOST, DB_USER, DB_PASS, DB_NAME)

3. **Run initial migration:**
   ```bash
   alembic upgrade head
   ```

## Common Commands

### Check current database version
```bash
alembic current
```

### View migration history
```bash
alembic history --verbose
```

### Upgrade to latest version
```bash
alembic upgrade head
```

### Upgrade one version
```bash
alembic upgrade +1
```

### Downgrade one version
```bash
alembic downgrade -1
```

### Downgrade to specific version
```bash
alembic downgrade <revision_id>
```

### Create new migration (auto-generate)
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Create new migration (empty template)
```bash
alembic revision -m "Description of changes"
```

## Migration Files

Migrations are stored in `alembic/versions/` directory.

### Current Migrations:

1. **001_initial_schema.py** - Initial database schema
   - Creates users, documents, and sessions tables
   - Sets up indexes and foreign keys

## Best Practices

### Creating Migrations

1. **Always review auto-generated migrations** - Alembic's autogenerate is smart but not perfect
2. **Test migrations** - Run upgrade and downgrade in development first
3. **One logical change per migration** - Don't mix unrelated changes
4. **Write descriptive messages** - Make it clear what the migration does

### Example: Adding a new column

```bash
# 1. Create migration
alembic revision --autogenerate -m "Add avatar_url to users"

# 2. Review the generated file in alembic/versions/
# 3. Test upgrade
alembic upgrade head

# 4. Test downgrade (in dev only!)
alembic downgrade -1
alembic upgrade head
```

### Example: Modifying existing data

For data migrations (not just schema changes), create an empty migration:

```bash
alembic revision -m "Migrate user roles"
```

Then manually write the upgrade/downgrade logic:

```python
def upgrade() -> None:
    # Update existing data
    op.execute("""
        UPDATE users
        SET ai_role = 'consultant'
        WHERE is_premium = true
    """)

def downgrade() -> None:
    # Reverse the changes
    op.execute("""
        UPDATE users
        SET ai_role = 'assistant'
        WHERE is_premium = true
    """)
```

## Production Deployment

### Safe deployment workflow:

1. **Backup database** before running migrations
   ```bash
   pg_dump -U ai_bot_user ai_bot_db > backup_$(date +%Y%m%d).sql
   ```

2. **Test migrations in staging** environment first

3. **Run migrations** in production:
   ```bash
   alembic upgrade head
   ```

4. **Verify** database state:
   ```bash
   alembic current
   ```

### Rollback procedure:

If something goes wrong:

```bash
# Downgrade to previous version
alembic downgrade -1

# Or downgrade to specific version
alembic downgrade <previous_revision_id>

# Restore from backup if needed
psql -U ai_bot_user ai_bot_db < backup_20250110.sql
```

## Troubleshooting

### "Can't locate revision identified by 'xxxx'"

The database version doesn't match migration files. Usually happens when:
- Migrations were deleted
- Database was created manually
- Working with multiple branches

**Solution:**
```bash
# Stamp database with current version
alembic stamp head
```

### "Target database is not up to date"

You're behind on migrations.

**Solution:**
```bash
alembic upgrade head
```

### Autogenerate doesn't detect changes

Alembic compares metadata to database. If it's not detecting changes:

1. Ensure your models are imported in `alembic/env.py`
2. Check that SQLAlchemy metadata is correctly defined
3. Use `--autogenerate` flag when creating revision

### Merge conflicts in migrations

When working with multiple branches:

1. Don't merge conflicting migrations - create a merge migration:
   ```bash
   alembic merge -m "merge branches" head1 head2
   ```

2. Or rebase and re-create migrations in order

## Environment Variables

Required in `.env`:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_USER=ai_bot_user
DB_PASS=your_password
DB_NAME=ai_bot_db
```

## Architecture

```
alembic/
├── env.py              # Alembic environment configuration
├── script.py.mako      # Template for new migrations
├── versions/           # Migration scripts
│   └── 001_initial_schema.py
└── README.md          # This file
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
