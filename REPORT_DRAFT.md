# Informe de Proyecto: Sistema de Reconocimiento Facial

## 1. Informe de Revisión de Literatura y Método

### Introducción
El reconocimiento facial es una tecnología biométrica que identifica o verifica a una persona en una imagen digital o video. Este proyecto implementa una solución basada en el aprendizaje profundo (Deep Learning).

### Tecnologías Utilizadas
*   **Python**: Lenguaje de programación principal.
*   **OpenCV**: Biblioteca de visión por computador utilizada para el procesamiento de imágenes y captura de video.
*   **Dlib**: Biblioteca de C++ moderna que contiene algoritmos de aprendizaje automático, incluyendo el detector facial HOG y la red neuronal profunda para generar los "encodings" (codificaciones) faciales.
*   **Face_recognition**: Una API de alto nivel construida sobre dlib que simplifica el proceso de detección y reconocimiento.

### Estado del Arte (Referencias sugeridas para buscar)
1.  *Histograms of Oriented Gradients for Human Detection* (Dalal & Triggs, 2005): Base del detector facial HOG.
2.  *Deep Residual Learning for Image Recognition* (He et al., 2016): Arquitectura ResNet utilizada para los embeddings.
3.  *FaceNet: A Unified Embedding for Face Recognition and Clustering* (Schroff et al., 2015): Introduce el concepto de triplet loss y embeddings faciales.

## 2. Definición del Producto

### Objetivos
*   Implementar un sistema local de reconocimiento facial.
*   Entrenar el modelo con un conjunto de datos personalizado de estudiantes.
*   Identificar rostros en tiempo real (video) e imágenes estáticas.

### Descripción
El sistema es una aplicación de escritorio que utiliza la cámara web para escanear el entorno, detectar rostros humanos y compararlos con una base de datos pre-entrenada para mostrar el nombre de la persona identificada en pantalla.

## 3. Planteamiento de la Arquitectura y Desarrollo

### Arquitectura del Sistema
El flujo de datos sigue la siguiente tubería (pipeline):

1.  **Adquisición**: Captura de imagen (Webcam o archivo).
2.  **Pre-procesamiento**: Conversión a RGB y redimensionado para eficiencia.
3.  **Detección Facial (Face Detection)**:
    *   Se utiliza el algoritmo **HOG (Histogram of Oriented Gradients)** para localizar rostros en la imagen.
4.  **Extracción de Características (Feature Extraction)**:
    *   Se utiliza una Red Neuronal Convolucional (CNN) pre-entrenada para generar un vector de **128 dimensiones** (embedding) por cada rostro.
    *   Este vector representa numéricamente las características únicas del rostro.
5.  **Clasificación (Matching)**:
    *   Se calcula la **Distancia Euclidiana** entre el vector del rostro detectado y los vectores almacenados en `encodings.pickle`.
    *   Si la distancia es menor a un umbral (tolerancia), se considera una coincidencia.
6.  **Salida**: Superposición del nombre y caja delimitadora (bounding box) sobre la imagen original.

### Desarrollo
El código se estructura en tres scripts principales:
*   `train_model.py`: Genera los embeddings.
*   `recognize_video.py`: Motor de inferencia en tiempo real.
*   `recognize_image.py`: Motor de inferencia estática.

## 4. Resultados de las Pruebas (Experimentación)

*Esta sección debe ser completada por el estudiante con sus pruebas específicas.*

### Prueba 1: Variación de Iluminación
*   **Descripción**: Se probó el reconocimiento en condiciones de baja luz.
*   **Resultado**: (Ejemplo: El sistema falló al detectar el rostro, o lo reconoció con lentitud).

### Prueba 2: Oclusión Parcial
*   **Descripción**: El estudiante usó gafas o mascarilla.
*   **Resultado**: ...

### Prueba 3: Distancia
*   **Descripción**: El estudiante se alejó a 3 metros de la cámara.
*   **Resultado**: ...

## 5. Conclusiones
*   La librería `dlib` proporciona una robustez significativa en la detección facial mediante HOG.
*   El uso de embeddings de 128 dimensiones permite una comparación rápida y ligera, adecuada para sistemas en tiempo real.
*   (Añadir conclusiones propias sobre las dificultades encontradas y la precisión del sistema).

## 6. Referencias Bibliográficas
*   King, D. E. (2009). Dlib-ml: A Machine Learning Toolkit. Journal of Machine Learning Research, 10, 1755-1758.
*   Geitgey, A. (2018). Face Recognition. GitHub Repository.
