"""
Модуль визуализации данных из Excel и других источников.
Создание графиков и диаграмм для Telegram бота.
"""
import io
from typing import List, Dict, Any, Optional, Tuple
try:
    import matplotlib
    matplotlib.use('Agg')  # Без GUI backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Профессиональная цветовая палитра
COLORS = {
    'primary': '#1a73e8',
    'secondary': '#34a853',
    'accent': '#fbbc04',
    'danger': '#ea4335',
    'purple': '#9334e6',
    'teal': '#00897b',
    'orange': '#ff6f00',
    'pink': '#e91e63',
}

PALETTE = list(COLORS.values())

def is_available() -> bool:
    """Проверить доступность визуализации"""
    return MATPLOTLIB_AVAILABLE and PANDAS_AVAILABLE

def create_bar_chart(
    data: Dict[str, float],
    title: str = "Диаграмма",
    xlabel: str = "Категории",
    ylabel: str = "Значения",
    color: Optional[str] = None
) -> bytes:
    """
    Создать столбчатую диаграмму.

    Args:
        data: Словарь {категория: значение}
        title: Заголовок графика
        xlabel: Подпись оси X
        ylabel: Подпись оси Y
        color: Цвет столбцов

    Returns:
        bytes: PNG изображение
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib не установлен")

    fig, ax = plt.subplots(figsize=(10, 6))

    categories = list(data.keys())
    values = list(data.values())

    bars = ax.bar(categories, values, color=color or COLORS['primary'], alpha=0.8, edgecolor='black')

    # Добавляем значения на столбцах
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{height:.1f}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Сохраняем в байты
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    plt.close(fig)

    return image_bytes

def create_pie_chart(
    data: Dict[str, float],
    title: str = "Круговая диаграмма"
) -> bytes:
    """
    Создать круговую диаграмму.

    Args:
        data: Словарь {категория: значение}
        title: Заголовок

    Returns:
        bytes: PNG изображение
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib не установлен")

    fig, ax = plt.subplots(figsize=(10, 8))

    labels = list(data.keys())
    sizes = list(data.values())
    colors = PALETTE[:len(labels)]

    # Взрыв для самого большого сегмента
    explode = [0.1 if size == max(sizes) else 0 for size in sizes]

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        explode=explode,
        shadow=True,
        textprops={'fontsize': 11}
    )

    # Улучшаем читаемость
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    plt.close(fig)

    return image_bytes

def create_line_chart(
    data: Dict[str, List[float]],
    x_labels: List[str],
    title: str = "Линейный график",
    xlabel: str = "X",
    ylabel: str = "Y"
) -> bytes:
    """
    Создать линейный график.

    Args:
        data: Словарь {серия: [значения]}
        x_labels: Подписи оси X
        title: Заголовок
        xlabel: Подпись оси X
        ylabel: Подпись оси Y

    Returns:
        bytes: PNG изображение
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib не установлен")

    fig, ax = plt.subplots(figsize=(12, 6))

    for idx, (label, values) in enumerate(data.items()):
        color = PALETTE[idx % len(PALETTE)]
        ax.plot(x_labels, values, marker='o', linewidth=2, label=label, color=color)

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    plt.close(fig)

    return image_bytes

def create_excel_visualization(
    file_path: str,
    sheet_name: Optional[str] = None,
    chart_type: str = 'bar'
) -> bytes:
    """
    Автоматическая визуализация данных из Excel файла.

    Args:
        file_path: Путь к Excel файлу
        sheet_name: Название листа (None = первый лист)
        chart_type: Тип графика ('bar', 'pie', 'line')

    Returns:
        bytes: PNG изображение
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("pandas не установлен")
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib не установлен")

    # Читаем Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name or 0)

    # Находим числовые столбцы
    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) == 0:
        raise ValueError("В таблице нет числовых данных для визуализации")

    # Берем первые 2 столбца (или первый числовой + индекс)
    if len(df.columns) >= 2:
        # Предполагаем: первый столбец - категории, второй - значения
        categories = df.iloc[:, 0].astype(str).tolist()
        values = df[numeric_cols[0]].tolist()

        # Ограничиваем количество для читаемости
        if len(categories) > 15:
            categories = categories[:15] + ['...остальные']
            values = values[:15] + [sum(values[15:])]

        data = dict(zip(categories, values))

        if chart_type == 'pie':
            return create_pie_chart(data, title=f"Распределение: {numeric_cols[0]}")
        elif chart_type == 'line':
            return create_line_chart(
                {numeric_cols[0]: values},
                categories,
                title=f"Динамика: {numeric_cols[0]}"
            )
        else:  # bar
            return create_bar_chart(
                data,
                title=f"Анализ: {numeric_cols[0]}",
                xlabel=str(df.columns[0]),
                ylabel=str(numeric_cols[0])
            )

    else:
        # Только числовые данные - создаем простой график
        values = df[numeric_cols[0]].tolist()
        categories = [f"Запись {i+1}" for i in range(len(values))]
        data = dict(zip(categories, values))

        return create_bar_chart(data, title=f"Данные: {numeric_cols[0]}")

def create_stats_visualization(stats: Dict[str, Any]) -> bytes:
    """
    Создать визуализацию статистики пользователя.

    Args:
        stats: Словарь со статистикой

    Returns:
        bytes: PNG изображение с несколькими графиками
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib не установлен")

    # Создаем фигуру с 2 подграфиками
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # График 1: Типы документов (круговая диаграмма)
    doc_types = {
        'PDF': stats.get('pdf_count', 0),
        'Excel': stats.get('excel_count', 0),
        'Word': stats.get('word_count', 0),
        'URL': stats.get('url_count', 0),
        'Audio': stats.get('audio_count', 0),
    }

    # Фильтруем нулевые значения
    doc_types = {k: v for k, v in doc_types.items() if v > 0}

    if doc_types:
        labels = list(doc_types.keys())
        sizes = list(doc_types.values())
        colors = PALETTE[:len(labels)]

        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Типы документов', fontsize=14, fontweight='bold')

    # График 2: Активность (столбчатая диаграмма)
    activity_data = {
        'Всего\nдокументов': stats.get('total_docs', 0),
        'За этот\nмесяц': stats.get('docs_this_month', 0),
        'Задано\nвопросов': stats.get('questions_asked', 0),
        'Streak\nдней': stats.get('streak_days', 0),
    }

    categories = list(activity_data.keys())
    values = list(activity_data.values())
    colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['purple']]

    bars = ax2.bar(categories, values, color=colors_list, alpha=0.8, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    ax2.set_title('Активность', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Количество', fontsize=11)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    plt.suptitle('📊 Ваша статистика', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    plt.close(fig)

    return image_bytes
