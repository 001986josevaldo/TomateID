import cv2

def obter_resolucao_video(caminho_do_video):
    """
    Retorna a resolução (largura x altura) de um vídeo no formato 'LARGURAxALTURA'
    
    Parâmetros:
        caminho_do_video (str): Caminho para o arquivo de vídeo
        
    Retorna:
        str: Resolução no formato 'LARGURAxALTURA' ou mensagem de erro
    """
    try:
        # Abre o vídeo
        video = cv2.VideoCapture(caminho_do_video)
        
        # Verifica se o vídeo foi aberto corretamente
        if not video.isOpened():
            return "Erro: Não foi possível abrir o vídeo."
        
        # Obtém as dimensões
        largura = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        altura = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Libera o vídeo
        video.release()
        
        return f"{largura}x{altura}"
    
    except Exception as e:
        return f"Erro: {str(e)}"

# Exemplo de uso
if __name__ == "__main__":
    caminho = input("Digite o caminho do arquivo de vídeo: ")
    resolucao = obter_resolucao_video(caminho)
    print(f"Resolução do vídeo: {resolucao}")