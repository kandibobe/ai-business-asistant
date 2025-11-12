#!/bin/bash
# ==============================================================================
# PostgreSQL Automated Backup Script
# ==============================================================================
# This script creates compressed backups of PostgreSQL database
# with automatic cleanup of old backups (keeps last 30 days)
# ==============================================================================

set -e

# Configuration
BACKUP_DIR="/backups"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER}"
DB_PASS="${DB_PASS}"
DB_NAME="${DB_NAME}"
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "=========================================="
echo "Starting PostgreSQL Backup"
echo "=========================================="
echo "Database: $DB_NAME"
echo "Host: $DB_HOST"
echo "Timestamp: $TIMESTAMP"
echo "=========================================="

# Set password for pg_dump
export PGPASSWORD="$DB_PASS"

# Create backup with compression
echo "Creating backup..."
pg_dump -h "$DB_HOST" \
        -p "$DB_PORT" \
        -U "$DB_USER" \
        -d "$DB_NAME" \
        --verbose \
        --format=plain \
        --no-owner \
        --no-acl \
        | gzip > "$BACKUP_FILE"

# Check if backup was successful
if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✅ Backup completed successfully!"
    echo "   File: $BACKUP_FILE"
    echo "   Size: $BACKUP_SIZE"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Clean up old backups
echo "=========================================="
echo "Cleaning up old backups (>$RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete
echo "✅ Cleanup completed!"

# List current backups
echo "=========================================="
echo "Current backups:"
ls -lh "$BACKUP_DIR"/*.sql.gz 2>/dev/null || echo "No backups found"
echo "=========================================="

# Unset password
unset PGPASSWORD

echo "✅ Backup process completed successfully!"
