# ######################################################################################################
#                                     Proyecto de Localización de Drones
# Autores: Guillermo Aix García, Alejandro Bernabéu Moreno y Miguel Cox Caballero
# Tutor: Celso Molina Ibáñez
# 
# Descripción:
# Este script procesa imágenes de la cámara de un dron, identifica códigos QR, extrae datos codificados y 
# calcula la posición real del dron en tres dimensiones. Luego, si hay una diferencia entre la posición real 
# y la deseada, se corrige la trayectoria del dron.
#
# Detalles del Funcionamiento:
# - Se utilizan los datos de los códigos QR para calcular la posición y la distancia del dron.
# - La posición y distancia se comparan con la posición deseada para corregir la trayectoria.
# - Se implementa un protocolo de comunicación entre Raspberry Pi y Arduino para enviar comandos de corrección.
# - Se utiliza un MPU6050 para proporcionar datos de orientación y aceleración al Arduino para correcciones en vuelo.
# - Se emplea Python en una Raspberry Pi para procesar imágenes y enviar comandos al sistema de control del dron.
#
# Notas Importantes:
# - Este script se divide en dos partes: procesado de imágenes y corrección de error.
# - Se requiere la biblioteca OpenCV y pyzbar para el procesamiento de imágenes y decodificación de códigos QR.
#
# Mini Tutorial para Configurar el Entorno:
# 1. Descargar e instalar Python:
#    - Descarga Python 3.7 o superior desde https://www.python.org/downloads/windows/.
#    - Ejecuta el instalador y asegúrate de marcar la casilla "Add Python to PATH".
# 2. Abrir la Terminal de Windows:
#    - Presiona la tecla de Windows, escribe "cmd" y presiona Enter para abrir la Terminal.
# 3. Instalar las librerías necesarias:
#    - Ejecuta los siguientes comandos en la Terminal:
#      - pip install opencv-python
#      - pip install pyzbar
# ######################################################################################################


# Variables Configurables
video_source = 0  # Número del dispositivo de la cámara (0 para la cámara predeterminada)
angulo_de_vision = 0.74  # Ángulo de visión de la cámara en radianes
lado_cm = 6  # Este valor se actualiza automáticamente con el lado real del código QR

import cv2
from pyzbar import pyzbar
import numpy as np
import os
import math

# Configuración de la interfaz gráfica
fuente = cv2.FONT_HERSHEY_SIMPLEX
tamaño_fuente = 0.5
tamaño_fuente_grande = 0.75  
grosor_fuente = 1
grosor_fuente_grande = 2 
color_fuente = (255, 255, 255)
color_contorno_fuente = (0, 0, 0)

# Fuente del script
nombre_script = os.path.basename(__file__)

# Definiciones de Funciones
def extraer_valores_desde_qr(texto_qr):
    """
    Función para extraer los valores (longitud, coordenadas X e Y) desde un código QR.
    """
    try:
        valores = texto_qr.split(',')
        longitud = float(valores[0])
        x = float(valores[1])
        y = float(valores[2])
        return longitud, x, y
    except Exception as e:
        print(f"Error al extraer los valores: {e}")
        return None, None, None

class DetectorQR:
    """
    Clase que se encarga de detectar y procesar los códigos QR en una imagen.
    """
    def __init__(self, longitud_focal, distancia_maxima):
        self.longitud_focal = longitud_focal
        self.distancia_maxima = distancia_maxima

    def encontrar_codigos_qr(self, frame):
        """
        Función para encontrar códigos QR en una imagen y procesarlos.
        """
        global lado_cm
        objetos_decodificados = pyzbar.decode(frame)
        coordenadas_dron = None
        for obj in objetos_decodificados:
            puntos = obj.polygon
            if len(puntos) > 4:
                hull = cv2.convexHull(np.array([punto for punto in puntos], dtype=np.float32))
                puntos = hull

            longitud, x, y = extraer_valores_desde_qr(obj.data.decode('utf-8'))
            if longitud is not None and x is not None and y is not None:
                lado_cm = longitud  

            longitud_lado = self.calcular_longitud_lado(puntos)
            altura_imagen_cm = (frame.shape[0] / longitud_lado) * lado_cm
            distancia = ((altura_imagen_cm / 2) * math.sin(90 - (angulo_de_vision / 2))) / math.sin(angulo_de_vision / 2)

            cv2.drawContours(frame, [np.int0(puntos)], 0, (255, 0, 255), 2)

            ubicacion_texto_longitud_lado = (obj.rect.left, obj.rect.top - 10)
            cv2.putText(frame, f"Longitud del lado: {longitud_lado:.2f} cm", ubicacion_texto_longitud_lado,
                        fuente, tamaño_fuente, color_contorno_fuente, grosor_fuente + 2, cv2.LINE_AA)
            cv2.putText(frame, f"Longitud del lado: {longitud_lado:.2f} cm", ubicacion_texto_longitud_lado,
                        fuente, tamaño_fuente, color_fuente, grosor_fuente, cv2.LINE_AA)

            ubicacion_texto_altura_imagen = (obj.rect.left, obj.rect.top - 30)
            cv2.putText(frame, f"Altura de la imagen: {altura_imagen_cm:.2f} cm", ubicacion_texto_altura_imagen,
                        fuente, tamaño_fuente, color_contorno_fuente, grosor_fuente + 2, cv2.LINE_AA)
            cv2.putText(frame, f"Altura de la imagen: {altura_imagen_cm:.2f} cm", ubicacion_texto_altura_imagen,
                        fuente, tamaño_fuente, color_fuente, grosor_fuente, cv2.LINE_AA)

            ubicacion_texto_distancia = (obj.rect.left, obj.rect.top - 50)
            cv2.putText(frame, f"Distancia: {distancia:.2f} cm", ubicacion_texto_distancia,
                        fuente, tamaño_fuente, color_contorno_fuente, grosor_fuente + 2, cv2.LINE_AA)
            cv2.putText(frame, f"Distancia: {distancia:.2f} cm", ubicacion_texto_distancia,
                        fuente, tamaño_fuente, color_fuente, grosor_fuente, cv2.LINE_AA)

            x_cm, y_cm, vector = self.calcular_vector(puntos, longitud_lado, x, y)
            coordenadas_dron = (x_cm, y_cm, distancia / 100.0)  

            texto_qr = obj.data.decode('utf-8')
            ubicacion_texto_qr = (obj.rect.left, obj.rect.top - 70)
            cv2.putText(frame, f"Código QR: {texto_qr}", ubicacion_texto_qr,
                        fuente, tamaño_fuente, color_contorno_fuente, grosor_fuente + 2, cv2.LINE_AA)
            cv2.putText(frame, f"Código QR: {texto_qr}", ubicacion_texto_qr,
                        fuente, tamaño_fuente, color_fuente, grosor_fuente, cv2.LINE_AA)

        return objetos_decodificados, frame, coordenadas_dron

    def calcular_longitud_lado(self, puntos):
        """
        Función para calcular la longitud del lado de un cuadrilátero a partir de sus puntos.
        """
        return max([np.linalg.norm(np.array(puntos[i]) - np.array(puntos[(i + 1) % 4])) for i in range(4)])

    def calcular_vector(self, puntos, longitud_lado, x_ref, y_ref):
        """
        Función para calcular un vector a partir de puntos de referencia y coordenadas.
        """
        mitad_frame = (frame.shape[1] // 2, frame.shape[0] // 2)
        mitad_qr = np.mean(puntos, axis=0, dtype=np.intp)

        h_px = mitad_frame[0] - mitad_qr[0]  
        v_px = mitad_qr[1] - mitad_frame[1]

        pixeles_por_cm = longitud_lado / lado_cm
        h_cm = h_px / pixeles_por_cm
        v_cm = v_px / pixeles_por_cm

        x_ref_cm = x_ref * 100
        y_ref_cm = y_ref * 100

        x_final = x_ref_cm + h_cm
        y_final = y_ref_cm + v_cm

        cv2.line(frame, mitad_frame, tuple(mitad_qr), (0, 255, 0), 2)

        offset_texto_x = 10  
        offset_texto_y = 10  
        ubicacion_texto_vector = (mitad_qr[0] + offset_texto_x, mitad_qr[1] + offset_texto_y)
        
        texto_vector = f"Vec:({x_final:.2f},{y_final:.2f}) cm"
        cv2.putText(frame, texto_vector, ubicacion_texto_vector,
                    fuente, tamaño_fuente, color_contorno_fuente, grosor_fuente + 2, cv2.LINE_AA)
        cv2.putText(frame, texto_vector, ubicacion_texto_vector,
                    fuente, tamaño_fuente, color_fuente, grosor_fuente, cv2.LINE_AA)

        return x_final / 100.0, y_final / 100.0, texto_vector  

# Inicialización de Variables
video_source = 0
longitud_focal = 850.0
distancia_maxima = 200.0
angulo_de_vision = 0.74
lado_cm = 6  

# Inicialización del Detector QR
detector_qr = DetectorQR(longitud_focal, distancia_maxima)

# Inicializar captura de video de la cámara
cap = cv2.VideoCapture(video_source)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  

# Obtener dimensiones de la cámara
_, frame = cap.read()
altura, ancho, _ = frame.shape
dimensiones_camara = f"Dimensiones de la cámara: {ancho}x{altura}"

# Bucle Principal (Procesamiento de Video)
while True:
    ret, frame = cap.read()
    if ret:
        objetos_decodificados, frame_anotado, coordenadas_dron = detector_qr.encontrar_codigos_qr(frame)

        cv2.putText(frame_anotado, nombre_script, (10, frame_anotado.shape[0] - 10),
                    fuente, tamaño_fuente, (192, 192, 192, 128), grosor_fuente, cv2.LINE_AA)
        cv2.putText(frame_anotado, dimensiones_camara, (10, frame_anotado.shape[0] - 30),
                    fuente, tamaño_fuente, (192, 192, 192, 128), grosor_fuente, cv2.LINE_AA)

        # Mostrar coordenadas del dron en texto grande
        if coordenadas_dron:
            x, y, z = coordenadas_dron
            texto_coordenadas_dron = f"x={x:.3f} m, y={y:.3f} m, z={z:.3f} m"
            cv2.putText(frame_anotado, texto_coordenadas_dron, (10, 50),
                        fuente, tamaño_fuente_grande, color_contorno_fuente, grosor_fuente_grande + 2, cv2.LINE_AA)
            cv2.putText(frame_anotado, texto_coordenadas_dron, (10, 50),
                        fuente, tamaño_fuente_grande, color_fuente, grosor_fuente_grande, cv2.LINE_AA)

        cv2.imshow('Frame', frame_anotado)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
