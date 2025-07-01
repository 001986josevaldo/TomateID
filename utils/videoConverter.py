import subprocess
import os

class VideoConverter:
    @staticmethod
    def convert_video_to_h264(input_video):
        """
        Converte um vídeo para o codec H.264 usando ffmpeg, sobrescrevendo o arquivo original.
        Não exibe o processo no terminal.
        """
        try:
            temp_output = input_video + ".tmp.mp4"
            command = [
                "ffmpeg",
                "-i", input_video,
                "-vcodec", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "medium",
                "-crf", "23",
                temp_output
            ]
            # Executa o comando, suprimindo stdout e stderr
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            os.replace(temp_output, input_video)
            return True
        except subprocess.CalledProcessError:
            # Aqui você pode registrar em log se quiser
            return False
