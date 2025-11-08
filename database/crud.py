# database/crud.py

from sqlalchemy.orm import Session
from . import models

def get_latest_document_for_user(db: Session, user: models.User) -> models.Document | None:
    # Эта функция нам больше не нужна в таком виде, но пока оставим ее.
    # Мы будем использовать get_active_document_for_user.
    return db.query(models.Document).filter(models.Document.user_id == user.id).order_by(models.Document.uploaded_at.desc()).first()

# +++ НАЧАЛО НОВОГО КОДА +++
def get_all_user_documents(db: Session, user: models.User) -> list[models.Document]:
    """Возвращает список всех документов пользователя."""
    return db.query(models.Document).filter(models.Document.user_id == user.id).order_by(models.Document.uploaded_at.desc()).all()

def set_active_document(db: Session, user: models.User, document_id: int | None):
    """Устанавливает или сбрасывает активный документ для пользователя."""
    user.active_document_id = document_id
    db.commit()

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