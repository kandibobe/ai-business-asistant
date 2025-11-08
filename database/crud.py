# database/crud.py

from sqlalchemy.orm import Session
from . import models

def get_or_create_user(db: Session, user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> models.User:
    """Получает существующего пользователя или создает нового."""
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        user = models.User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Создан новый пользователь: {user_id}")
    return user

def create_user_document(db: Session, user: models.User, filename: str, file_path: str, extracted_text: str) -> models.Document:
    """Создает новый документ для пользователя."""
    document = models.Document(
        filename=filename,
        file_path=file_path,
        extracted_text=extracted_text,
        user_id=user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    print(f"✅ Документ '{filename}' сохранен для пользователя {user.user_id}")
    return document

def get_latest_document_for_user(db: Session, user: models.User) -> models.Document | None:
    # Эта функция нам больше не нужна в таком виде, но пока оставим ее.
    # Мы будем использовать get_active_document_for_user.
    return db.query(models.Document).filter(models.Document.user_id == user.id).order_by(models.Document.uploaded_at.desc()).first()

# +++ НАЧАЛО НОВОГО КОДА +++
def get_all_user_documents(db: Session, user: models.User) -> list[models.Document]:
    """Возвращает список всех документов пользователя."""
    return db.query(models.Document).filter(models.Document.user_id == user.id).order_by(models.Document.uploaded_at.desc()).all()

def get_active_document_for_user(db: Session, user: models.User) -> models.Document | None:
    """Возвращает активный документ пользователя."""
    if not user.active_document_id:
        return None
    return db.query(models.Document).filter(models.Document.id == user.active_document_id).first()
# +++ КОНЕЦ НОВОГО КОДА +++

def delete_user_documents(db: Session, user: models.User) -> int:
    """Удаляет все документы, связанные с пользователем."""
    # Сначала сбросим активный документ, если он был одним из удаляемых
    set_active_document(db, user, None)
    num_deleted = db.query(models.Document).filter(models.Document.user_id == user.id).delete()
    db.commit()
    print(f"Удалено {num_deleted} документов для пользователя {user.user_id}")
    return num_deleted

def set_active_document(db: Session, user: models.User, document_id: int | None) -> models.Document | None:
    """
    Устанавливает или сбрасывает активный документ для пользователя.
    Возвращает установленный документ или None.
    """
    user.active_document_id = document_id
    db.commit()
    db.refresh(user)
    if user.active_document:
        db.refresh(user.active_document)
    return user.active_document