"""
Unit tests for database models.
Tests User and Document models.
"""
import pytest
from datetime import datetime
from database.models import User, Document


@pytest.mark.unit
@pytest.mark.database
class TestUserModel:
    """Tests for User model."""

    def test_create_user(self, db_session, sample_user_data):
        """Test creating a new user."""
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.user_id == sample_user_data['user_id']
        assert user.username == sample_user_data['username']
        assert user.first_name == sample_user_data['first_name']
        assert user.last_name == sample_user_data['last_name']

    def test_user_defaults(self, db_session, sample_user_data):
        """Test user default values."""
        user = User(**sample_user_data)
        db_session.add(user)
        db_session.commit()

        assert user.language == 'ru'
        assert user.mode == 'standard'
        assert user.ai_role == 'assistant'
        assert user.response_style == 'standard'
        assert user.notifications_enabled == 'true'
        assert user.auto_analysis_enabled == 'false'
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)

    def test_user_unique_user_id(self, db_session, sample_user_data):
        """Test that user_id must be unique."""
        user1 = User(**sample_user_data)
        db_session.add(user1)
        db_session.commit()

        # Try to create another user with same user_id
        user2 = User(**sample_user_data)
        db_session.add(user2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_user_repr(self, sample_user):
        """Test user string representation."""
        repr_str = repr(sample_user)
        assert f"user_id={sample_user.user_id}" in repr_str

    def test_user_settings_update(self, db_session, sample_user):
        """Test updating user settings."""
        sample_user.language = 'en'
        sample_user.mode = 'advanced'
        sample_user.ai_role = 'analyst'
        db_session.commit()

        db_session.refresh(sample_user)
        assert sample_user.language == 'en'
        assert sample_user.mode == 'advanced'
        assert sample_user.ai_role == 'analyst'


@pytest.mark.unit
@pytest.mark.database
class TestDocumentModel:
    """Tests for Document model."""

    def test_create_document(self, db_session, sample_user, sample_document_data):
        """Test creating a new document."""
        document = Document(
            user_id=sample_user.id,
            **sample_document_data
        )
        db_session.add(document)
        db_session.commit()

        assert document.id is not None
        assert document.file_name == sample_document_data['file_name']
        assert document.content == sample_document_data['content']
        assert document.document_type == sample_document_data['document_type']
        assert document.user_id == sample_user.id

    def test_document_user_relationship(self, db_session, sample_user, sample_document):
        """Test relationship between Document and User."""
        assert sample_document.owner == sample_user
        assert sample_document in sample_user.documents

    def test_document_defaults(self, db_session, sample_user):
        """Test document default values."""
        document = Document(
            user_id=sample_user.id,
            file_name='test.pdf'
        )
        db_session.add(document)
        db_session.commit()

        assert document.uploaded_at is not None
        assert isinstance(document.uploaded_at, datetime)
        assert document.processed_at is None
        assert document.summary is None
        assert document.keywords is None

    def test_document_cascade_delete(self, db_session, sample_user, sample_document):
        """Test that documents are deleted when user is deleted."""
        doc_id = sample_document.id
        user_id = sample_user.id

        db_session.delete(sample_user)
        db_session.commit()

        # Document should be deleted too
        deleted_doc = db_session.query(Document).filter_by(id=doc_id).first()
        assert deleted_doc is None

    def test_document_repr(self, sample_document):
        """Test document string representation."""
        repr_str = repr(sample_document)
        assert sample_document.file_name in repr_str
        assert sample_document.document_type in repr_str

    def test_document_properties(self, db_session, sample_user):
        """Test document backward compatibility properties."""
        document = Document(
            user_id=sample_user.id,
            file_name='test.pdf'
        )
        document.content = 'Test content'
        db_session.add(document)
        db_session.commit()

        # Test properties
        assert document.filename == document.file_name
        assert document.extracted_text == document.content

        # Test setters
        document.filename = 'new_name.pdf'
        document.extracted_text = 'New content'

        assert document.file_name == 'new_name.pdf'
        assert document.content == 'New content'

    def test_multiple_documents_per_user(self, db_session, sample_user):
        """Test that user can have multiple documents."""
        docs = []
        for i in range(5):
            doc = Document(
                user_id=sample_user.id,
                file_name=f'document_{i}.pdf',
                content=f'Content {i}',
                document_type='pdf'
            )
            db_session.add(doc)
            docs.append(doc)

        db_session.commit()

        assert len(sample_user.documents) == 5
        assert all(doc in sample_user.documents for doc in docs)


@pytest.mark.unit
@pytest.mark.database
class TestActiveDocumentRelationship:
    """Tests for active_document relationship."""

    def test_set_active_document(self, db_session, sample_user, sample_document):
        """Test setting active document."""
        sample_user.active_document_id = sample_document.id
        db_session.commit()

        db_session.refresh(sample_user)
        assert sample_user.active_document_id == sample_document.id
        assert sample_user.active_document == sample_document

    def test_active_document_null_by_default(self, sample_user):
        """Test that active_document is null by default."""
        assert sample_user.active_document_id is None
        assert sample_user.active_document is None

    def test_change_active_document(self, db_session, sample_user):
        """Test changing active document."""
        # Create two documents
        doc1 = Document(user_id=sample_user.id, file_name='doc1.pdf')
        doc2 = Document(user_id=sample_user.id, file_name='doc2.pdf')
        db_session.add_all([doc1, doc2])
        db_session.commit()

        # Set first as active
        sample_user.active_document_id = doc1.id
        db_session.commit()
        assert sample_user.active_document == doc1

        # Change to second
        sample_user.active_document_id = doc2.id
        db_session.commit()
        db_session.refresh(sample_user)
        assert sample_user.active_document == doc2
