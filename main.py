
from tomateDetector import TomateDetector  # Salve a classe acima como detector.py
from utils.localizaCamera import localizar_proxima_camera_externa

def main(linhas):
    
    #input_source = monitor.monitor_and_get_video()
    input_source = localizar_proxima_camera_externa()
    #input_source = "/media/josevaldo/E02A-3159/Ceagre/App/videos/video1.mp4"
    #input_source = 
    if input_source is None:
        print("Encerrando: nenhuma câmera externa disponível.")
        return 
    
    detector = TomateDetector()
    detector.processar_video(input_source, linhas)

if __name__ == "__main__":
    # Caminho do vídeo de entrada
    #input_source = 'videos/tomateEsteira.mp4'
    #input_source = 2  # ou 'videos/tomate2.mp4'
     
    
    linhas = (420,0,420, 630)
    #video_path = cv2.VideoCapture(input_path)
    main(linhas)
