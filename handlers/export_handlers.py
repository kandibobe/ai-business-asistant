"""
Обработчики экспорта данных в различные форматы.
Поддержка PDF, визуализации, и других форматов.
"""
import io
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import crud
from export import (
    create_document_report,
    create_stats_report,
    pdf_available,
    create_stats_visualization,
    create_excel_visualization,
    viz_available,
)
from analytics import get_user_stats, get_document_stats
from ui import get_export_format_keyboard


async def handle_export_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, doc_id: int) -> None:
    """Показать меню выбора формата экспорта"""
    query = update.callback_query

    await query.edit_message_text(
        text="📥 <b>Выберите формат экспорта:</b>\n\nВыберите в каком формате вы хотите получить отчет по документу.",
        reply_markup=get_export_format_keyboard(doc_id),
        parse_mode='HTML'
    )


async def handle_export_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE, doc_id: int) -> None:
    """Экспорт документа в PDF отчет"""
    query = update.callback_query
    user = update.effective_user

    if not pdf_available():
        await query.answer(
            "⚠️ PDF экспорт недоступен. Установите: pip install reportlab",
            show_alert=True
        )
        return

    await query.answer("📄 Создаю PDF отчет...")

    db: Session = SessionLocal()
    try:
        # Получаем документ
        document = db.query(crud.models.Document).filter(
            crud.models.Document.id == doc_id
        ).first()

        if not document:
            await query.answer("❌ Документ не найден", show_alert=True)
            return

        # Получаем статистику документа
        doc_stats = get_document_stats(db, doc_id)

        # Создаем PDF отчет
        metadata = {
            'uploaded_date': document.created_at.strftime('%d.%m.%Y %H:%M'),
            'char_count': len(document.content),
            'file_size': f"{len(document.content) // 1024} KB",
        }

        # Content summary (first 2000 characters)
        content_preview = document.content[:2000] if document.content else "Content unavailable"

        # TODO: Add question history from DB when implemented
        questions_history = []

        pdf_bytes = create_document_report(
            document_name=document.file_name,
            document_content=content_preview,
            analysis_results=doc_stats.get('summary', 'Analysis not performed'),
            questions_history=questions_history,
            metadata=metadata
        )

        # Send PDF file
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_file.name = f"report_{document.file_name}.pdf"

        await context.bot.send_document(
            chat_id=user.id,
            document=pdf_file,
            caption=f"📄 <b>PDF отчет готов!</b>\n\nДокумент: {document.file_name}\nСоздан: {metadata['uploaded_date']}",
            parse_mode='HTML'
        )

        await query.edit_message_text(
            text="✅ <b>PDF отчет отправлен!</b>\n\nПроверьте чат выше.",
            parse_mode='HTML'
        )

    except Exception as e:
        await query.answer(f"❌ Ошибка при создании PDF: {str(e)}", show_alert=True)
    finally:
        db.close()


async def handle_export_stats_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Экспорт статистики пользователя в PDF"""
    query = update.callback_query
    user = update.effective_user

    if not pdf_available():
        await query.answer(
            "⚠️ PDF экспорт недоступен. Установите: pip install reportlab",
            show_alert=True
        )
        return

    await query.answer("📊 Создаю PDF с вашей статистикой...")

    db: Session = SessionLocal()
    try:
        stats = get_user_stats(db, user.id)

        if not stats:
            await query.answer("❌ Статистика недоступна", show_alert=True)
            return

        # Создаем PDF отчет
        user_name = user.first_name or user.username or f"User {user.id}"
        pdf_bytes = create_stats_report(stats, user_name)

        # Отправляем PDF файл
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_file.name = f"stats_{user.id}.pdf"

        await context.bot.send_document(
            chat_id=user.id,
            document=pdf_file,
            caption=f"📊 <b>Ваша статистика в PDF!</b>\n\nПользователь: {user_name}",
            parse_mode='HTML'
        )

        await query.edit_message_text(
            text="✅ <b>PDF со статистикой отправлен!</b>\n\nПроверьте чат выше.",
            parse_mode='HTML'
        )

    except Exception as e:
        await query.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
    finally:
        db.close()


async def handle_visualize_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Визуализация статистики пользователя"""
    query = update.callback_query
    user = update.effective_user

    if not viz_available():
        await query.answer(
            "⚠️ Визуализация недоступна. Установите: pip install matplotlib pandas",
            show_alert=True
        )
        return

    await query.answer("📈 Создаю графики...")

    db: Session = SessionLocal()
    try:
        stats = get_user_stats(db, user.id)

        if not stats:
            await query.answer("❌ Статистика недоступна", show_alert=True)
            return

        # Создаем визуализацию
        image_bytes = create_stats_visualization(stats)

        # Отправляем изображение
        photo = io.BytesIO(image_bytes)
        photo.name = 'stats.png'

        await context.bot.send_photo(
            chat_id=user.id,
            photo=photo,
            caption=f"📊 <b>Ваша статистика</b>\n\n"
                    f"📄 Всего документов: {stats.get('total_docs', 0)}\n"
                    f"💬 Задано вопросов: {stats.get('questions_asked', 0)}\n"
                    f"🔥 Streak: {stats.get('streak_days', 0)} дней",
            parse_mode='HTML'
        )

        await query.edit_message_text(
            text="✅ <b>Визуализация отправлена!</b>\n\nПроверьте чат выше.",
            parse_mode='HTML'
        )

    except Exception as e:
        await query.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
    finally:
        db.close()


async def handle_visualize_document(update: Update, context: ContextTypes.DEFAULT_TYPE, doc_id: int) -> None:
    """Визуализация данных из документа (для Excel)"""
    query = update.callback_query
    user = update.effective_user

    if not viz_available():
        await query.answer(
            "⚠️ Визуализация недоступна. Установите: pip install matplotlib pandas",
            show_alert=True
        )
        return

    await query.answer("📊 Создаю визуализацию...")

    db: Session = SessionLocal()
    try:
        # Получаем документ
        document = db.query(crud.models.Document).filter(
            crud.models.Document.id == doc_id
        ).first()

        if not document:
            await query.answer("❌ Документ не найден", show_alert=True)
            return

        # Проверяем, что это Excel файл
        if not document.file_name.lower().endswith(('.xlsx', '.xls')):
            await query.answer(
                "⚠️ Визуализация доступна только для Excel файлов",
                show_alert=True
            )
            return

        # Создаем визуализацию из Excel
        try:
            image_bytes = create_excel_visualization(
                document.file_path,
                chart_type='bar'
            )

            # Отправляем изображение
            photo = io.BytesIO(image_bytes)
            photo.name = f'chart_{document.file_name}.png'

            await context.bot.send_photo(
                chat_id=user.id,
                photo=photo,
                caption=f"📊 <b>Визуализация данных</b>\n\nДокумент: {document.file_name}",
                parse_mode='HTML'
            )

            await query.edit_message_text(
                text="✅ <b>График отправлен!</b>\n\nПроверьте чат выше.",
                parse_mode='HTML'
            )

        except Exception as viz_error:
            await query.answer(
                f"❌ Не удалось создать визуализацию: {str(viz_error)[:100]}",
                show_alert=True
            )

    except Exception as e:
        await query.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
    finally:
        db.close()
