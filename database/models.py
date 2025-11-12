# database/models.py

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# func убираем, так как он больше не используется напрямую здесь
# from sqlalchemy.sql import func 
# Вместо него импортируем server_default для установки времени
from sqlalchemy.sql.functions import now

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True, index=True)
    email = Column(String, nullable=True, unique=True, index=True)  # Для web users
    password_hash = Column(String, nullable=True)  # Для web users
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=now())

    # Настройки пользователя
    language = Column(String, default='ru', nullable=True)  # Язык интерфейса
    mode = Column(String, default='standard', nullable=True)  # Режим работы AI (fast/standard/advanced)
    ai_role = Column(String, default='assistant', nullable=True)  # Роль AI (analyst/consultant/teacher/etc)
    response_style = Column(String, default='standard', nullable=True)  # Стиль ответов (brief/standard/detailed/etc)
    notifications_enabled = Column(String, default='true', nullable=True)  # Уведомления (true/false как строка)
    auto_analysis_enabled = Column(String, default='false', nullable=True)  # Авто-анализ документов

    # RBAC - Role-Based Access Control
    role = Column(String, default='free', nullable=False, index=True)  # User role: guest, free, premium, business, admin, etc.

    # ID документа, который пользователь выбрал как активный
    active_document_id = Column(Integer, ForeignKey('documents.id'), nullable=True, index=True)  # PERFORMANCE: FK indexed

    # Связь "один ко многим": один пользователь может иметь много документов
    # Явно указываем foreign_keys чтобы избежать неоднозначности
    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete-orphan",
        foreign_keys="[Document.user_id]"
    )

    # Создаем "виртуальное" поле для удобного доступа к активному документу
    # Явно указываем foreign_keys чтобы избежать неоднозначности
    active_document = relationship(
        "Document",
        foreign_keys=[active_document_id],
        post_update=True  # Важно для избежания циклических зависимостей
    )
    # +++ КОНЕЦ НОВОГО КОДА +++

    def __repr__(self):
        return f"<User(user_id={self.user_id})>"

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)

    # Основные поля
    file_name = Column('filename', String, nullable=False)  # Используем alias для обратной совместимости
    file_path = Column(String, nullable=True)
    content = Column('extracted_text', Text, nullable=True)  # Alias для обратной совместимости

    # Метаданные документа
    document_type = Column(String, nullable=True, index=True)  # PERFORMANCE: Indexed for filtering
    source_url = Column(String, nullable=True)         # URL источника (для web страниц)
    file_size = Column(Integer, nullable=True)         # Размер файла в байтах

    # Аналитические поля
    word_count = Column(Integer, nullable=True)        # Количество слов
    char_count = Column(Integer, nullable=True)        # Количество символов
    language_detected = Column(String, nullable=True)  # Определенный язык

    # AI обработка
    summary = Column(Text, nullable=True)              # Краткое содержание от AI
    keywords = Column(Text, nullable=True)             # Ключевые слова (JSON строка)

    # Временные метки
    uploaded_at = Column(DateTime(timezone=True), server_default=now(), index=True)  # PERFORMANCE: Indexed for sorting
    processed_at = Column('processed_at', DateTime(timezone=True), nullable=True)  # Явный alias для существующей колонки

    # Связи
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)  # PERFORMANCE: FK should be indexed
    owner = relationship("User", back_populates="documents", foreign_keys=[user_id])

    # Свойства для обратной совместимости
    @property
    def filename(self):
        return self.file_name

    @filename.setter
    def filename(self, value):
        self.file_name = value

    @property
    def extracted_text(self):
        return self.content

    @extracted_text.setter
    def extracted_text(self, value):
        self.content = value

    @property
    def created_at(self):
        """Alias for uploaded_at for backward compatibility."""
        return self.uploaded_at

    @created_at.setter
    def created_at(self, value):
        """Alias for uploaded_at for backward compatibility."""
        self.uploaded_at = value

    def __repr__(self):
        return f"<Document(file_name='{self.file_name}', type='{self.document_type}')>"