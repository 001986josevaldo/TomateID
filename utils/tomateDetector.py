import cv2
import numpy as np
from ultralytics import YOLO
from utils.sort import Sort
from utils.videoConverter import VideoConverter
from utils.videohandler import VideoHandler
from utils.cruzamentoSaver import CruzamentoSaver
from utils.introOverlay import IntroOverlay
class TomateDetector:
    def __init__(self, model_path="modelos/modeloTomate.pt"):
        self.model = YOLO(model_path)
        self.tracker = Sort(max_age=30)
        self.saver = CruzamentoSaver()
        self.classNames = ["Bom", "Geral", "Grave"]

    def redimensionar_frame(self, frame, largura=840):
        altura = int(frame.shape[0] * (largura / frame.shape[1]))
        return cv2.resize(frame, (largura, altura))

    def processar_video(self, input_source, linhas):
        vh = VideoHandler(input_source)
        vh.initialize(self.redimensionar_frame)
        
        Lx1, Ly1, Lx2, Ly2 = linhas
        #print(Lx1, Ly1, Lx2,Ly2)

        historico_cy = {}
        historico_cx = {}
        cruzamentos_registrados = {}

        # Introdução
        overlay = IntroOverlay()
        success = overlay.exibir_primeiro_frame(vh.video_capture)
        if not success:
            # Tratar erro se necessário
            pass

        while True:
            ret, img = vh.video_capture.read()
            if img is None:
                break

            img = self.redimensionar_frame(img)
            #altura, largura = img.shape[:2]
            #print("AlturaxLargura", altura, largura)
            
            
            results = self.model(img, verbose=False)
            detections = np.empty((0, 5))

            

            #cv2.line(img, (420, 20), (420, 350), (255, 255, 0), 2)
            

            for obj in results:
                dados = obj.boxes
                for x in dados:
                    conf = int(x.conf[0] * 100)
                    cls = int(x.cls[0])
                    nomeClass = self.classNames[cls]

                    x1, y1, x2, y2 = x.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    cx, cy = x1 + w // 2, y1 + h // 2  

                    cv2.putText(img, nomeClass, ((x1 - 10), y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                    #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 1)

                    crArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, crArray))

            resultTracker = self.tracker.update(detections)
            
            for result in resultTracker:
                x1, y1, x2, y2, obj_id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 1)

                cx = x1 + (x2 - x1) // 2
                cy = y1 + (y2 - y1) // 2

                # Para cada veículo rastreado
                cy_anterior = historico_cy.get(obj_id)
                cx_anterior = historico_cx.get(obj_id)


                cruzou = (
                    cx_anterior is not None and
                    Ly1 <= cy <= Ly2 and
                    ((cx_anterior < Lx1 <= cx) or (cx_anterior > Lx1 >= cx))
                )                   
                if cruzou:
                   cv2.circle(img, (cx,cy), 5, (0, 165, 255), -1) 
                   cruzamentos_registrados[obj_id] = nomeClass
                   #print(f"✅ ID {obj_id} cruzou: {nomeClass}")

                historico_cx[obj_id] = cx
                historico_cy[obj_id] = cy


            cv2.line(img, (Lx1, Ly1), (Lx2, Ly2), (255, 0, 0), 2)
            vh.write_frame(img)
            cv2.imshow('TomateId', img)

            if cv2.waitKey(1) == 27:  # ESC para sair
                break
        #print(cruzamentos_registrados)
        self.saver.salvar_totais_csv(cruzamentos_registrados, vh.get_output_path())

        vh.release()
        cv2.destroyAllWindows()
        VideoConverter.convert_video_to_h264(vh.get_output_path())
        print(f"✅ Vídeo processado e salvo: {vh.get_output_path()}")
