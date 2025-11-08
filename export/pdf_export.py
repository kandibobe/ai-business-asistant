"""
Экспорт результатов анализа в PDF формат.
Профессиональные отчеты для клиентов.
"""
import io
from datetime import datetime
from typing import Dict, Any, Optional, List
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def is_available() -> bool:
    """Проверить доступность экспорта в PDF"""
    return REPORTLAB_AVAILABLE

def create_document_report(
    document_name: str,
    document_content: str,
    analysis_results: Optional[str] = None,
    questions_history: Optional[List[Dict[str, str]]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> bytes:
    """
    Создать PDF отчет по документу.

    Args:
        document_name: Название документа
        document_content: Содержимое документа (краткое)
        analysis_results: Результаты AI анализа
        questions_history: История вопросов и ответов
        metadata: Дополнительные метаданные

    Returns:
        bytes: PDF файл в виде байтов
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab не установлен. Установите: pip install reportlab")

    # Создаем буфер для PDF
    buffer = io.BytesIO()

    # Создаем документ
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Стили
    styles = getSampleStyleSheet()

    # Кастомные стили
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1a73e8'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=HexColor('#444444'),
        alignment=TA_JUSTIFY,
        spaceAfter=12,
    )

    # Контент документа
    story = []

    # Заголовок
    story.append(Paragraph("📊 Отчет по документу", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Информация о документе
    story.append(Paragraph("📄 Документ", heading_style))

    doc_info = [
        ['Название:', document_name],
        ['Дата создания:', datetime.now().strftime('%d.%m.%Y %H:%M')],
    ]

    if metadata:
        if 'uploaded_date' in metadata:
            doc_info.append(['Загружен:', metadata['uploaded_date']])
        if 'file_size' in metadata:
            doc_info.append(['Размер:', metadata['file_size']])
        if 'char_count' in metadata:
            doc_info.append(['Символов:', f"{metadata['char_count']:,}"])

    # Таблица с информацией
    info_table = Table(doc_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#333333')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc'))
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3 * inch))

    # Краткое содержание
    if document_content:
        story.append(Paragraph("📝 Краткое содержание", heading_style))

        # Ограничиваем длину для отчета
        content_preview = document_content[:2000] + "..." if len(document_content) > 2000 else document_content

        # Разбиваем на параграфы
        paragraphs = content_preview.split('\n\n')
        for para in paragraphs[:5]:  # Первые 5 параграфов
            if para.strip():
                story.append(Paragraph(para.strip(), body_style))

        story.append(Spacer(1, 0.2 * inch))

    # Результаты анализа
    if analysis_results:
        story.append(Paragraph("🤖 AI Анализ", heading_style))
        story.append(Paragraph(analysis_results, body_style))
        story.append(Spacer(1, 0.2 * inch))

    # История вопросов
    if questions_history and len(questions_history) > 0:
        story.append(PageBreak())
        story.append(Paragraph("💬 История вопросов и ответов", heading_style))
        story.append(Spacer(1, 0.1 * inch))

        for idx, qa in enumerate(questions_history, 1):
            # Вопрос
            q_style = ParagraphStyle(
                'Question',
                parent=body_style,
                fontSize=11,
                textColor=HexColor('#1a73e8'),
                fontName='Helvetica-Bold',
                leftIndent=20,
            )
            story.append(Paragraph(f"<b>❓ Вопрос {idx}:</b> {qa.get('question', '')}", q_style))
            story.append(Spacer(1, 0.1 * inch))

            # Ответ
            a_style = ParagraphStyle(
                'Answer',
                parent=body_style,
                fontSize=10,
                leftIndent=20,
                rightIndent=20,
            )
            story.append(Paragraph(f"<b>💡 Ответ:</b> {qa.get('answer', '')}", a_style))
            story.append(Spacer(1, 0.2 * inch))

    # Футер
    story.append(Spacer(1, 0.5 * inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=body_style,
        fontSize=9,
        textColor=HexColor('#888888'),
        alignment=TA_CENTER,
    )
    story.append(Paragraph("─" * 60, footer_style))
    story.append(Paragraph(
        f"Сгенерировано AI Business Intelligence Agent<br/>{datetime.now().strftime('%d.%m.%Y %H:%M')}",
        footer_style
    ))

    # Строим PDF
    doc.build(story)

    # Получаем байты
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes

def create_stats_report(stats: Dict[str, Any], user_name: str) -> bytes:
    """
    Создать PDF отчет со статистикой пользователя.

    Args:
        stats: Словарь со статистикой
        user_name: Имя пользователя

    Returns:
        bytes: PDF файл
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab не установлен")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Заголовок
    title = Paragraph(f"📊 Статистика использования<br/>{user_name}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.3 * inch))

    # Таблица статистики
    data = [
        ['Метрика', 'Значение'],
        ['Всего документов', str(stats.get('total_docs', 0))],
        ['Активный документ', str(stats.get('active_doc', 'Нет'))],
        ['Документов за месяц', str(stats.get('docs_this_month', 0))],
        ['Задано вопросов', str(stats.get('questions_asked', 0))],
        ['PDF документов', str(stats.get('pdf_count', 0))],
        ['Excel документов', str(stats.get('excel_count', 0))],
        ['Word документов', str(stats.get('word_count', 0))],
        ['URL документов', str(stats.get('url_count', 0))],
        ['Аудио записей', str(stats.get('audio_count', 0))],
        ['Streak дней', str(stats.get('streak_days', 0))],
    ]

    t = Table(data, colWidths=[3*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f9f9f9')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc'))
    ]))

    story.append(t)
    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
