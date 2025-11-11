"""
Quick fix script to update .env file with proper JWT_SECRET_KEY.

Run this if you're getting JWT_SECRET_KEY validation errors.
"""
import os
import secrets
from pathlib import Path


def generate_jwt_secret():
    """Generate a secure JWT secret key (32+ chars)."""
    return secrets.token_urlsafe(48)  # Generates ~64 character string


def fix_env_file():
    """Fix .env file with proper JWT_SECRET_KEY."""
    env_path = Path('.env')
    env_example_path = Path('.env.example')

    print("=" * 60)
    print("🔧 Fixing .env file")
    print("=" * 60)

    # Check if .env exists
    if not env_path.exists():
        print("\n❌ .env file not found!")
        if env_example_path.exists():
            print("📝 Creating .env from .env.example...")
            env_path.write_text(env_example_path.read_text(encoding='utf-8'), encoding='utf-8')
            print("✅ .env file created")
        else:
            print("❌ .env.example also not found!")
            return False

    # Read .env content
    print("\n[1/3] Reading .env file...")
    content = env_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find and fix JWT_SECRET_KEY
    print("[2/3] Fixing JWT_SECRET_KEY...")
    fixed = False
    new_lines = []

    for line in lines:
        if line.strip().startswith('JWT_SECRET_KEY='):
            # Extract current value
            current_value = line.split('=', 1)[1] if '=' in line else ''

            # Check if it's the placeholder or too short
            if ('your-secret-key' in current_value or
                'change-in-production' in current_value or
                len(current_value.strip()) < 32):

                # Generate new secure key
                new_key = generate_jwt_secret()
                new_line = f'JWT_SECRET_KEY={new_key}'
                new_lines.append(new_line)
                print(f"   ✅ Generated new JWT_SECRET_KEY ({len(new_key)} chars)")
                fixed = True
            else:
                print(f"   ✅ JWT_SECRET_KEY already set ({len(current_value.strip())} chars)")
                new_lines.append(line)
        else:
            new_lines.append(line)

    # If JWT_SECRET_KEY line wasn't found, add it
    if not any('JWT_SECRET_KEY=' in line for line in new_lines):
        print("   ➕ Adding JWT_SECRET_KEY (not found in .env)")
        new_key = generate_jwt_secret()
        # Find good place to insert (after API_PORT or at end)
        insert_pos = -1
        for i, line in enumerate(new_lines):
            if 'API_PORT=' in line:
                insert_pos = i + 1
                break

        if insert_pos > 0:
            new_lines.insert(insert_pos, f'JWT_SECRET_KEY={new_key}')
        else:
            new_lines.append(f'\n# JWT Secret Key\nJWT_SECRET_KEY={new_key}')

        print(f"   ✅ Added new JWT_SECRET_KEY ({len(new_key)} chars)")
        fixed = True

    # Write back
    print("[3/3] Writing updated .env file...")
    env_path.write_text('\n'.join(new_lines), encoding='utf-8')

    if fixed:
        print("\n✅ .env file has been fixed!")
    else:
        print("\n✅ .env file was already correct!")

    print("\n" + "=" * 60)
    print("✅ Done! You can now run: python -m config.settings")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = fix_env_file()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
