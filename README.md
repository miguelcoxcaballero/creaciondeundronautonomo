# Sistema de Seguimiento de Drones con Códigos QR

Este proyecto consiste en un sistema de seguimiento de drones utilizando códigos QR para determinar la posición del drone en el espacio. El sistema utiliza una cámara montada en el drone para detectar códigos QR en el suelo y calcular su posición en relación con ellos.

## Autores

- Guillermo Aix García
- Alejandro Bernabéu Moreno
- Miguel Cox Caballero

## Tutor

- Celso Molina Ibáñez

## Descripción

El sistema utiliza una cámara conectada a una Raspberry Pi para capturar imágenes del entorno del drone. Utilizando la biblioteca OpenCV y PyZbar, el sistema es capaz de detectar códigos QR en las imágenes. Cada código QR contiene información sobre su posición en el plano y su tamaño.

El programa calcula la posición tridimensional del drone utilizando la información del código QR detectado y la geometría básica. Además, el sistema es capaz de corregir la trayectoria del drone en tiempo real en caso de desviación.

## Requisitos

- Python 3
- OpenCV
- PyZbar

## Instalación


1. Clona este repositorio en tu máquina local:

git clone https://github.com/tu_usuario/sistema-seguimiento-drones.git


2. Instala las dependencias utilizando pip:

pip install opencv-python pyzbar

## Uso

1. Conecta la cámara a la Raspberry Pi.
2. Ejecuta el script principal:

python main.py


3. Observa la salida en tiempo real en la pantalla. Puedes ajustar los parámetros según sea necesario en el archivo `main.py`.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir a este proyecto, por favor, crea una rama con tu función o corrección y envía un pull request.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).
