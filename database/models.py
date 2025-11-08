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
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    extracted_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=now())
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    owner = relationship("User", back_populates="documents", foreign_keys=[user_id])

    def __repr__(self):
        return f"<Document(filename='{self.filename}')>"