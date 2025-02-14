import fitz
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

def remove_grid(image):
    # Преобразуем изображение в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Определяем диапазон синего цвета (сетку)
    lower_blue = np.array([110, 40, 60])
    upper_blue = np.array([130, 255, 255])

    # Создаем маску для синего цвета
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Применяем морфологическую операцию для улучшения маски (удаляем мелкие шумы)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Убираем мелкие артефакты

    # Применяем маску к изображению, оставляя только те пиксели, которые соответствуют маске
    blue_area = cv2.bitwise_and(image, image, mask=mask)

    # Заменяем черный фон на белый
    white_background = np.ones_like(image) * 255
    final_image = np.where(blue_area == 0, white_background, blue_area)

    # Применяем размытие для устранения мелких артефактов
    final_image = cv2.GaussianBlur(final_image, (3, 3), 0)

    return final_image

def process_pdf(input_pdf, output_pdf):
    # Конвертируем PDF в изображения
    images = convert_from_path(input_pdf, dpi=600)
    processed_images = []
    
    for img in images:
        # Конвертируем PIL изображение в OpenCV
        open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        processed_image = remove_grid(open_cv_image)
        processed_images.append(Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)))
        print(
            int(len(processed_images) / len(images) * 100)
        )
    
    # Собираем PDF обратно
    processed_images[0].save(output_pdf, save_all=True, append_images=processed_images[1:])
    
if __name__ == "__main__":
    input_pdf = "input.pdf"  # Укажите путь к исходному PDF
    output_pdf = "output.pdf"  # Имя выходного файла
    process_pdf(input_pdf, output_pdf)
    print("Обработка завершена. Файл сохранен как", output_pdf)
