"""
Integration tests for document handlers.
Tests document upload and processing flow.
"""
import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch
from handlers.documents import handle_document


@pytest.mark.integration
@pytest.mark.telegram
class TestDocumentHandlers:
    """Integration tests for document upload handlers."""

    @pytest.mark.asyncio
    async def test_handle_pdf_document_success(
        self,
        mock_telegram_update,
        mock_telegram_context,
        sample_pdf_file,
        mock_redis_client,
        temp_directory
    ):
        """Test successful PDF document upload."""
        # Setup
        mock_telegram_update.message.document = MagicMock()
        mock_telegram_update.message.document.file_id = 'test_file_123'
        mock_telegram_update.message.document.file_name = 'test.pdf'
        mock_telegram_update.message.document.file_size = 1024

        # Mock telegram file download
        mock_file = AsyncMock()
        mock_file.download_to_drive = AsyncMock()
        mock_telegram_context.bot.get_file = AsyncMock(return_value=mock_file)

        # Mock celery task
        with patch('handlers.documents.process_pdf_task') as mock_task:
            mock_task.delay = MagicMock(return_value=None)

            # Execute
            await handle_document(mock_telegram_update, mock_telegram_context)

            # Verify bot responded
            mock_telegram_update.message.reply_text.assert_called()
            reply_text = mock_telegram_update.message.reply_text.call_args[0][0]
            assert 'принят в работу' in reply_text or 'PDF' in reply_text

            # Verify task was queued
            mock_task.delay.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_excel_document(
        self,
        mock_telegram_update,
        mock_telegram_context,
        mock_redis_client
    ):
        """Test Excel document upload."""
        mock_telegram_update.message.document = MagicMock()
        mock_telegram_update.message.document.file_id = 'excel_123'
        mock_telegram_update.message.document.file_name = 'spreadsheet.xlsx'
        mock_telegram_update.message.document.file_size = 2048

        mock_file = AsyncMock()
        mock_file.download_to_drive = AsyncMock()
        mock_telegram_context.bot.get_file = AsyncMock(return_value=mock_file)

        with patch('handlers.documents.process_excel_task') as mock_task:
            mock_task.delay = MagicMock()

            await handle_document(mock_telegram_update, mock_telegram_context)

            mock_task.delay.assert_called_once()
            reply_text = mock_telegram_update.message.reply_text.call_args[0][0]
            assert 'Excel' in reply_text

    @pytest.mark.asyncio
    async def test_handle_word_document(
        self,
        mock_telegram_update,
        mock_telegram_context,
        mock_redis_client
    ):
        """Test Word document upload."""
        mock_telegram_update.message.document = MagicMock()
        mock_telegram_update.message.document.file_id = 'word_123'
        mock_telegram_update.message.document.file_name = 'document.docx'
        mock_telegram_update.message.document.file_size = 3072

        mock_file = AsyncMock()
        mock_file.download_to_drive = AsyncMock()
        mock_telegram_context.bot.get_file = AsyncMock(return_value=mock_file)

        with patch('handlers.documents.process_word_task') as mock_task:
            mock_task.delay = MagicMock()

            await handle_document(mock_telegram_update, mock_telegram_context)

            mock_task.delay.assert_called_once()
            reply_text = mock_telegram_update.message.reply_text.call_args[0][0]
            assert 'Word' in reply_text

    @pytest.mark.asyncio
    async def test_handle_unsupported_file_type(
        self,
        mock_telegram_update,
        mock_telegram_context,
        mock_redis_client
    ):
        """Test upload of unsupported file type."""
        mock_telegram_update.message.document = MagicMock()
        mock_telegram_update.message.document.file_id = 'exe_123'
        mock_telegram_update.message.document.file_name = 'malware.exe'
        mock_telegram_update.message.document.file_size = 1024

        mock_file = AsyncMock()
        mock_file.download_to_drive = AsyncMock()
        mock_telegram_context.bot.get_file = AsyncMock(return_value=mock_file)

        await handle_document(mock_telegram_update, mock_telegram_context)

        # Should show error message
        reply_text = mock_telegram_update.message.reply_text.call_args[0][0]
        assert 'Неподдерживаемый формат' in reply_text or 'not allowed' in reply_text.lower()

    @pytest.mark.asyncio
    async def test_handle_file_too_large(
        self,
        mock_telegram_update,
        mock_telegram_context,
        mock_redis_client
    ):
        """Test upload of file exceeding size limit."""
        mock_telegram_update.message.document = MagicMock()
        mock_telegram_update.message.document.file_id = 'large_file'
        mock_telegram_update.message.document.file_name = 'large.pdf'
        mock_telegram_update.message.document.file_size = 100 * 1024 * 1024  # 100 MB

        await handle_document(mock_telegram_update, mock_telegram_context)

        # Should reject before download
        reply_text = mock_telegram_update.message.reply_text.call_args[0][0]
        assert 'большой' in reply_text.lower() or 'large' in reply_text.lower()

    @pytest.mark.asyncio
    async def test_handle_no_document(
        self,
        mock_telegram_update,
        mock_telegram_context
    ):
        """Test handler when no document is attached."""
        mock_telegram_update.message.document = None

        await handle_document(mock_telegram_update, mock_telegram_context)

        reply_text = mock_telegram_update.message.reply_text.call_args[0][0]
        assert 'файл' in reply_text.lower() or 'file' in reply_text.lower()

    @pytest.mark.asyncio
    async def test_rate_limiting_triggered(
        self,
        mock_telegram_update,
        mock_telegram_context,
        mock_redis_client
    ):
        """Test that rate limiting is enforced."""
        # Simulate rate limit exceeded
        mock_redis_client.get.return_value = b'3'  # Already at limit
        mock_redis_client.ttl.return_value = 120

        mock_telegram_update.message.document = MagicMock()
        mock_telegram_update.message.document.file_id = 'file_123'
        mock_telegram_update.message.document.file_name = 'test.pdf'
        mock_telegram_update.message.document.file_size = 1024

        # This should be caught by rate_limit decorator
        # The actual rate limit check happens in the decorator
        # So we need to test it differently
        from middleware.rate_limiter import check_rate_limit, RateLimitExceeded

        with pytest.raises(RateLimitExceeded):
            check_rate_limit(
                mock_telegram_update.effective_user.id,
                'document_upload'
            )


@pytest.mark.integration
@pytest.mark.database
class TestDocumentProcessingFlow:
    """Integration tests for complete document processing flow."""

    def test_pdf_processing_creates_document(
        self,
        db_session,
        sample_user,
        sample_pdf_file
    ):
        """Test that PDF processing creates document in database."""
        from tasks import process_pdf_task
        from database import crud

        # Mock telegram bot and database session
        with patch('tasks.bot') as mock_bot, \
             patch('tasks.SessionLocal', return_value=db_session):
            mock_bot.send_message = MagicMock()

            # Process PDF
            process_pdf_task(
                chat_id=123,
                user_id=sample_user.user_id,
                username=sample_user.username,
                first_name=sample_user.first_name,
                last_name=sample_user.last_name,
                file_path=sample_pdf_file,
                file_name='test.pdf'
            )

            # Verify document was created
            docs = crud.get_user_documents(db_session, sample_user)
            assert len(docs) > 0

            # Verify active document was set
            active_doc = crud.get_active_document_for_user(db_session, sample_user)
            assert active_doc is not None

    def test_excel_processing_extracts_data(
        self,
        db_session,
        sample_user,
        sample_excel_file
    ):
        """Test that Excel processing extracts data correctly."""
        from tasks import process_excel_task

        with patch('tasks.bot') as mock_bot, \
             patch('tasks.SessionLocal', return_value=db_session):
            mock_bot.send_message = MagicMock()

            process_excel_task(
                chat_id=123,
                user_id=sample_user.user_id,
                username=sample_user.username,
                first_name=sample_user.first_name,
                last_name=sample_user.last_name,
                file_path=sample_excel_file,
                file_name='test.xlsx'
            )

            # Verify bot was notified
            mock_bot.send_message.assert_called()
            call_args = mock_bot.send_message.call_args[0]
            message = call_args[1] if len(call_args) > 1 else ''
            assert 'Excel' in message or 'листов' in message

    def test_word_processing_extracts_text(
        self,
        db_session,
        sample_user,
        sample_word_file
    ):
        """Test that Word processing extracts text and tables."""
        from tasks import process_word_task

        with patch('tasks.bot') as mock_bot, \
             patch('tasks.SessionLocal', return_value=db_session):
            mock_bot.send_message = MagicMock()

            process_word_task(
                chat_id=123,
                user_id=sample_user.user_id,
                username=sample_user.username,
                first_name=sample_user.first_name,
                last_name=sample_user.last_name,
                file_path=sample_word_file,
                file_name='test.docx'
            )

            mock_bot.send_message.assert_called()
