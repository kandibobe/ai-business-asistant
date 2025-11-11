"""Add role field to users table for RBAC

Revision ID: 002_add_role_field
Revises: 001_initial_schema
Create Date: 2025-11-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_role_field'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add role column to users table for Role-Based Access Control.

    Default role is 'free' for existing users.
    """
    # Add role column with default value
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(),
            nullable=False,
            server_default='free'
        )
    )

    # Add index for faster role-based queries
    op.create_index(
        'ix_users_role',
        'users',
        ['role'],
        unique=False
    )

    print("✅ Added 'role' column to users table")
    print("   Default role: 'free'")
    print("   Index created: ix_users_role")


def downgrade() -> None:
    """
    Remove role column from users table.
    """
    # Remove index first
    op.drop_index('ix_users_role', table_name='users')

    # Remove column
    op.drop_column('users', 'role')

    print("⚠️  Removed 'role' column from users table")
