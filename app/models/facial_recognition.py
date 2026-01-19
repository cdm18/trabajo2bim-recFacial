import face_recognition
import cv2
import pickle
import os
import numpy as np

class SistemaReconocimientoFacial:
    def __init__(self, ruta_encodings="encodings.pickle", metodo_deteccion="hog"):
        # inicializa el sistema cargando los datos ya entrenados
        self.ruta_encodings = ruta_encodings
        self.metodo_deteccion = metodo_deteccion
        self.data = self._cargar_encodings()

    def _cargar_encodings(self):
        # intenta cargar el archivo pickle mas si falla devuelve listas vacias
        if not os.path.exists(self.ruta_encodings):
            return {"encodings": [], "names": []}
        
        try:
            with open(self.ruta_encodings, "rb") as f:
                return pickle.loads(f.read())
        except Exception as e:
            print(f"[error] no se pudo cargar encodings: {e}")
            return {"encodings": [], "names": []}

    def procesar_frame(self, frame, tolerancia=0.5):
        # achicamos el frame a la mitad para que procese mas rapido
        rgb_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small = cv2.cvtColor(rgb_small, cv2.COLOR_BGR2RGB)

        # buscamos las caras y sacamos sus caracteristicas
        cajas = face_recognition.face_locations(rgb_small, model=self.metodo_deteccion)
        encodings = face_recognition.face_encodings(rgb_small, cajas)

        nombres = []
        confianzas = []

        for encoding in encodings:
            # calculamos distancias euclidianas contra todos los conocidos
            distancias = face_recognition.face_distance(self.data["encodings"], encoding)
            
            # vemos si hay match segun la tolerancia
            coincidencias = face_recognition.compare_faces(self.data["encodings"], encoding, tolerance=tolerancia)
            
            nombre = "Desconocido"
            confianza = 0.0

            if True in coincidencias:
                indices_coicidentes = [i for (i, b) in enumerate(coincidencias) if b]
                
                # elegimos el que tenga menor distancia (mas parecido)
                mejor_indice = None
                mejor_distancia = 1.0
                
                for i in indices_coicidentes:
                    if distancias[i] < mejor_distancia:
                        mejor_distancia = distancias[i]
                        mejor_indice = i
                
                if mejor_indice is not None:
                    nombre = self.data["names"][mejor_indice]
                    # convertimos distancia inversa a porcentaje de confianza
                    confianza = (1.0 - mejor_distancia) * 100

            nombres.append(nombre)
            confianzas.append(confianza)

        # pintamos los cuadritos en el frame original
        for ((top, right, bottom, left), nombre, conf) in zip(cajas, nombres, confianzas):
            # como achicamos a la mitad, ahora multiplicamos x2
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            color = (0, 0, 255) if nombre == "Desconocido" else (0, 255, 0)

            # dibujamos el rectangulo
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            etiqueta = nombre
            if nombre != "Desconocido":
                etiqueta = f"{nombre} ({conf:.1f}%)"
            
            # dibujamos la etiqueta abajo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, etiqueta, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        return frame

    def entrenar_modelo(self, dataset_path="dataset"):
        # recolectamos primero todas las imagenes para saber cuantas son
        archivos_imagen = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.PNG')):
                    path = os.path.join(root, file)
                    name = os.path.basename(root)
                    archivos_imagen.append((path, name))

        if not archivos_imagen:
            print("[info] no hay imagenes para entrenar")
            return False

        print(f"[info] se encontraron {len(archivos_imagen)} imagenes")

        known_encodings = []
        known_names = []

        # procesamos imagen por imagen
        for i, (path, name) in enumerate(archivos_imagen):
            print(f"[info] procesando {i + 1}/{len(archivos_imagen)}: {name}")
            
            imagen = cv2.imread(path)
            if imagen is None:
                continue
                
            rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            # detectamos caras en la imagen de entrenamiento
            cajas = face_recognition.face_locations(rgb, model=self.metodo_deteccion)
            encodings = face_recognition.face_encodings(rgb, cajas)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)

        print("[info] guardando datos en pickle...")
        data = {"encodings": known_encodings, "names": known_names}
        with open(self.ruta_encodings, "wb") as f:
            f.write(pickle.dumps(data))
        
        # recargamos en memoria para que funcione al instante
        self.data = data
        return True
