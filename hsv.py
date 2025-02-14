import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('tets.png')

# Преобразование в HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

fragment = hsv_image

# Поиск минимальных и максимальных значений в фрагменте
min_hue = np.min(fragment[:,:,0])
max_hue = np.max(fragment[:,:,0])
min_saturation = np.min(fragment[:,:,1])
max_saturation = np.max(fragment[:,:,1])
min_value = np.min(fragment[:,:,2])
max_value = np.max(fragment[:,:,2])

print(f"Диапазон оттенков (H): {min_hue} - {max_hue}")
print(f"Диапазон насыщенности (S): {min_saturation} - {max_saturation}")
print(f"Диапазон яркости (V): {min_value} - {max_value}")
