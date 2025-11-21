import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np
warnings.filterwarnings('ignore')
from PIL import Image
import os

# Загрузка данных
df = pd.read_csv('https://drive.google.com/uc?export=download&id=130KYOX8O4wrP_T8vdz2GfvJRQ03ONmE7')

# Функция для очистки и преобразования цены
def clean_price(price_str):
    """
    Преобразует строку цены в числовое значение
    Пример: "500000.0 руб./ За месяц" -> 500000.0
    """
    if isinstance(price_str, str):
        # Удаляем всё после "руб." и нечисловые символы
        price_clean = price_str.split('руб.')[0].strip()
        # Удаляем все пробелы и оставляем только цифры и точку
        price_clean = ''.join(ch for ch in price_clean if ch.isdigit() or ch == '.')
        try:
            return float(price_clean) if price_clean else None
        except ValueError:
            return None
    return price_str

# Функция для анализа пропущенных значений
def create_missing_data_analysis(df):
    st.subheader("🔍 Анализ пропущенных значений")
    
    # Вычисляем пропущенные значения
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100

    # Создаем DataFrame с результатами
    missing_df = pd.DataFrame({
        'Колонка': missing_data.index,
        'Пропущено': missing_data.values,
        'Процент': missing_percent.values
    }).sort_values('Пропущено', ascending=False)

    # Показываем общую статистику
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_missing = missing_data.sum()
        st.metric("Всего пропусков", f"{total_missing:,}")
    
    with col2:
        columns_with_missing = len(missing_df[missing_df['Пропущено'] > 0])
        st.metric("Колонок с пропусками", columns_with_missing)
    
    with col3:
        complete_columns = len(missing_df[missing_df['Пропущено'] == 0])
        st.metric("Полностью заполненных", complete_columns)

    # Создаем вкладки для разных представлений
    tab1, tab2, tab3 = st.tabs(["📊 График", "📋 Таблица", "💡 Рекомендации"])

    with tab1:
        # График пропущенных значений
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Фильтруем только колонки с пропусками
        missing_plot = missing_df[missing_df['Пропущено'] > 0]
        
        if len(missing_plot) > 0:
            # Создаем горизонтальный барплот
            bars = ax.barh(missing_plot['Колонка'], missing_plot['Процент'], 
                          color='lightcoral', edgecolor='darkred', alpha=0.7)
            
            ax.set_xlabel('Процент пропусков (%)', fontsize=12)
            ax.set_title('Распределение пропущенных значений по колонкам', 
                        fontsize=14, fontweight='bold', pad=20)
            
            # Добавляем значения на столбцы
            for i, (idx, row) in enumerate(missing_plot.iterrows()):
                ax.text(row['Процент'] + 1, i, 
                       f'{row["Процент"]:.1f}% ({row["Пропущено"]} проп.)', 
                       va='center', fontsize=10, fontweight='bold')
            
            # Настройка внешнего вида
            ax.grid(axis='x', alpha=0.3)
            ax.set_axisbelow(True)
            
        else:
            ax.text(0.5, 0.5, 'Нет пропущенных значений! 🎉', 
                   ha='center', va='center', transform=ax.transAxes, 
                   fontsize=16, fontweight='bold', color='green')
        
        plt.tight_layout()
        st.pyplot(fig)

    with tab2:
        # Таблица с детальной информацией
        st.write("**Детальная информация о пропущенных значениях:**")
        
        if len(missing_df[missing_df['Пропущено'] > 0]) > 0:
            # Форматируем таблицу для отображения
            display_df = missing_df[missing_df['Пропущено'] > 0].copy()
            display_df['Процент'] = display_df['Процент'].round(2)
            display_df['Пропущено'] = display_df['Пропущено'].apply(lambda x: f"{x:,}")
            display_df['Процент'] = display_df['Процент'].apply(lambda x: f"{x}%")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Скачивание данных о пропусках
            csv = missing_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Скачать данные о пропусках (CSV)",
                data=csv,
                file_name="missing_data_analysis.csv",
                mime="text/csv",
            )
        else:
            st.success("🎉 В данных нет пропущенных значений!")

    with tab3:
        st.write("**Рекомендации по обработке пропусков:**")
        
        if len(missing_df[missing_df['Пропущено'] > 0]) > 0:
            high_missing = missing_df[missing_df['Процент'] > 50]
            medium_missing = missing_df[(missing_df['Процент'] > 20) & (missing_df['Процент'] <= 50)]
            low_missing = missing_df[missing_df['Процент'] <= 20]
            
            if len(high_missing) > 0:
                st.warning("**Высокий уровень пропусков (>50%):**")
                for _, row in high_missing.iterrows():
                    st.write(f"- **{row['Колонка']}**: {row['Процент']:.1f}% пропусков")
                    st.write("  *Рекомендация: рассмотреть удаление колонки*")
                st.write("")
            
            if len(medium_missing) > 0:
                st.info("**Средний уровень пропусков (20-50%):**")
                for _, row in medium_missing.iterrows():
                    st.write(f"- **{row['Колонка']}**: {row['Процент']:.1f}% пропусков")
                    st.write("  *Рекомендация: осторожная импутация или анализ причин*")
                st.write("")
            
            if len(low_missing) > 0:
                st.success("**Низкий уровень пропусков (≤20%):**")
                for _, row in low_missing.iterrows():
                    st.write(f"- **{row['Колонка']}**: {row['Процент']:.1f}% пропусков")
                    st.write("  *Рекомендация: безопасная импутация*")
        else:
            st.success("**Отличные новости!** Все данные заполнены. Можно приступать к анализу.")

# Функция для анализа животных/детей
def create_animal_child_analysis(df):
    st.subheader("🐕‍🦺 Анализ цен по разрешению на детей и животных")
    
    # Создаем копию DataFrame
    df_clean = df.copy()
    
    # Преобразуем цену в числовой формат
    df_clean['Цена_число'] = df_clean['Цена'].apply(clean_price)
    
    # Удаляем строки с отсутствующими значениями
    df_clean = df_clean.dropna(subset=['Можно с детьми/животными', 'Цена_число'])
    
    # Группируем и считаем медианную цену
    try:
        animal_positive = df_clean.groupby("Можно с детьми/животными")["Цена_число"].median()
        animal_positive = animal_positive.sort_values(ascending=False)
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = animal_positive.plot(kind="bar", color=colors, ax=ax)
        
        ax.set_title("Медианная цена по разрешению на детей/животных", fontsize=14, fontweight='bold')
        ax.set_ylabel("Цена (руб)", fontsize=12)
        ax.set_xlabel("")
        ax.grid(axis='y', alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
        
        # Добавляем значения на столбцы
        for i, v in enumerate(animal_positive.values):
            ax.text(i, v + max(animal_positive.values) * 0.01, 
                   f'{v:,.0f} руб', 
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Статистика
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_ads = len(df_clean)
            st.metric("Всего объявлений", total_ads)
        
        with col2:
            most_expensive = animal_positive.index[0]
            st.metric("Самая дорогая категория", most_expensive)
        
        with col3:
            price_diff = animal_positive.iloc[0] - animal_positive.iloc[-1]
            st.metric("Разница макс-мин", f"{price_diff:,.0f} руб")
        
        # Детальная таблица
        st.subheader("Детальная статистика по категориям")
        
        detailed_stats = df_clean.groupby("Можно с детьми/животными").agg({
            'Цена_число': ['median', 'mean', 'count', 'min', 'max']
        }).round(0)
        
        # Упрощаем названия колонок
        detailed_stats.columns = ['Медиана', 'Среднее', 'Количество', 'Мин', 'Макс']
        detailed_stats = detailed_stats.sort_values('Медиана', ascending=False)
        
        # Форматируем числа
        display_stats = detailed_stats.copy()
        for col in ['Медиана', 'Среднее', 'Мин', 'Макс']:
            display_stats[col] = display_stats[col].apply(lambda x: f"{x:,.0f} руб")
        
        st.dataframe(display_stats, use_container_width=True)
        
        # Дополнительная информация
        with st.expander("💡 Интересные наблюдения"):
            if "Можно с детьми, Можно с животными" in animal_positive.index:
                st.write("**Объекты, где разрешены и дети, и животные:**")
                st.write(f"- Медианная цена: {animal_positive['Можно с детьми, Можно с животными']:,.0f} руб")
                
            if "Можно с детьми" in animal_positive.index:
                st.write("**Объекты, где разрешены только дети:**")
                st.write(f"- Медианная цена: {animal_positive['Можно с детьми']:,.0f} руб")
                
            if "Можно с животными" in animal_positive.index:
                st.write("**Объекты, где разрешены только животные:**")
                st.write(f"- Медианная цена: {animal_positive['Можно с животными']:,.0f} руб")
            
            st.write(f"**Самая дорогая категория:** {animal_positive.index[0]} - {animal_positive.iloc[0]:,.0f} руб")
            st.write(f"**Самая дешевая категория:** {animal_positive.index[-1]} - {animal_positive.iloc[-1]:,.0f} руб")
            
    except Exception as e:
        st.error(f"Ошибка при построении графиков: {e}")
        st.write("Данные для отладки:")
        st.write(f"Уникальные значения в колонке 'Можно с детьми/животными': {df_clean['Можно с детьми/животными'].unique()}")

# Основной код для анализа высоты потолков
def create_ceiling_height_analysis(df):
    st.subheader("📏 Анализ зависимости цены от высоты потолков")
    
    # Создаем копию DataFrame чтобы не изменять оригинал
    df_clean = df.copy()
    
    # Преобразуем цену в числовой формат
    df_clean['Цена_число'] = df_clean['Цена'].apply(clean_price)
    
    # Удаляем строки с отсутствующими значениями
    df_clean = df_clean.dropna(subset=['Высота потолков, м', 'Цена_число'])
    
    # Преобразуем высоту потолков в числовой формат
    df_clean['Высота потолков, м'] = pd.to_numeric(df_clean['Высота потолков, м'], errors='coerce')
    df_clean = df_clean.dropna(subset=['Высота потолков, м'])
    
    # Группируем по высоте потолков и считаем медиану цены
    try:
        ceiling_price = df_clean.groupby("Высота потолков, м")["Цена_число"].median().sort_values(ascending=False).head(10)
        
        # Создаем график
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # График 1: Медианная цена по высоте потолков
        ceiling_price.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Медианная цена аренды по высоте потолков')
        ax1.set_xlabel('Высота потолков (м)')
        ax1.set_ylabel('Медианная цена (руб)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Добавляем значения на столбцы
        for i, v in enumerate(ceiling_price.values):
            ax1.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # График 2: Scatter plot
        ax2.scatter(df_clean['Высота потолков, м'], df_clean['Цена_число'], alpha=0.6)
        ax2.set_title('Зависимость цены от высоты потолков')
        ax2.set_xlabel('Высота потолков (м)')
        ax2.set_ylabel('Цена аренды (руб)')
        
        # Линия тренда
        z = np.polyfit(df_clean['Высота потолков, м'], df_clean['Цена_число'], 1)
        p = np.poly1d(z)
        ax2.plot(df_clean['Высота потолков, м'], p(df_clean['Высота потолков, м']), "r--", alpha=0.8)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Статистика
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Количество записей в анализе", len(df_clean))
        
        with col2:
            correlation = df_clean['Высота потолков, м'].corr(df_clean['Цена_число'])
            st.metric("Корреляция", f"{correlation:.3f}")
        
        with col3:
            avg_price_per_meter = df_clean['Цена_число'].mean() / df_clean['Высота потолков, м'].mean()
            st.metric("Средняя цена за 1м высоты", f"{avg_price_per_meter:,.0f} руб")
        
        # Таблица с топом
        st.subheader("Топ-10 по медианной цене")
        top_table = pd.DataFrame({
            'Высота потолков (м)': ceiling_price.index,
            'Медианная цена (руб)': ceiling_price.values
        })
        st.dataframe(top_table, use_container_width=True)
        
    except Exception as e:
        st.error(f"Ошибка при построении графиков: {e}")
        st.write("Данные для отладки:")
        st.write(f"Тип цены: {df_clean['Цена_число'].dtype}")
        st.write(f"Тип высоты потолков: {df_clean['Высота потолков, м'].dtype}")
        st.write(f"Пример цен: {df_clean['Цена_число'].head().tolist()}")

# Альтернативный упрощенный вариант
def simple_ceiling_analysis(df):
    st.subheader("📏 Анализ высоты потолков")
    
    # Очистка данных
    df_clean = df.copy()
    
    # Преобразуем цену
    df_clean['Цена_число'] = df_clean['Цена'].apply(clean_price)
    df_clean['Высота потолков, м'] = pd.to_numeric(df_clean['Высота потолков, м'], errors='coerce')
    
    # Удаляем пропуски
    df_clean = df_clean.dropna(subset=['Высота потолков, м', 'Цена_число'])
    
    if len(df_clean) == 0:
        st.warning("Нет данных для анализа после очистки")
        return
    
    # Группируем и считаем
    ceiling_stats = df_clean.groupby("Высота потолков, м").agg({
        'Цена_число': ['median', 'count']
    }).round(0)
    
    # Упрощаем мультииндекс
    ceiling_stats.columns = ['Медианная_цена', 'Количество']
    ceiling_stats = ceiling_stats.sort_values('Медианная_цена', ascending=False).head(10)
    
    # График
    fig, ax = plt.subplots(figsize=(10, 6))
    ceiling_stats['Медианная_цена'].plot(kind='bar', ax=ax, color='lightcoral')
    ax.set_title('Медианная цена аренды по высоте потолков')
    ax.set_xlabel('Высота потолков (м)')
    ax.set_ylabel('Медианная цена (руб)')
    ax.tick_params(axis='x', rotation=45)
    
    # Добавляем значения
    for i, v in enumerate(ceiling_stats['Медианная_цена']):
        ax.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    st.pyplot(fig)
    
    # Таблица
    st.dataframe(ceiling_stats, use_container_width=True)

# Основное приложение Streamlit
def main():
    st.set_page_config(page_title="Анализ недвижимости", page_icon="🏠", layout="wide")
    
    st.title("🏠 Анализ аренды недвижимости в Москве")
    st.markdown("---")
    
    # Показываем основную информацию о данных
    st.subheader("Обзор данных")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Всего объявлений", len(df))
    
    with col2:
        st.metric("Колонок в данных", len(df.columns))
    
    with col3:
        # Проверяем наличие ключевых колонок
        key_columns = ['Цена', 'Высота потолков, м', 'Можно с детьми/животными']
        missing_cols = [col for col in key_columns if col not in df.columns]
        if missing_cols:
            st.metric("Отсутствующие колонки", len(missing_cols))
        else:
            st.metric("Данные готовы", "✅")
    
    # Показываем первые несколько строк данных
    with st.expander("📊 Посмотреть данные"):
        st.dataframe(df.head(10))
    
    st.markdown("---")
    
    # Анализ пропущенных значений (добавлено в начало)
    create_missing_data_analysis(df)
    
    st.markdown("---")
    
    # Анализ животных и детей
    create_animal_child_analysis(df)
    
    st.markdown("---")
    
    # Анализ высоты потолков
    # Создаем вкладки для разных вариантов анализа
    tab1, tab2 = st.tabs(["📏 Детальный анализ потолков", "📏 Упрощенный анализ потолков"])
    
    with tab1:
        create_ceiling_height_analysis(df)
    
    with tab2:
        simple_ceiling_analysis(df)

# Запускаем приложение
if __name__ == "__main__":
    main()