# src/scripts/create_super_user.py
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError # Импортируем для обработки конфликта уникальности

from src.infrastructure.postgres.database import SessionLocal
from src.infrastructure.postgres.repositories.user_rep import UserRepository
from src.infrastructure.postgres.models.user_m import User
from src.config import settings
from src.auth.security import get_hash_password


async def create_super_user():
    print(f"DEBUG: Starting create_super_user script.")
    print(f"DEBUG: Using credentials from settings - Username: {settings.SUPERUSER_USERNAME}, Email: {settings.SUPERUSER_EMAIL}")

    async with SessionLocal() as session:
        print(f"DEBUG: Got database session.")
        repo = UserRepository(session)
        print(f"DEBUG: Created UserRepository instance.")

        print(f"DEBUG: Querying for existing superuser with role 'super_admin'...")
        try:
            result = await session.execute(
                select(User).where(User.role == "super_admin")
            )
            existing_superuser = result.scalars().first()
            print(f"DEBUG: Query executed. Found existing superuser: {existing_superuser is not None}")
            if existing_superuser:
                print(f"INFO: Superuser '{existing_superuser.username}' (ID: {existing_superuser.id}) already exists with role 'super_admin'. Exiting.")
                return  # Скрипт завершается здесь, если пользователь найден

        except Exception as e:
            print(f"ERROR: Failed to query for existing superuser: {e}")
            return  # Завершаем при ошибке запроса

        username = settings.SUPERUSER_USERNAME
        password = settings.SUPERUSER_PASSWORD
        email = settings.SUPERUSER_EMAIL

        print(f"DEBUG: Checking if credentials are empty. Username: {bool(username)}, Password: {bool(password)}, Email: {bool(email)}")

        if not username or not password or not email:
            print("ERROR: Superuser credentials cannot be empty.")
            return

        print(f"DEBUG: All credentials are provided. Proceeding with creation.")
        hashed_password = get_hash_password(password)
        print(f"DEBUG: Password hashed successfully.")

        superuser_data = User(
            username=username,
            password=hashed_password,
            email=email,
            role="super_admin"
        )
        print(f"DEBUG: User object created in memory.")

        try:
            print(f"DEBUG: Attempting to create user via repo.create()...")
            superuser = await repo.create(superuser_data)
            print(f"DEBUG: repo.create() succeeded. Returned user: {superuser.username} (ID: {superuser.id})")
            print(f"DEBUG: Attempting to commit transaction...")
            await session.commit()
            print(f"DEBUG: Transaction committed.")
            print(f"Superuser '{superuser.username}' created successfully with role 'super_admin'.")
        except IntegrityError as err:
            await session.rollback()
            print(f"ERROR: IntegrityError during superuser creation (likely duplicate username/email): {err}")
            print(f"DEBUG: Transaction rolled back.")
        except Exception as err:
            await session.rollback()
            print(f"ERROR: Unexpected error creating superuser: {err}")
            print(f"DEBUG: Transaction rolled back.")


if __name__ == "__main__":
    import asyncio
    print(f"DEBUG: Script __main__ block entered.")
    asyncio.run(create_super_user())
    print(f"DEBUG: Script finished execution.")