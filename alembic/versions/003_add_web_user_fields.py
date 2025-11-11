"""Add email and password_hash for web users

Revision ID: 003_add_web_user_fields
Revises: 002_add_role_field
Create Date: 2025-11-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_web_user_fields'
down_revision = '002_add_role_field'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add email and password_hash columns to users table for web authentication.

    These fields are used by the FastAPI web interface for user authentication.
    Telegram users don't need these fields (they remain NULL).
    """
    # Add email column
    op.add_column(
        'users',
        sa.Column(
            'email',
            sa.String(),
            nullable=True  # NULL for telegram users
        )
    )

    # Add password_hash column
    op.add_column(
        'users',
        sa.Column(
            'password_hash',
            sa.String(),
            nullable=True  # NULL for telegram users
        )
    )

    # Add unique constraint on email (but allow NULL)
    op.create_index(
        'ix_users_email',
        'users',
        ['email'],
        unique=True,
        postgresql_where=sa.text('email IS NOT NULL')
    )

    print("✅ Added 'email' and 'password_hash' columns to users table")
    print("   These fields are for web users only (NULL for Telegram users)")
    print("   Unique index created on email (excluding NULLs)")


def downgrade() -> None:
    """
    Remove email and password_hash columns from users table.
    """
    # Remove index first
    op.drop_index('ix_users_email', table_name='users')

    # Remove columns
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')

    print("⚠️  Removed 'email' and 'password_hash' columns from users table")
