from flask import Blueprint, render_template, Response, jsonify
from app.models.facial_recognition import SistemaReconocimientoFacial
import cv2
import threading

# definimos el blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

# instanciamos el modelo globalmente
sistema = SistemaReconocimientoFacial()
lock = threading.Lock()
is_training = False

def generar_frames():
    # funcion generadora que captura video y lo manda por http
    global lock, is_training
    
    cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        if is_training:
            # si estamos entrenando pausamos el reconocimiento para no cargar la cpu
            cv2.putText(frame, "ENTRENANDO... (pausa)", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            frame_procesado = frame
        else:
            # si no, procesamos normal
            frame_procesado = sistema.procesar_frame(frame)
        
        # codificamos a jpg para el navegador
        (flag, encodedImage) = cv2.imencode(".jpg", frame_procesado)
        if not flag:
            continue
            
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
              bytearray(encodedImage) + b'\r\n')

@main_bp.route("/")
def index():
    # carga la pagina principal
    return render_template("index.html")

@main_bp.route("/video_feed")
def video_feed():
    # ruta del streaming de video
    return Response(generar_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@main_bp.route("/entrenar", methods=["POST"])
def entrenar():
    # endpoint para disparar el entrenamiento en segundo plano
    global is_training
    
    if is_training:
        return jsonify({"status": "error", "message": "ya se esta entrenando"})

    def tarea_entrenamiento():
        global is_training
        is_training = True
        try:
            sistema.entrenar_modelo()
        except Exception as e:
            print(f"error entrenando: {e}")
        finally:
            is_training = False
            
    # lanzamos el hilo daemon para que no bloquee
    hilo = threading.Thread(target=tarea_entrenamiento)
    hilo.start()
        
    return jsonify({"status": "success", "message": "entrenamiento iniciado"})

@main_bp.route("/status")
def status():
    # endpoint para consultar si se esta entrenando
    return jsonify({"training": is_training})
