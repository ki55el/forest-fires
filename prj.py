import io
import json
from PIL import Image
import numpy as np
import streamlit as st
import tifffile as tiff
from tensorflow.python.keras.models import load_model
from api import call_api

st.title("Предиктивная оценка возникновения лесных пожаров")
st.markdown("---")
st.write("Выполнено командой «Декада»")

latitude = st.number_input('Введите широту', format="%.6f")
longitude = st.number_input('Введите долготу', format="%.6f")
date = st.date_input('Введите дату').strftime("%Y-%m-%d")
img = st.file_uploader('Загрузите изображение', type=['png','jpg','jpeg','tiff'])

if img.type == "image/tiff":
    tiff_image = tiff.imread(img)
        
    if tiff_image.shape[-1] > 3:
            tiff_image = tiff_image[..., :3]

    pil_image = Image.fromarray(np.uint8(tiff_image))

    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    buffer.seek(0)

    st.image(buffer, caption="Загруженное TIFF изображение", use_column_width=True)
else:
    image = Image.open(img)
    st.image(image, caption="Загруженное изображение", use_column_width=True)

model = load_model('model.h5')

predictions = model.predict(X_test)
st.write(model.evaluate(X_test))


results = call_api(str(latitude), str(longitude), str(date))
    
team_name = "Декада"
file_path = f'{team_name}.json'
with open(file_path, 'w') as f:
    json.dump(results, f, indent=4)

st.write("Результат вызова API:")
st.json(results)
    
st.success(f"Результаты успешно сохранены в файл {file_path}")
