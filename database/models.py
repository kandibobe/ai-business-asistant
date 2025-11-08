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
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=now())
    language = Column(String, default='ru', nullable=True)  # Язык пользователя
    mode = Column(String, default='standard', nullable=True)  # Режим работы

    # Связь "один ко многим": один пользователь может иметь много документов
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")

    # +++ НАЧАЛО НОВОГО КОДА +++
    # ID документа, который пользователь выбрал как активный
    active_document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)
    
    # Создаем "виртуальное" поле для удобного доступа к активному документу
    active_document = relationship("Document", foreign_keys=[active_document_id])
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
    document_type = Column(String, nullable=True)      # Тип: pdf, excel, word, audio, url
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
    uploaded_at = Column(DateTime(timezone=True), server_default=now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Связи
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
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

    def __repr__(self):
        return f"<Document(file_name='{self.file_name}', type='{self.document_type}')>"