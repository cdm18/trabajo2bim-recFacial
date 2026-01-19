# Guía de Comandos (Cheatsheet)

Aquí tienes los comandos exactos que necesitas ejecutar en tu terminal para controlar el proyecto paso a paso.

## 1. Preparación del Entorno
Si cierras la terminal, siempre debes volver a activar el entorno virtual primero:
```powershell
.\venv\Scripts\activate
```
*(Verás que aparece `(venv)` al principio de la línea de comandos)*

## 2. Entrenamiento del Modelo
Cada vez que agregues fotos nuevas de estudiantes a la carpeta `dataset`, debes ejecutar esto para que el sistema "aprenda" los nuevos rostros.
```powershell
python train_model.py --dataset dataset --encodings encodings.pickle
```

## 3. Reconocimiento en Video (Tiempo Real)
Para probar el sistema con tu cámara web:
```powershell
python recognize_video.py --encodings encodings.pickle
```
*Presiona la tecla `q` para salir y cerrar la cámara.*

## 4. Reconocimiento en Imagen Estática
Para probar con una foto guardada (cambia `ruta/a/la/foto.jpg` por tu archivo real):
```powershell
python recognize_image.py --encodings encodings.pickle --image "dataset/Antuan Agurto/imagen.jpeg"
```

## 5. Experimentación

### Ajustar la Tolerancia (Estrictez)
Si el sistema confunde personas, puedes hacer más estricto el reconocimiento bajando la tolerancia:
```powershell
python recognize_video.py --encodings encodings.pickle --tolerance 0.45
```
*   **Tolerancia por defecto**: 0.5
*   **Más estricto (menos falsos positivos)**: 0.4 o 0.45
*   **Menos estricto (reconoce más pero puede confundir)**: 0.6

### Cambiar el Método de Detección
Por defecto es `hog` (rápido). `cnn` es más preciso pero lento:
```powershell
python recognize_video.py --encodings encodings.pickle --detection-method cnn
```
