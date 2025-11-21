import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
#nazvanie
#opisanie
st.title('REAL ESTATE AGENCY')
import streamlit as st



st.title(" AI REA Ltd - Отчет по проекту")
st.markdown("---")

st.header("О проекте")
st.write("""
Мы начали работу в отделе аналитики и оптимизации международного сервиса по продаже и аренде жилой недвижимости 
**Alyona Ivanovna Real Estate Agency (AI REA Ltd)**. Наш сервис пользуется популярностью у сотен тысяч клиентов 
со всего мира, включая студентов из разных городов и стран.
""")

st.header("Поставленная задача")
st.write("""
**Основная цель:** Создать модель машинного обучения для оценки стоимости аренды квартир, которая будет 
максимально приближена к ценам, устанавливаемым людьми.

**Техническое требование:** Улучшить метрику качества модели MAPE с 50% до 30% и менее. 
MAPE (Mean Absolute Percentage Error) - средняя абсолютная ошибка в процентах, понятная для менеджеров.

**Пилотный регион:** Москва.
""")

st.header("Этапы работы (Релизы)")

st.subheader("Релиз 1.0 - Exploratory Data Analysis (EDA)")
st.write("""
- Проведен разведочный анализ данных
- Создан HTML-отчет с графиками и агрегированной информацией
- Изучены особенности и структура данных по аренде недвижимости в Москве
""")

st.subheader("Релиз 2.0 - Очистка данных")
st.write("""
- Обработаны пропущенные значения (NaN, None)
- Приведены названия колонок к английскому языку
- Подготовлен чистый dataset для дальнейшей работы
""")

st.subheader("Релиз 3.0 - Feature Engineering")
st.write("""
- Созданы новые признаки для улучшения качества модели
- Все данные преобразованы в числовой формат
- Удалены дубликаты объявлений
- Подготовлен финальный dataset для обучения моделей
""")

st.header("Ключевые выводы")
st.write("""
1. **Качество данных** - основа успеха любой ML-модели
2. **Тщательная подготовка** данных позволяет значительно улучшить метрики
3. **Feature engineering** - критически важный этап для достижения целевого MAPE ≤30%
4. **Московский рынок** недвижимости имеет свои особенности, которые необходимо учитывать в модели
""")

st.success("Проект успешно завершен! Данные готовы для обучения моделей машинного обучения.")

import base64
import os

print("=== КОНВЕРТАЦИЯ PNG В BASE64 ===")
print("Скопируйте этот код в main1.py:\n")

image_files = [f for f in os.listdir() if f.endswith('.png')]

print("images_base64 = {")
for image_file in sorted(image_files):
    try:
        with open(image_file, "rb") as img_file:
            base64_data = base64.b64encode(img_file.read()).decode()
            print(f'    "{image_file}": """{base64_data}""",')
    except Exception as e:
        print(f"# Ошибка с {image_file}: {e}")
print("}")
