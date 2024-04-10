
![Texto alternativo](https://github.com/miguelcoxcaballero/creaciondeundronautonomo/blob/main/P%C3%B3sterDrone.png?raw=true)


# Creación de un drone autónomo

Este proyecto consiste en un sistema de seguimiento de drones utilizando códigos QR para determinar la posición del drone en el espacio. El sistema utiliza una cámara montada en el drone para detectar códigos QR en el suelo y calcular su posición en relación con ellos.

## Autores

- Guillermo Aix García
- Alejandro Bernabéu Moreno
- Miguel Cox Caballero

## Tutor

- Celso Molina Ibáñez

## Descripción

El sistema utiliza una cámara conectada a un Raspberry Pi, aunque también se puede probar el código en Windows. Utilizando la biblioteca OpenCV y PyZbar, el sistema es capaz de detectar códigos QR en las imágenes. Cada código QR contiene información sobre su posición en el plano y su tamaño.

El programa calcula la posición tridimensional del drone utilizando la información del código QR detectado y trigonometría básica. Además, el sistema es capaz de corregir la trayectoria del drone en tiempo real en caso de desviación.

## Requisitos

- Python 3
- OpenCV
- PyZbar

## Instalación

1. Asegúrate de tener Python 3 instalado. Puedes descargarlo desde [el sitio web oficial de Python](https://www.python.org/downloads/) e instalarlo siguiendo las instrucciones.

2. Abre la terminal (cmd) en tu ordenador.

3. Clona este repositorio en tu máquina local (o simplemente descarga el archivo que quieras usar):

git clone https://github.com/miguelcoxcaballero/creaciondeundronautonomo.git

4. Navega al directorio del repositorio clonado

5. Instala las dependencias utilizando pip:

pip install opencv-python pyzbar

## Uso

1. Conecta la cámara y configura su entrada en el código (si sólo tienes una cámara conectada debería ser automático).

2. Ejecuta el script principal:

python Visión UI.py

3. Observa la salida en tiempo real en la pantalla. Puedes ajustar los parámetros según sea necesario en el archivo `Visión UI.py`.

## Generación de QR

Para evitar tener que generar cada QR con los datos de forma manual, hemos creado dos programas de generación de QR que facilitan su generación e impresión. El primero, `QRgen1.py` permite un uso más simple y el segundo `QrGen1.py` una generación masiva más rápida.

Para utilizar estos programas se necesitan las siguientes librerías:

pip install opencv-python
pip install pyzbar
pip install Pillow

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir a este proyecto, por favor, crea una rama con tu función o corrección y envía un pull request.

