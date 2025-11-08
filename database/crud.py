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

def create_user_document(
    db: Session,
    user: models.User,
    filename: str,
    file_path: str,
    extracted_text: str,
    document_type: str = None,
    source_url: str = None,
    file_size: int = None
) -> models.Document:
    """Создает новый документ для пользователя с расширенными метаданными."""

    # Определяем тип документа автоматически, если не указан
    if not document_type:
        filename_lower = filename.lower()
        if filename_lower.endswith('.pdf'):
            document_type = 'pdf'
        elif filename_lower.endswith(('.xlsx', '.xls')):
            document_type = 'excel'
        elif filename_lower.endswith(('.docx', '.doc')):
            document_type = 'word'
        elif filename_lower.endswith(('.mp3', '.wav', '.m4a', '.ogg', '.flac')):
            document_type = 'audio'
        elif file_path and file_path.startswith('http'):
            document_type = 'url'
        else:
            document_type = 'unknown'

    # Подсчитываем слова и символы
    word_count = None
    char_count = None
    if extracted_text:
        char_count = len(extracted_text)
        word_count = len(extracted_text.split())

    document = models.Document(
        filename=filename,
        file_path=file_path,
        extracted_text=extracted_text,
        document_type=document_type,
        source_url=source_url,
        file_size=file_size,
        word_count=word_count,
        char_count=char_count,
        user_id=user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    print(f"✅ Документ '{filename}' ({document_type}) сохранен для пользователя {user.user_id}")
    return document

def update_document_analysis(
    db: Session,
    document: models.Document,
    summary: str = None,
    keywords: str = None,
    language_detected: str = None
) -> models.Document:
    """Обновляет документ результатами AI анализа."""
    from datetime import datetime

    if summary:
        document.summary = summary
    if keywords:
        document.keywords = keywords
    if language_detected:
        document.language_detected = language_detected

    document.processed_at = datetime.now()

    db.commit()
    db.refresh(document)
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

def get_document_by_id(db: Session, document_id: int) -> models.Document | None:
    """Получает документ по ID."""
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def delete_user_documents(db: Session, user: models.User) -> int:
    """Удаляет все документы, связанные с пользователем."""
    # Сначала сбросим активный документ, если он был одним из удаляемых
    set_active_document(db, user, None)
    num_deleted = db.query(models.Document).filter(models.Document.user_id == user.id).delete()
    db.commit()
    print(f"Удалено {num_deleted} документов для пользователя {user.user_id}")
    return num_deleted

# Alias для обратной совместимости
def clear_user_documents(db: Session, user: models.User) -> int:
    """Alias для delete_user_documents."""
    return delete_user_documents(db, user)

def delete_document(db: Session, document_id: int) -> bool:
    """Удаляет конкретный документ по ID."""
    document = get_document_by_id(db, document_id)
    if not document:
        return False

    # Если это активный документ пользователя, сбрасываем его
    if document.owner and document.owner.active_document_id == document_id:
        document.owner.active_document_id = None

    db.delete(document)
    db.commit()
    print(f"Удален документ ID {document_id}")
    return True

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