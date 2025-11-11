"""
Role-Based Access Control (RBAC) system.

Provides fine-grained permissions and role management for users.
Supports multiple roles, permissions, and resource-level access control.
"""
import logging
from enum import Enum
from typing import List, Set, Optional, Dict, Any
from dataclasses import dataclass, field
from functools import wraps

logger = logging.getLogger(__name__)


class Permission(str, Enum):
    """
    System permissions.

    Each permission grants access to a specific feature or resource.
    """
    # Document permissions
    DOCUMENT_VIEW = "document:view"
    DOCUMENT_UPLOAD = "document:upload"
    DOCUMENT_DELETE = "document:delete"
    DOCUMENT_EXPORT = "document:export"
    DOCUMENT_SHARE = "document:share"

    # AI permissions
    AI_QUERY = "ai:query"
    AI_ADVANCED_MODE = "ai:advanced_mode"
    AI_CUSTOM_PROMPTS = "ai:custom_prompts"

    # Analytics permissions
    ANALYTICS_VIEW_OWN = "analytics:view_own"
    ANALYTICS_VIEW_ALL = "analytics:view_all"
    ANALYTICS_EXPORT = "analytics:export"

    # Admin permissions
    ADMIN_USERS_VIEW = "admin:users:view"
    ADMIN_USERS_EDIT = "admin:users:edit"
    ADMIN_USERS_DELETE = "admin:users:delete"
    ADMIN_SETTINGS = "admin:settings"
    ADMIN_LOGS = "admin:logs"

    # API permissions
    API_ACCESS = "api:access"
    API_WEBHOOKS = "api:webhooks"

    # Rate limits (special permissions that affect quotas)
    RATE_STANDARD = "rate:standard"
    RATE_PREMIUM = "rate:premium"
    RATE_UNLIMITED = "rate:unlimited"


class Role(str, Enum):
    """
    User roles with predefined permission sets.
    """
    # Basic user roles
    GUEST = "guest"           # Limited read-only access
    FREE = "free"             # Standard free tier
    PREMIUM = "premium"       # Paid subscription
    BUSINESS = "business"     # Business plan

    # Admin roles
    MODERATOR = "moderator"   # Can moderate content
    ADMIN = "admin"           # Full system access
    SUPERADMIN = "superadmin" # Unrestricted access


@dataclass
class RoleDefinition:
    """
    Role definition with permissions and limits.
    """
    name: Role
    display_name: str
    description: str
    permissions: Set[Permission]

    # Rate limits (requests per minute)
    rate_limit_per_minute: int = 30

    # Document limits
    max_documents: int = 100
    max_file_size_mb: int = 50

    # AI limits
    max_ai_tokens_per_day: int = 100000
    max_context_length: int = 50000

    # Feature flags
    can_export: bool = False
    can_use_api: bool = False
    can_use_webhooks: bool = False

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


# ==================== Role Definitions ====================

ROLE_DEFINITIONS: Dict[Role, RoleDefinition] = {
    Role.GUEST: RoleDefinition(
        name=Role.GUEST,
        display_name="Guest",
        description="Limited read-only access for trial",
        permissions={
            Permission.DOCUMENT_VIEW,
            Permission.AI_QUERY,
            Permission.ANALYTICS_VIEW_OWN,
            Permission.RATE_STANDARD,
        },
        rate_limit_per_minute=10,
        max_documents=5,
        max_file_size_mb=10,
        max_ai_tokens_per_day=10000,
        max_context_length=10000,
    ),

    Role.FREE: RoleDefinition(
        name=Role.FREE,
        display_name="Free",
        description="Standard free tier with basic features",
        permissions={
            Permission.DOCUMENT_VIEW,
            Permission.DOCUMENT_UPLOAD,
            Permission.DOCUMENT_DELETE,
            Permission.AI_QUERY,
            Permission.ANALYTICS_VIEW_OWN,
            Permission.RATE_STANDARD,
        },
        rate_limit_per_minute=30,
        max_documents=50,
        max_file_size_mb=20,
        max_ai_tokens_per_day=50000,
        max_context_length=50000,
    ),

    Role.PREMIUM: RoleDefinition(
        name=Role.PREMIUM,
        display_name="Premium",
        description="Premium subscription with advanced features",
        permissions={
            Permission.DOCUMENT_VIEW,
            Permission.DOCUMENT_UPLOAD,
            Permission.DOCUMENT_DELETE,
            Permission.DOCUMENT_EXPORT,
            Permission.DOCUMENT_SHARE,
            Permission.AI_QUERY,
            Permission.AI_ADVANCED_MODE,
            Permission.AI_CUSTOM_PROMPTS,
            Permission.ANALYTICS_VIEW_OWN,
            Permission.ANALYTICS_EXPORT,
            Permission.API_ACCESS,
            Permission.RATE_PREMIUM,
        },
        rate_limit_per_minute=100,
        max_documents=500,
        max_file_size_mb=50,
        max_ai_tokens_per_day=500000,
        max_context_length=100000,
        can_export=True,
        can_use_api=True,
    ),

    Role.BUSINESS: RoleDefinition(
        name=Role.BUSINESS,
        display_name="Business",
        description="Business plan with team features",
        permissions={
            Permission.DOCUMENT_VIEW,
            Permission.DOCUMENT_UPLOAD,
            Permission.DOCUMENT_DELETE,
            Permission.DOCUMENT_EXPORT,
            Permission.DOCUMENT_SHARE,
            Permission.AI_QUERY,
            Permission.AI_ADVANCED_MODE,
            Permission.AI_CUSTOM_PROMPTS,
            Permission.ANALYTICS_VIEW_OWN,
            Permission.ANALYTICS_VIEW_ALL,
            Permission.ANALYTICS_EXPORT,
            Permission.API_ACCESS,
            Permission.API_WEBHOOKS,
            Permission.RATE_PREMIUM,
        },
        rate_limit_per_minute=200,
        max_documents=5000,
        max_file_size_mb=100,
        max_ai_tokens_per_day=2000000,
        max_context_length=200000,
        can_export=True,
        can_use_api=True,
        can_use_webhooks=True,
    ),

    Role.MODERATOR: RoleDefinition(
        name=Role.MODERATOR,
        display_name="Moderator",
        description="Can moderate user content",
        permissions={
            # All premium permissions
            *ROLE_DEFINITIONS.get(Role.PREMIUM, RoleDefinition(
                name=Role.PREMIUM,
                display_name="",
                description="",
                permissions=set()
            )).permissions,
            # Plus moderator permissions
            Permission.ADMIN_USERS_VIEW,
            Permission.ADMIN_LOGS,
            Permission.RATE_UNLIMITED,
        },
        rate_limit_per_minute=500,
        max_documents=10000,
        max_file_size_mb=200,
        max_ai_tokens_per_day=10000000,
        max_context_length=500000,
        can_export=True,
        can_use_api=True,
        can_use_webhooks=True,
    ),

    Role.ADMIN: RoleDefinition(
        name=Role.ADMIN,
        display_name="Administrator",
        description="Full system access",
        permissions=set(Permission),  # All permissions
        rate_limit_per_minute=1000,
        max_documents=100000,
        max_file_size_mb=500,
        max_ai_tokens_per_day=100000000,
        max_context_length=1000000,
        can_export=True,
        can_use_api=True,
        can_use_webhooks=True,
    ),

    Role.SUPERADMIN: RoleDefinition(
        name=Role.SUPERADMIN,
        display_name="Super Administrator",
        description="Unrestricted access to all features",
        permissions=set(Permission),  # All permissions
        rate_limit_per_minute=0,  # Unlimited
        max_documents=0,  # Unlimited
        max_file_size_mb=0,  # Unlimited
        max_ai_tokens_per_day=0,  # Unlimited
        max_context_length=0,  # Unlimited
        can_export=True,
        can_use_api=True,
        can_use_webhooks=True,
    ),
}


# Fix circular reference for MODERATOR
if Role.MODERATOR in ROLE_DEFINITIONS and Role.PREMIUM in ROLE_DEFINITIONS:
    ROLE_DEFINITIONS[Role.MODERATOR].permissions = {
        *ROLE_DEFINITIONS[Role.PREMIUM].permissions,
        Permission.ADMIN_USERS_VIEW,
        Permission.ADMIN_LOGS,
        Permission.RATE_UNLIMITED,
    }


class RBACService:
    """
    RBAC Service for permission checking.
    """

    @staticmethod
    def get_role_definition(role: Role) -> RoleDefinition:
        """
        Get role definition by role enum.

        Args:
            role: Role enum

        Returns:
            RoleDefinition: Role definition

        Raises:
            ValueError: If role not found
        """
        if role not in ROLE_DEFINITIONS:
            raise ValueError(f"Unknown role: {role}")
        return ROLE_DEFINITIONS[role]

    @staticmethod
    def has_permission(role: Role, permission: Permission) -> bool:
        """
        Check if role has a specific permission.

        Args:
            role: User's role
            permission: Permission to check

        Returns:
            bool: True if role has permission
        """
        try:
            role_def = RBACService.get_role_definition(role)
            return permission in role_def.permissions
        except ValueError:
            logger.warning(f"Unknown role: {role}")
            return False

    @staticmethod
    def has_any_permission(role: Role, permissions: List[Permission]) -> bool:
        """
        Check if role has any of the specified permissions.

        Args:
            role: User's role
            permissions: List of permissions to check

        Returns:
            bool: True if role has at least one permission
        """
        return any(RBACService.has_permission(role, perm) for perm in permissions)

    @staticmethod
    def has_all_permissions(role: Role, permissions: List[Permission]) -> bool:
        """
        Check if role has all of the specified permissions.

        Args:
            role: User's role
            permissions: List of permissions to check

        Returns:
            bool: True if role has all permissions
        """
        return all(RBACService.has_permission(role, perm) for perm in permissions)

    @staticmethod
    def get_rate_limit(role: Role) -> int:
        """
        Get rate limit for role.

        Args:
            role: User's role

        Returns:
            int: Rate limit per minute (0 = unlimited)
        """
        try:
            role_def = RBACService.get_role_definition(role)
            return role_def.rate_limit_per_minute
        except ValueError:
            return 30  # Default to free tier limit

    @staticmethod
    def get_max_file_size(role: Role) -> int:
        """
        Get max file size for role in MB.

        Args:
            role: User's role

        Returns:
            int: Max file size in MB (0 = unlimited)
        """
        try:
            role_def = RBACService.get_role_definition(role)
            return role_def.max_file_size_mb
        except ValueError:
            return 20  # Default to free tier limit

    @staticmethod
    def can_upload_file_size(role: Role, file_size_bytes: int) -> bool:
        """
        Check if user can upload file of given size.

        Args:
            role: User's role
            file_size_bytes: File size in bytes

        Returns:
            bool: True if allowed
        """
        max_size_mb = RBACService.get_max_file_size(role)
        if max_size_mb == 0:  # Unlimited
            return True

        max_size_bytes = max_size_mb * 1024 * 1024
        return file_size_bytes <= max_size_bytes


# ==================== Decorators ====================

def require_permission(permission: Permission):
    """
    Decorator to require a specific permission.

    Usage:
        @require_permission(Permission.DOCUMENT_UPLOAD)
        async def upload_document(user_role: Role):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract role from kwargs or args
            user_role = kwargs.get('user_role') or kwargs.get('role')

            if user_role is None:
                # Try to find role in args (assuming it's a User object or Role)
                for arg in args:
                    if isinstance(arg, Role):
                        user_role = arg
                        break
                    elif hasattr(arg, 'role'):
                        user_role = arg.role
                        break

            if user_role is None:
                raise PermissionError("User role not found in function arguments")

            if not RBACService.has_permission(user_role, permission):
                raise PermissionError(
                    f"Permission denied. Required permission: {permission.value}"
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


def require_any_permission(*permissions: Permission):
    """
    Decorator to require any of the specified permissions.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role = kwargs.get('user_role') or kwargs.get('role')

            if user_role is None:
                for arg in args:
                    if isinstance(arg, Role):
                        user_role = arg
                        break
                    elif hasattr(arg, 'role'):
                        user_role = arg.role
                        break

            if user_role is None:
                raise PermissionError("User role not found in function arguments")

            if not RBACService.has_any_permission(user_role, list(permissions)):
                perm_names = ", ".join(p.value for p in permissions)
                raise PermissionError(
                    f"Permission denied. Required one of: {perm_names}"
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


def require_role(role: Role):
    """
    Decorator to require a specific role or higher.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role = kwargs.get('user_role') or kwargs.get('role')

            if user_role is None:
                for arg in args:
                    if isinstance(arg, Role):
                        user_role = arg
                        break
                    elif hasattr(arg, 'role'):
                        user_role = arg.role
                        break

            if user_role is None:
                raise PermissionError("User role not found in function arguments")

            # Simple role hierarchy check
            role_hierarchy = [
                Role.GUEST,
                Role.FREE,
                Role.PREMIUM,
                Role.BUSINESS,
                Role.MODERATOR,
                Role.ADMIN,
                Role.SUPERADMIN
            ]

            if user_role not in role_hierarchy or role not in role_hierarchy:
                raise PermissionError(f"Invalid role: {user_role}")

            if role_hierarchy.index(user_role) < role_hierarchy.index(role):
                raise PermissionError(
                    f"Insufficient role. Required: {role.value} or higher"
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


# ==================== Usage Example ====================

if __name__ == "__main__":
    """
    Test RBAC system.

    Run: python -m services.rbac
    """
    print("=" * 60)
    print("🔒 Testing RBAC System")
    print("=" * 60)

    # Test permissions
    print("\n📋 Permission Tests:")
    print(f"   Free user can upload: {RBACService.has_permission(Role.FREE, Permission.DOCUMENT_UPLOAD)}")
    print(f"   Free user can export: {RBACService.has_permission(Role.FREE, Permission.DOCUMENT_EXPORT)}")
    print(f"   Premium user can export: {RBACService.has_permission(Role.PREMIUM, Permission.DOCUMENT_EXPORT)}")
    print(f"   Admin can edit users: {RBACService.has_permission(Role.ADMIN, Permission.ADMIN_USERS_EDIT)}")

    # Test rate limits
    print("\n⏱️  Rate Limits:")
    for role in [Role.FREE, Role.PREMIUM, Role.BUSINESS, Role.ADMIN]:
        limit = RBACService.get_rate_limit(role)
        print(f"   {role.value}: {limit if limit > 0 else 'Unlimited'} req/min")

    # Test file size limits
    print("\n📦 File Size Limits:")
    for role in [Role.FREE, Role.PREMIUM, Role.BUSINESS]:
        max_size = RBACService.get_max_file_size(role)
        print(f"   {role.value}: {max_size if max_size > 0 else 'Unlimited'} MB")

    # Test role definitions
    print("\n👥 Role Definitions:")
    for role in [Role.FREE, Role.PREMIUM, Role.ADMIN]:
        role_def = RBACService.get_role_definition(role)
        print(f"\n   {role_def.display_name}:")
        print(f"      {role_def.description}")
        print(f"      Permissions: {len(role_def.permissions)}")
        print(f"      Max Documents: {role_def.max_documents if role_def.max_documents > 0 else 'Unlimited'}")

    print("\n" + "=" * 60)
    print("✅ RBAC tests completed!")
    print("=" * 60)
