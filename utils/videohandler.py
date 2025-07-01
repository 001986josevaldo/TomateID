import cv2
import os
from datetime import datetime

class VideoHandler:
    def __init__(self, input_source):
        """
        Inicializa com a fonte de entrada: caminho do arquivo (str) ou índice da câmera (int).
        """
        self.input_source = input_source
        self.video_capture = None
        self.video_writer = None
        self.output_path = None
        self.frame_size = None
        self.fps = 30
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    def initialize(self, redimensionar_frame_func):
        """
        Abre o vídeo/câmera e prepara o VideoWriter.
        redimensionar_frame_func: função usada para redimensionar os frames.
        """
        self.video_capture = cv2.VideoCapture(self.input_source)

        if not self.video_capture.isOpened():
            raise RuntimeError("❌ Não foi possível abrir o vídeo ou câmera.")

        ret, frame = self.video_capture.read()
        if not ret:
            raise RuntimeError("❌ Erro ao capturar o primeiro frame.")

        # Redimensiona o frame conforme o processo desejado
        frame_redimensionado = redimensionar_frame_func(frame)
        altura, largura = frame_redimensionado.shape[:2]
        self.frame_size = (largura, altura)

        # Define o nome do arquivo de saída
        if isinstance(self.input_source, str):
            input_filename = os.path.basename(self.input_source)
            name_without_ext, _ = os.path.splitext(input_filename)
            self.output_path = f"Processed/{name_without_ext}.mp4"
        else:
            self.output_path = f"Processed/camera_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # Cria o VideoWriter
        self.video_writer = cv2.VideoWriter(self.output_path, self.fourcc, self.fps, self.frame_size)

    def write_frame(self, frame):
        """
        Escreve um frame no vídeo de saída.
        """
        self.video_writer.write(frame)

    def release(self):
        """
        Libera recursos de vídeo/câmera e fecha arquivos.
        """
        if self.video_capture:
            self.video_capture.release()
        if self.video_writer:
            self.video_writer.release()
        cv2.destroyAllWindows()

    def get_output_path(self):
        """
        Retorna o caminho do arquivo de saída.
        """
        return self.output_path
