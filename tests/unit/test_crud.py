"""
Unit tests for CRUD operations.
Tests database/crud.py functions.
"""
import pytest
from database import crud
from database.models import User, Document


@pytest.mark.unit
@pytest.mark.database
class TestUserCRUD:
    """Tests for User CRUD operations."""

    def test_get_or_create_user_creates_new(self, db_session, sample_user_data):
        """Test creating a new user when it doesn't exist."""
        user = crud.get_or_create_user(
            db_session,
            user_id=sample_user_data['user_id'],
            username=sample_user_data['username'],
            first_name=sample_user_data['first_name'],
            last_name=sample_user_data['last_name']
        )

        assert user is not None
        assert user.user_id == sample_user_data['user_id']
        assert user.username == sample_user_data['username']

        # Check it's in DB
        db_user = db_session.query(User).filter_by(
            user_id=sample_user_data['user_id']
        ).first()
        assert db_user is not None
        assert db_user.id == user.id

    def test_get_or_create_user_gets_existing(self, db_session, sample_user):
        """Test getting an existing user."""
        # Get the same user
        user = crud.get_or_create_user(
            db_session,
            user_id=sample_user.user_id,
            username=sample_user.username,
            first_name=sample_user.first_name,
            last_name=sample_user.last_name
        )

        assert user.id == sample_user.id
        assert user.user_id == sample_user.user_id

        # Should only be one user in DB
        user_count = db_session.query(User).filter_by(
            user_id=sample_user.user_id
        ).count()
        assert user_count == 1

    def test_get_user_by_id(self, db_session, sample_user):
        """Test getting user by internal ID."""
        user = crud.get_user_by_id(db_session, sample_user.id)
        assert user is not None
        assert user.id == sample_user.id

    def test_get_user_by_id_not_found(self, db_session):
        """Test getting non-existent user."""
        user = crud.get_user_by_id(db_session, 99999)
        assert user is None


@pytest.mark.unit
@pytest.mark.database
class TestDocumentCRUD:
    """Tests for Document CRUD operations."""

    def test_create_user_document(self, db_session, sample_user):
        """Test creating a document for a user."""
        filename = 'test_document.pdf'
        filepath = '/path/to/test_document.pdf'
        content = 'This is test content'

        document = crud.create_user_document(
            db_session,
            sample_user,
            filename,
            filepath,
            content
        )

        assert document is not None
        assert document.file_name == filename
        assert document.file_path == filepath
        assert document.content == content
        assert document.user_id == sample_user.id
        assert document.owner == sample_user

    def test_get_user_documents(self, db_session, sample_user):
        """Test getting all documents for a user."""
        # Create multiple documents
        for i in range(3):
            crud.create_user_document(
                db_session,
                sample_user,
                f'doc_{i}.pdf',
                f'/path/doc_{i}.pdf',
                f'Content {i}'
            )

        documents = crud.get_user_documents(db_session, sample_user)
        assert len(documents) == 3
        assert all(doc.user_id == sample_user.id for doc in documents)

    def test_get_user_documents_empty(self, db_session, sample_user):
        """Test getting documents when user has none."""
        documents = crud.get_user_documents(db_session, sample_user)
        assert documents == []

    def test_delete_document(self, db_session, sample_document):
        """Test deleting a document."""
        doc_id = sample_document.id
        result = crud.delete_document(db_session, sample_document)

        assert result is True

        # Check document is deleted
        deleted_doc = db_session.query(Document).filter_by(id=doc_id).first()
        assert deleted_doc is None

    def test_clear_user_documents(self, db_session, sample_user):
        """Test clearing all documents for a user."""
        # Create documents
        for i in range(3):
            crud.create_user_document(
                db_session,
                sample_user,
                f'doc_{i}.pdf',
                f'/path/doc_{i}.pdf',
                f'Content {i}'
            )

        # Clear all
        crud.clear_user_documents(db_session, sample_user)

        # Check all are deleted
        documents = crud.get_user_documents(db_session, sample_user)
        assert len(documents) == 0


@pytest.mark.unit
@pytest.mark.database
class TestActiveDocumentCRUD:
    """Tests for active document CRUD operations."""

    def test_set_active_document(self, db_session, sample_user, sample_document):
        """Test setting active document for a user."""
        crud.set_active_document(db_session, sample_user, sample_document.id)

        db_session.refresh(sample_user)
        assert sample_user.active_document_id == sample_document.id
        assert sample_user.active_document == sample_document

    def test_get_active_document_for_user(self, db_session, sample_user, sample_document):
        """Test getting active document for a user."""
        # Set active
        crud.set_active_document(db_session, sample_user, sample_document.id)

        # Get active
        active_doc = crud.get_active_document_for_user(db_session, sample_user)
        assert active_doc is not None
        assert active_doc.id == sample_document.id

    def test_get_active_document_when_none(self, db_session, sample_user):
        """Test getting active document when none is set."""
        active_doc = crud.get_active_document_for_user(db_session, sample_user)
        assert active_doc is None

    def test_clear_active_document(self, db_session, sample_user, sample_document):
        """Test clearing active document."""
        # Set active
        crud.set_active_document(db_session, sample_user, sample_document.id)

        # Clear
        sample_user.active_document_id = None
        db_session.commit()

        # Verify cleared
        active_doc = crud.get_active_document_for_user(db_session, sample_user)
        assert active_doc is None
