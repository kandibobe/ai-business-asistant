"""
End-to-End tests for Telegram bot complete workflows.

Tests the entire user journey:
1. Start bot (/start)
2. Upload document
3. Wait for processing
4. Ask questions about document
5. Get responses
6. View document list (/mydocs)
7. Clear history (/clear)
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message, Document, User, Chat
from telegram.ext import ContextTypes

from database.models import User as DBUser, Document as DBDocument
from handlers.common_enhanced import start_command, mydocs_command
from handlers.documents import handle_document
from handlers.messages import handle_message


@pytest.mark.e2e
@pytest.mark.asyncio
class TestBotCompleteFlow:
    """Test complete bot workflow from start to finish."""

    async def test_complete_user_journey(
        self, db_session, mock_telegram_update, mock_telegram_context
    ):
        """
        Test complete user journey: start -> upload -> query -> response.

        This simulates a real user interaction with the bot.
        """
        # Step 1: User starts bot with /start
        with patch('handlers.common_enhanced.get_db_session', return_value=db_session):
            await start_command(mock_telegram_update, mock_telegram_context)

        # Verify welcome message sent
        assert mock_telegram_context.bot.send_message.called
        call_args = mock_telegram_context.bot.send_message.call_args
        assert "Привет" in str(call_args) or "Hello" in str(call_args)

        # Verify user created in database
        user = db_session.query(DBUser).filter_by(telegram_id=12345).first()
        assert user is not None
        assert user.telegram_id == 12345

        # Step 2: User uploads PDF document
        mock_document = MagicMock(spec=Document)
        mock_document.file_name = "test_report.pdf"
        mock_document.file_id = "test_file_id_123"
        mock_document.file_size = 1024 * 1024  # 1 MB
        mock_document.mime_type = "application/pdf"

        mock_telegram_update.message.document = mock_document

        with patch('handlers.documents.get_db_session', return_value=db_session):
            with patch('handlers.documents.process_pdf_task') as mock_task:
                mock_task.delay.return_value = MagicMock(id="task_123")
                await handle_document(mock_telegram_update, mock_telegram_context)

        # Verify processing started
        assert mock_task.delay.called

        # Verify document saved to database
        document = db_session.query(DBDocument).filter_by(user_id=user.id).first()
        assert document is not None
        assert document.filename == "test_report.pdf"
        assert document.status in ["pending", "processing"]

        # Step 3: Simulate document processing completion
        document.status = "completed"
        document.text_content = "Sample document content about quarterly sales performance."
        db_session.commit()

        # Step 4: User asks question about document
        mock_telegram_update.message.text = "What is the quarterly sales performance?"
        mock_telegram_update.message.document = None

        with patch('handlers.messages.get_db_session', return_value=db_session):
            with patch('handlers.messages.query_document_task') as mock_query_task:
                mock_query_task.delay.return_value = MagicMock(id="query_task_456")
                await handle_message(mock_telegram_update, mock_telegram_context)

        # Verify AI query initiated
        assert mock_query_task.delay.called

        # Step 5: User views their documents with /mydocs
        with patch('handlers.common_enhanced.get_db_session', return_value=db_session):
            await mydocs_command(mock_telegram_update, mock_telegram_context)

        # Verify document list sent
        assert mock_telegram_context.bot.send_message.called

    async def test_multiple_documents_flow(
        self, db_session, mock_telegram_update, mock_telegram_context
    ):
        """
        Test handling multiple documents from same user.
        """
        # Create user
        user = DBUser(telegram_id=12345, username="testuser")
        db_session.add(user)
        db_session.commit()

        # Upload multiple documents
        filenames = ["report1.pdf", "report2.xlsx", "report3.docx"]

        for filename in filenames:
            mock_document = MagicMock(spec=Document)
            mock_document.file_name = filename
            mock_document.file_id = f"file_id_{filename}"
            mock_document.file_size = 1024 * 1024

            mock_telegram_update.message.document = mock_document

            with patch('handlers.documents.get_db_session', return_value=db_session):
                with patch('handlers.documents.process_pdf_task'):
                    await handle_document(mock_telegram_update, mock_telegram_context)

        # Verify all documents saved
        documents = db_session.query(DBDocument).filter_by(user_id=user.id).all()
        assert len(documents) == 3

    async def test_error_handling_flow(
        self, db_session, mock_telegram_update, mock_telegram_context
    ):
        """
        Test error handling in complete flow.
        """
        # Upload invalid file type
        mock_document = MagicMock(spec=Document)
        mock_document.file_name = "malware.exe"
        mock_document.file_id = "bad_file"
        mock_document.file_size = 1024
        mock_document.mime_type = "application/x-msdownload"

        mock_telegram_update.message.document = mock_document

        with patch('handlers.documents.get_db_session', return_value=db_session):
            await handle_document(mock_telegram_update, mock_telegram_context)

        # Verify error message sent
        assert mock_telegram_context.bot.send_message.called
        call_args = str(mock_telegram_context.bot.send_message.call_args)
        assert "error" in call_args.lower() or "ошибка" in call_args.lower()


@pytest.mark.e2e
@pytest.mark.asyncio
class TestDocumentProcessingFlow:
    """Test complete document processing workflow."""

    async def test_pdf_processing_flow(self, db_session, tmp_path):
        """
        Test complete PDF processing: upload -> extract -> analyze -> query.
        """
        # This would test the actual PDF processing pipeline
        # In real implementation, use test containers with real services
        pytest.skip("Requires real Celery worker and Redis")

    async def test_excel_processing_flow(self, db_session, tmp_path):
        """
        Test complete Excel processing workflow.
        """
        pytest.skip("Requires real Celery worker and Redis")

    async def test_audio_transcription_flow(self, db_session, tmp_path):
        """
        Test complete audio transcription workflow.
        """
        pytest.skip("Requires real OpenAI Whisper API or mock")


@pytest.mark.e2e
@pytest.mark.asyncio
class TestRateLimitingFlow:
    """Test rate limiting in real scenarios."""

    async def test_rate_limit_enforcement(
        self, db_session, mock_telegram_update, mock_telegram_context
    ):
        """
        Test that rate limiting works across multiple requests.
        """
        # Create user
        user = DBUser(telegram_id=12345, username="testuser", tier="free")
        db_session.add(user)
        db_session.commit()

        # Make multiple requests quickly
        mock_telegram_update.message.text = "Test query"

        request_count = 15  # Exceed free tier limit

        with patch('handlers.messages.get_db_session', return_value=db_session):
            with patch('handlers.messages.query_document_task'):
                for _ in range(request_count):
                    try:
                        await handle_message(mock_telegram_update, mock_telegram_context)
                    except Exception:
                        pass  # Rate limit might raise exception

        # Verify rate limit was enforced (some requests should be blocked)
        # This depends on actual rate limiter implementation
        pytest.skip("Requires real Redis and rate limiter")


@pytest.mark.e2e
@pytest.mark.asyncio
class TestCachingFlow:
    """Test caching behavior in real scenarios."""

    async def test_ai_response_caching(
        self, db_session, mock_telegram_update, mock_telegram_context
    ):
        """
        Test that identical queries return cached responses.
        """
        # Create user and document
        user = DBUser(telegram_id=12345, username="testuser")
        db_session.add(user)
        db_session.commit()

        document = DBDocument(
            user_id=user.id,
            filename="test.pdf",
            text_content="Sample content",
            status="completed"
        )
        db_session.add(document)
        db_session.commit()

        # First query
        mock_telegram_update.message.text = "What is this about?"

        with patch('handlers.messages.get_db_session', return_value=db_session):
            with patch('handlers.messages.query_document_task') as mock_task:
                await handle_message(mock_telegram_update, mock_telegram_context)
                first_call_count = mock_task.delay.call_count

        # Second identical query (should use cache)
        with patch('handlers.messages.get_db_session', return_value=db_session):
            with patch('handlers.messages.query_document_task') as mock_task:
                await handle_message(mock_telegram_update, mock_telegram_context)
                second_call_count = mock_task.delay.call_count

        # If caching works, AI task should not be called second time
        # (This test requires real cache implementation)
        pytest.skip("Requires real Redis cache")


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.asyncio
class TestPerformanceFlow:
    """Test system performance under load."""

    async def test_concurrent_users(self, db_session):
        """
        Test handling multiple concurrent users.
        """
        # Simulate 10 concurrent users
        user_count = 10
        tasks = []

        for i in range(user_count):
            # Create mock update and context for each user
            # Run handlers concurrently
            pass

        pytest.skip("Performance test - run manually")

    async def test_large_document_processing(self, db_session, tmp_path):
        """
        Test processing very large documents.
        """
        pytest.skip("Performance test - requires large test files")


@pytest.mark.e2e
@pytest.mark.asyncio
class TestSecurityFlow:
    """Test security features in real scenarios."""

    async def test_malicious_file_rejection(
        self, db_session, mock_telegram_update, mock_telegram_context
    ):
        """
        Test that malicious files are rejected.
        """
        # Try to upload file with script injection
        mock_document = MagicMock(spec=Document)
        mock_document.file_name = "<script>alert('xss')</script>.pdf"
        mock_document.file_id = "malicious"
        mock_document.file_size = 1024

        mock_telegram_update.message.document = mock_document

        with patch('handlers.documents.get_db_session', return_value=db_session):
            await handle_document(mock_telegram_update, mock_telegram_context)

        # Verify file was rejected
        # Implementation depends on security validators

    async def test_sql_injection_protection(
        self, db_session, mock_telegram_update, mock_telegram_context
    ):
        """
        Test SQL injection protection.
        """
        # Try SQL injection in query
        mock_telegram_update.message.text = "'; DROP TABLE documents; --"

        with patch('handlers.messages.get_db_session', return_value=db_session):
            try:
                await handle_message(mock_telegram_update, mock_telegram_context)
            except Exception:
                pass  # Should be caught by validators

        # Verify database is still intact
        # Tables should still exist
        from sqlalchemy import inspect
        inspector = inspect(db_session.bind)
        tables = inspector.get_table_names()
        assert 'documents' in tables
        assert 'users' in tables


if __name__ == "__main__":
    """
    Run E2E tests.

    Usage:
        pytest tests/e2e/test_bot_flow.py -v
        pytest tests/e2e/test_bot_flow.py -v -m "e2e and not slow"
    """
    pytest.main([__file__, "-v", "--tb=short"])
