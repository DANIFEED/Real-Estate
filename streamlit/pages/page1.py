import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
from PIL import Image

from PIL import Image
import os

st.title("📈 Галерея графиков")
st.markdown("---")

image_files = [f for f in os.listdir() if f.endswith('.png')]

if image_files:
    for image_file in sorted(image_files):
        st.subheader(image_file.replace('.png', '').replace('_', ' ').title())
        image = Image.open(image_file)
        st.image(image, use_container_width=True)
        st.markdown("---")
else:
    st.warning("Графики не найдены. Добавьте PNG файлы в папку с приложением.")