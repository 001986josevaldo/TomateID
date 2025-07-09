import cv2
import time


class IntroOverlay:
    def __init__(self, frase="Created by: josevaldomr@gmail.com"):
        self.frase = frase

    def redimensionar_frame(self, frame, largura=840):
        altura = int(frame.shape[0] * (largura / frame.shape[1]))
        return cv2.resize(frame, (largura, altura))

    def exibir_primeiro_frame(self, video_capture):
        """
        Exibe o primeiro frame com frase sobreposta por 3 segundos.
        :param video_capture: objeto cv2.VideoCapture já inicializado
        
        #ret, frame = video_capture.read()

        if not ret:
            print("❌ Não foi possível capturar o primeiro frame.")
            return False"""
        frame = cv2.imread("image/tomateId.png")
        
        if frame is None:
            raise RuntimeError("❌ Não foi possível carregar a imagem.")
        frame = self.redimensionar_frame(frame)
        # Adiciona a frase no frame
        altura, largura = frame.shape[:2]
        cv2.putText(
            frame,
            self.frase,
            (150, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        # Exibe por 3 segundos
        cv2.imshow("TomateID", frame)
        cv2.waitKey(3000)  # 3000 ms = 3 s
        cv2.destroyWindow("TomateID")

        # Volta o frame lido para o fluxo (se desejar, podemos reusar)
        return True
