# Guía de Defensa del Proyecto: Sistema de Reconocimiento Facial

Este documento contiene la defensa técnica detallada del proyecto. Úsalo para responder preguntas específicas sobre el código, la arquitectura y el funcionamiento interno.

---

## 1. Arquitectura del Sistema

El sistema utiliza una arquitectura **MVC (Modelo-Vista-Controlador)** desacoplada:

1.  **Vista (Frontend)**: HTML/CSS/JS. Se encarga de la presentación y de interrogar al servidor (Polling) sobre el estado del sistema.
2.  **Controlador (Backend/Flask)**: `app/routes/main.py`. Orquesta las peticiones, gestiona el streaming de video y maneja la concurrencia (hilos).
3.  **Modelo (Lógica de Negocio)**: `app/models/facial_recognition.py`. Encapsula las librerías de visión artificial (OpenCV, Dlib).

---

## 2. Auditoría de Código: Análisis Detallado

Si el profesor te pide ver el código, dirígete a estos puntos clave. Estas son las líneas que definen el proyecto.

### Archivo: `app/models/facial_recognition.py` (El Núcleo de IA)

**La Detección de Rostros**
```python
cajas = face_recognition.face_locations(rgb_small, model=self.metodo_deteccion)
```
*   **Qué hace:** Utiliza el algoritmo HOG (Histogram of Oriented Gradients) para analizar la imagen en escala de grises y encontrar patrones de gradientes que formen un rostro. Devuelve las coordenadas (top, right, bottom, left) de cada cara.

**La Codificación (El paso más crítico)**
```python
encodings = face_recognition.face_encodings(rgb_small, cajas)
```
*   **Qué hace:** Pasa la imagen recortada del rostro por una Red Neuronal Convolucional (CNN) pre-entrenada (ResNet-34).
*   **Resultado:** Transforma la cara en un vector de **128 números flotantes** (embedding). Estos números representan características biométricas únicas. El sistema **no compara imágenes píxel por píxel**, compara estos vectores numéricos.

**La Comparación Matemática**
```python
distancias = face_recognition.face_distance(self.data["encodings"], encoding)
```
*   **Qué hace:** Calcula la **Distancia Euclidiana** entre el vector de la cara detectada y todos los vectores guardados en la base de datos.
*   **Lógica:** A menor distancia, mayor similitud. Si la distancia es 0.0, es la misma persona. Si es mayor a 0.6, es probable que no sean la misma. Nosotros usamos una tolerancia de 0.5 para mayor seguridad.

### Archivo: `app/routes/main.py` (El Servidor Web)

**El Streaming (Generator Function)**
```python
yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
```
*   **Qué hace:** Implementa el protocolo **Multipart Response**.
*   **Por qué:** No enviamos un archivo de video (como MP4). El servidor captura un frame, lo procesa, lo comprime a JPG y lo envía inmediatamente. El navegador recibe una secuencia infinita de imágenes JPG, creando la ilusión de video en tiempo real.

**Manejo de Hilos (Concurrencia)**
```python
hilo = threading.Thread(target=tarea_entrenamiento)
hilo.start()
```
*   **Importancia:** El entrenamiento es una operación bloqueante (usa 100% de CPU y tarda tiempo).
*   **Justificación:** Si ejecutamos esto en el hilo principal de Flask, el servidor se congelaría: el video se detendría y la interfaz web dejaría de responder. Al usar un `Thread` secundario, el servidor sigue sirviendo video y respondiendo peticiones mientras entrena en segundo plano.

---

## 3. Flujo de Datos y Relación entre Componentes

Si preguntan "¿Cómo se conecta todo al pulsar el botón Entrenar?", este es el camino:

1.  **Cliente (Navegador)**: El usuario hace clic en "Re-entrenar".
2.  **JavaScript (`main.js`)**: Lanza una petición asíncrona (`fetch POST`) a la ruta `/entrenar`.
3.  **Flask (`main.py`)**:
    *   Recibe la petición.
    *   Verifica que no se esté entrenando ya (`if is_training...`).
    *   Inicia el hilo secundario (`threading.Thread`).
    *   Devuelve "OK" al navegador inmediatamente (no espera a que termine).
4.  **Motor (`facial_recognition.py`)**:
    *   Empieza a leer fotos del disco.
    *   Actualiza la variable global `is_training = True`.
5.  **Streaming de Video**:
    *   Detecta que `is_training` es verdadero.
    *   Suspende temporalmente el reconocimiento facial (para liberar CPU para el entrenamiento).
    *   Pinta "ENTRENANDO..." en el video.
6.  **Cliente (Polling)**:
    *   El JavaScript pregunta cada segundo a la ruta `/status`.
    *   Cuando el entrenamiento termina, la ruta responde `training: false`.
    *   El JavaScript muestra el mensaje de éxito en verde.

---

## 4. Preguntas de Defensa (Q&A)

**P: ¿Por qué usó `pickle` en lugar de una base de datos?**
R: Por velocidad de acceso. Necesitamos comparar el rostro contra TODOS los usuarios en cada frame de video (30 veces por segundo). Tener los datos cargados en memoria RAM (desde el pickle) es órdenes de magnitud más rápido que hacer una consulta SQL a disco 30 veces por segundo.

**P: ¿Qué pasa si agrego una foto de mala calidad al dataset?**
R: El sistema intenta extraer los "encodings". Si la calidad es tan mala que HOG no detecta una cara, esa imagen se ignora (se salta). Si detecta una cara pero es borrosa, la precisión del reconocimiento futuro para esa persona bajará.

**P: ¿Cómo afecta la tolerancia de 0.5?**
R: La tolerancia define el umbral de rigor.
*   **Menor tolerancia (ej. 0.4)**: Más estricto. Menos falsos positivos (confundir gente), pero más difícil que te reconozca si hay mala luz.
*   **Mayor tolerancia (ej. 0.6)**: Más relajado. Te reconoce fácil, pero puede confundirte con alguien parecido. 0.5 es el balance ideal encontrado empíricamente.

**P: ¿Qué desventaja tiene este sistema?**
R: Al usar HOG, depende mucho de que el rostro esté de frente y bien iluminado. Si la persona gira mucho la cabeza o hay sombras fuertes, HOG puede perder la detección. Un modelo basado en CNN (disponible en la librería) sería más robusto pero mucho más lento en una CPU estándar.