''' Dados do treinamento no colab
Ultralytics 8.3.145 🔬 
Python-3.11.12 
torch-2.6.0+cu124 
CUDA:0 (Tesla T4, 15095MiB)'''

import cv2
from ultralytics import YOLO
from utils.sort import *
import cvzone
import time
import os
from utils.videoConverter import VideoConverter
from utils.videohandler import VideoHandler


# Carrega o modelo YOLO
model = YOLO("modelos/modeloTomate.pt")
tracker = Sort(max_age=30)  # Rastreador


# Redimensiona o frame para uma largura fixa (ex: 840px), mantendo a proporção
def redimensionar_frame(frame, largura=840):
    altura = int(frame.shape[0] * (largura / frame.shape[1]))
    frame = cv2.resize(frame, (largura, altura))
    return frame

# Caminho do vídeo de entrada
input_source= 'videos/tomateEsteira.mp4'
#input_source = 0  # ou 'videos/tomate2.mp4'

#video_path = cv2.VideoCapture(input_path)

vh = VideoHandler(input_source)
vh.initialize(redimensionar_frame)


# Classes de veículos
classNames = ["Bom", "Geral", "Grave",]

while True:
    ret, img = vh.video_capture.read()
    if img is None:
        break
    
    # Redimensiona o frame
    img = redimensionar_frame(img)
    print("size",img.size[:2])
    # Detecta 
    results = model(img, stream=True)
    detections = np.empty((0,5))
  

    # itera sobre todos os objetos detectados
    for obj in results:
        dados = obj.boxes
        for x in dados:
            #conf
            conf = int(x.conf[0]*100)
            cls = int(x.cls[0])
            nomeClass = classNames[cls]

            #if conf >= 50 and nomeClass == "carro" or nomeClass=="moto" or nomeClass=="caminhao":

            # Coordenadas do bounding box
            x1, y1, x2, y2 = x.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            # Calcula o centro do bounding box
            cx, cy = x1 + w // 2, y1 + h // 2  
            cv2.putText(img, nomeClass, ((x1-10), y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            #cv2.putText(img, str(conf), (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 1)# desenha o retangulo nos objettos
            crArray = np.array([x1,y1,x2,y2,conf])
            detections = np.vstack((detections,crArray))
            

    resultTracker = tracker.update(detections)
    for result in resultTracker:
        x1,y1,x2,y2,id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        cx,cy = x1+w//2, y1+h//2 # meio dos objetos
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 1)# desenha o retangulo nos objettos
        #cvzone.putTextRect(img,str(int(id)),(x1,y1-10),scale=1,thickness=1)
#------------------------------------------------------------------------------------------------\
    if cv2.waitKey(1) == 27:
        break
    # Escrever o frame no vídeo
    vh.write_frame(img)

    cv2.imshow('Classificador',img)

# Fechar o vídeo e arquivo de texto
vh.release()
vh.release()
cv2.destroyAllWindows()
VideoConverter.convert_video_to_h264(vh.get_output_path())

