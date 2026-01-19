# Documentación del Sistema (Importado de DeepWiki)

Esta documentación cubre el sistema de entrenamiento de reconocimiento facial. El sistema proporciona un flujo de trabajo (pipeline) para generar codificaciones faciales (encodings) a partir de conjuntos de datos de imágenes etiquetadas.

## Propósito y Alcance
Esta página proporciona una visión técnica de alto nivel de la arquitectura del sistema, los componentes principales y el flujo de trabajo.

## Visión General del Sistema
El sistema de entrenamiento de reconocimiento facial es un pipeline basado en datos que procesa imágenes de rostros etiquetadas y produce codificaciones faciales serializadas. El sistema consta de tres componentes principales:

1.  `dataset/`: Directorio con las imágenes.
2.  `train_model.py`: Script de procesamiento (ahora ubicado en `legacy/` o integrado en el modelo MVC).
3.  `encodings.pickle`: Archivo de salida con los datos biométricos.

## Arquitectura del Sistema
El script lee del directorio `dataset/` y escribe en `encodings.pickle`. La configuración de `.gitignore` controla qué artefactos se rastrean en el control de versiones.

## Componentes Principales

### Entrada: Estructura del Dataset
El directorio `dataset/` contiene subdirectorios etiquetados por persona con imágenes de entrenamiento. Cada nombre de subdirectorio se convierte en el identificador de la persona en las codificaciones generadas.

**Patrón de Directorio:**
```
dataset/
├── README.txt        # Documentación de estructura
├── Juan_Perez/       # Nombre del subdirectorio = etiqueta de la persona
│   ├── imagen1.jpg   # Se recomiendan 10-20 imágenes
│   ├── imagen2.jpg
│   └── ...
├── Maria_Lopez/
│   ├── foto_1.png
│   └── ...
└── ...
```

### Procesamiento
El componente central de procesamiento acepta argumentos de línea de comandos para definir el dataset y el archivo de salida.

*Comando de ejecución (referencia):*
```bash
python train_model.py --dataset dataset --encodings encodings.pickle
```

### Salida: encodings.pickle
El archivo `encodings.pickle` contiene datos serializados de codificación facial generados a partir de las imágenes de entrenamiento.

## Configuración de Control de Versiones
El archivo `.gitignore` implementa una política de exclusión estratégica:
*   Se excluyen entornos virtuales (`venv/`, `.venv/`).
*   Se excluyen archivos temporales y cachés (`__pycache__`, `*.log`).
*   Se excluyen las imágenes del dataset (`dataset/*`) para privacidad, pero se mantiene `dataset/README.txt`.
*   Se puede excluir opcionalmente el modelo entrenado (`encodings.pickle`).

## Conceptos Clave

### Requisitos de Cantidad de Imágenes
El sistema soporta cantidades flexibles de imágenes:
*   **Mínimo**: 1-2 imágenes por persona (funcional).
*   **Recomendado**: 10-20 imágenes por persona (mejor precisión).
*   **Variación**: Incluir diferentes ángulos y condiciones de iluminación.

### Formatos de Imagen Soportados
El pipeline de entrenamiento procesa:
*   Formato JPG (`.jpg`)
*   Formato PNG (`.png`)

### Identificación de Personas
El nombre del subdirectorio dentro de `dataset/` se convierte en el identificador de la persona.
*   `dataset/Juan_Perez/` → Persona identificada como "Juan_Perez"

## Referencia Rápida
**Archivos de Salida:**
*   `encodings.pickle`: Datos de codificación facial.
*   `*.log`: Registros de entrenamiento.
*   `__pycache__/`: Caché de bytecode de Python.
