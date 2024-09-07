import streamlit as st
import folium
from streamlit_folium import st_folium
import re
import requests
import rasterio
import math
import os

# API ключ
api_key = "c4f5fbad958248438ac110221240609"

def get_forecast_data(api_key, latitude, longitude):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={latitude},{longitude}&days=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Не удалось получить данные о погоде")
        return None

# Функция для расчета координат углов
def count_corner(root_dir):
    corners = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.tiff'):
                path = os.path.join(subdir, file)
                with rasterio.open(path) as src:
                    w_real = src.bounds.right - src.bounds.left
                    h_real = src.bounds.top - src.bounds.bottom
                    diff_real = abs(w_real - h_real)
                    w_pic = src.width
                    h_pic = src.height
                    diff_pic = abs(w_pic - h_pic)
                    if (diff_real / diff_pic == 10):
                        to_right_corner = src.bounds.left + 2*(180 * w_real / (math.pi * 6357000))
                        to_bottom = src.bounds.top + (180 * h_real / (math.pi * 6357000))

                        # Добавляем углы в список для использования в отображении
                        corners.append({
                            'left_upper': (src.bounds.top, src.bounds.left),
                            'right_lower': (to_bottom, to_right_corner)
                        })
    return corners


st.title("Предиктивная оценка возникновения лесных пожаров")
st.markdown("---")
st.write("Выполнено командой «Декада»")


# Путь к папке с файлами TIFF
folder_path = 'train_dataset_train_correct'

# Получаем координаты углов
corners = count_corner(folder_path)

# Если есть координаты, строим карту
if corners:
    
    # Создаем базовую карту с центром по первой точке
    map_center = corners[0]['left_upper']
    m = folium.Map(location=map_center, zoom_start=10)
    folium.TileLayer(
        tiles='https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.jpg',
        attr='&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | '
             '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; '
             '<a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; '
             '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name='Stadia Alidade Satellite',
        min_zoom=0,
        max_zoom=20
    ).add_to(m)
    
    # Добавляем прямоугольники на карту
    for corner in corners:
        left_upper = corner['left_upper']
        right_lower = corner['right_lower']

        center_lat = (left_upper[0] + right_lower[0]) / 2  # Среднее по широте (latitude)
        center_lon = (left_upper[1] + right_lower[1]) / 2

        # latitude = center_lat
        # longitude = center_lon

        #         # Получаем данные прогноза погоды
        # forecast_data = get_forecast_data(api_key, latitude, longitude)

        # if forecast_data:
        #             # Извлекаем текущие погодные условия
        #     current_weather = forecast_data['current']
        #     forecast = forecast_data['forecast']['forecastday'][0]['day']

        #     st.write("### Текущие погодные условия")
        #     st.write(f"Температура: {current_weather['temp_c']}°C")
        #     st.write(f"Минимальная температура за день: {forecast['mintemp_c']}°C")
        #     st.write(f"Максимальная температура за день: {forecast['maxtemp_c']}°C")
        #     st.write(f"Осадки: {forecast['totalprecip_mm']} мм")
        #     st.write(f"Направление ветра: {current_weather['wind_dir']}")
        #     st.write(f"Скорость ветра: {current_weather['wind_kph']} км/ч")
        #     st.write(f"Порывы ветра: {current_weather['gust_kph']} км/ч")
        #     st.write(f"Атмосферное давление: {current_weather['pressure_mb']} мбар")

        
        # Создаем координаты четырех углов для построения полигона
        rectangle_coords = [
            left_upper,  # Левый верхний угол
            (right_lower[0], left_upper[1]),  # Правый верхний угол
            right_lower,  # Правый нижний угол
            (left_upper[0], right_lower[1]),  # Левый нижний угол
        ]
        
        # Добавляем прямоугольник на карту
        folium.Polygon(locations=rectangle_coords, color="blue", fill=True).add_to(m)
        folium.Circle(
            location=[center_lat, center_lon],  # Центр круга
            radius=100,  # Радиус в метрах
            color="red",
            fill=True,
            fill_opacity=0.5
        ).add_to(m)

    # Отображаем карту в Streamlit
    st_folium(m)


else:
    st.write("Прямоугольников для отображения не найдено.")

