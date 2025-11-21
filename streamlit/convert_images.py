# convert_images.py - запустите этот файл локально
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