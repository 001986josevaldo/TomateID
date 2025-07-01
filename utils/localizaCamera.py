import cv2

def localizar_proxima_camera_externa(max_cameras=5):
    """
    Localiza o primeiro índice de câmera disponível além da integrada (índice 0).
    :param max_cameras: número máximo de índices a testar
    :return: índice da câmera disponível ou None
    """
    for index in range(1, max_cameras):  # começa em 1 para ignorar a integrada
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cap.release()
            print(f"🎥 Câmera externa disponível encontrada no índice {index}")
            return index
        cap.release()
    print("❌ Nenhuma câmera externa disponível encontrada.")
    return None
