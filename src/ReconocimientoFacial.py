import cv2
import face_recognition
import numpy as np
import pymysql
import os

# Conexión a la base de datos
def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="", db="db_secure_place")

# Cargar imágenes de la base de datos
def load_images_from_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT dni, foto FROM users WHERE foto IS NOT NULL")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    
    known_face_encodings = []
    known_face_dnis = []
    
    for user in users:
        dni, photo_path = user
        image_path = os.path.join('static', photo_path)
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            if image is None:
                print(f"No se pudo cargar la imagen para {dni} desde {image_path}")
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if len(image.shape) == 3 and image.shape[2] == 3:  # Asegurarse de que la imagen está en formato RGB
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_dnis.append(dni)
                else:
                    print(f"No se encontraron rostros en la imagen de {dni}")
            else:
                print(f"Imagen de {dni} no está en formato RGB: {image_path}")
    
    return known_face_encodings, known_face_dnis

known_face_encodings, known_face_dnis = load_images_from_db()

# Configuración del flujo de video
video_stream_url = "http://192.168.1.2:8080/live/stream.m3u8"

video_capture = cv2.VideoCapture(video_stream_url)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("No se pudo obtener el frame del video")
        break

    # Redimensionar el frame para procesarlo más rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convertir el frame de BGR a RGB
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconocido"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_dnis[best_match_index]

        print(f"Rostro detectado: {name}")

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
