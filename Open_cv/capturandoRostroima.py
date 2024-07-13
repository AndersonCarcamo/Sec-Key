import cv2
import os
import imutils
import numpy as np
import random

# Nombre de la persona y rutas
personName = 'yami'
dataPath = 'C:/Users/Acer/Desktop/ciclo/icc/proyecto/reconocimiento_facial/Open_cv/Data'  # Cambia a la ruta donde hayas almacenado Data
personPath = os.path.join(dataPath, personName)

# Crear carpeta si no existe
if not os.path.exists(personPath):
    print('Carpeta creada: ', personPath)
    os.makedirs(personPath)

# Cargar la imagen
image_path = 'C:/Users/Acer/Desktop/ciclo/icc/proyecto/reconocimiento_facial/Open_cv/Imagenes y Videos de Prueba/ima1.jpg'  # Cambia esta ruta a la imagen que quieres usar
frame = cv2.imread(image_path)

if frame is None:
    print('No se pudo abrir la imagen.')
    exit()

# Inicializar el clasificador de caras
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
count = 0

# Redimensionar la imagen para procesar mejor
frame = imutils.resize(frame, width=640)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

faces = faceClassif.detectMultiScale(gray, 1.3, 5)

if len(faces) == 0:
    print('No se detectaron caras en la imagen.')
    exit()

# Función para ajustar el brillo y el contraste
def apply_brightness_contrast(image, brightness=0, contrast=0):
    if brightness != 0:
        shadow = brightness if brightness > 0 else 0
        highlight = 255 if brightness > 0 else 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

# Procesar cada rostro detectado
for (x, y, w, h) in faces:
    rostro = frame[y:y + h, x:x + w]

    # Generar 300 variaciones de la cara detectada
    for i in range(300):
        # Redimensionar
        rostro_resized = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

        # Aplicar transformaciones aleatorias
        # Rotación aleatoria entre -10 y 10 grados
        angle = random.uniform(-10, 10)
        M = cv2.getRotationMatrix2D((75, 75), angle, 1)
        rostro_transformed = cv2.warpAffine(rostro_resized, M, (150, 150))

        # Brillo aleatorio entre -50 y 50
        brightness = random.randint(-50, 50)
        # Contraste aleatorio entre -50 y 50
        contrast = random.randint(-50, 50)
        rostro_transformed = apply_brightness_contrast(rostro_transformed, brightness, contrast)

        # Guardar la imagen transformada
        rostro_path = os.path.join(personPath, f'rostro_{count}.jpg')
        cv2.imwrite(rostro_path, rostro_transformed)
        count += 1

    # Dibujar un rectángulo alrededor de la cara detectada (opcional)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Mostrar la imagen con la detección (opcional)
cv2.imshow('Image', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
