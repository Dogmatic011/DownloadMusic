import os
import yt_dlp
import subprocess
import sys

def buscar_ffmpeg():
    """Intenta localizar ffmpeg en el sistema"""
    posibles_ubicaciones = [
        # Ubicaciones comunes en Windows
        "C:\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe",
        # Agregar más ubicaciones si es necesario
    ]
    
    # Verificar si ffmpeg está en el PATH
    try:
        result = subprocess.run(['where', 'ffmpeg'] if os.name == 'nt' else ['which', 'ffmpeg'], 
                               capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # Verificar ubicaciones comunes
    for ubicacion in posibles_ubicaciones:
        if os.path.exists(ubicacion):
            return ubicacion
    
    return None

def descargar_videos_mp4(url, ruta_destino, ruta_ffmpeg=None):
    """
    Descarga videos de YouTube en formato MP4 de alta calidad.
    
    Args:
        url: URL del video o playlist de YouTube
        ruta_destino: Ruta donde se guardarán los archivos MP4
        ruta_ffmpeg: Ruta al ejecutable ffmpeg (opcional)
    """
    try:
        # Crear la carpeta de destino si no existe
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)
            print(f"Carpeta '{ruta_destino}' creada con éxito.")
        
        # Opciones para yt-dlp optimizadas para video MP4 de alta calidad
        opciones = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Mejor video MP4 + mejor audio
            'merge_output_format': 'mp4',  # Asegurar salida en formato MP4
            'outtmpl': os.path.join(ruta_destino, '%(title)s.%(ext)s'),  # Plantilla para nombres
            'ignoreerrors': True,         # Continuar si hay un error en un video
            'progress_hooks': [progress_hook],  # Función para mostrar el progreso
            'quiet': False,
            'verbose': False,
            'postprocessors': [{
                'key': 'FFmpegMetadata',    # Mantener los metadatos
            }],
        }
        
        # Agregar la ruta de ffmpeg si está especificada
        if ruta_ffmpeg:
            ffmpeg_dir = os.path.dirname(ruta_ffmpeg)
            opciones['ffmpeg_location'] = ffmpeg_dir
        
        # Mostrar información
        print(f"Descargando desde: {url}")
        print(f"Los archivos MP4 se guardarán en: {ruta_destino}")
        print("Configurado para descargar video en formato MP4 de alta calidad...")

        # Crear el downloader y descargar el contenido
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                # Esto es una lista de videos (playlist)
                playlist_title = info.get('title', 'Playlist Desconocida')
                total_videos = len(info['entries'])
                print(f"Título de la playlist: {playlist_title}")
                print(f"Número de videos: {total_videos}")
            else:
                # Esto es un video único
                print(f"Título del video: {info.get('title', 'Desconocido')}")
                
            # Descargar videos en MP4
            ydl.download([url])
            
            print("\n¡Descarga completada!")
            print(f"Los archivos MP4 se han guardado en: {ruta_destino}")
                
    except Exception as e:
        print(f"Error al procesar la URL: {str(e)}")

def progress_hook(d):
    """Muestra el progreso de la descarga"""
    if d['status'] == 'downloading':
        video_title = d.get('filename', '').split(os.sep)[-1].split('.')[0]
        percent = d.get('_percent_str', 'Desconocido')
        speed = d.get('_speed_str', 'Desconocido')
        eta = d.get('_eta_str', 'Desconocido')
        print(f"\rDescargando: {video_title} | {percent} | Velocidad: {speed} | Tiempo restante: {eta}", end='')
    elif d['status'] == 'finished':
        print("\n✓ Descarga completada. Procesando video...")

def mostrar_instrucciones_ffmpeg():
    """Muestra instrucciones para instalar FFmpeg"""
    print("\n" + "="*80)
    print("INSTRUCCIONES PARA INSTALAR FFMPEG:")
    print("="*80)
    print("1. Descarga FFmpeg desde: https://ffmpeg.org/download.html")
    print("   - Para Windows, descarga el build de gyan.dev: https://www.gyan.dev/ffmpeg/builds/")

if __name__ == "__main__":
    # Verificar si se tiene ffmpeg
    ffmpeg_path = buscar_ffmpeg()
    
    if not ffmpeg_path:
        print("ERROR: No se pudo encontrar FFmpeg en su sistema.")
        mostrar_instrucciones_ffmpeg()
        # Solicitar ruta manual
        ruta_manual = input("\nRuta al ejecutable ffmpeg (o deje en blanco para salir): ")
        
        if not ruta_manual.strip():
            print("Saliendo del programa...")
            sys.exit(1)
        
        if not os.path.exists(ruta_manual):
            print(f"Error: La ruta '{ruta_manual}' no existe.")
            sys.exit(1)
            
        ffmpeg_path = ruta_manual
    
    print(f"Usando FFmpeg desde: {ffmpeg_path}")
    
    # Solicitar la URL del video o playlist
    url_video = input("Introduce la URL del video o playlist de YouTube: ")
    
    # Ruta donde se guardarán los archivos MP4
    ruta_destino = r"F:\Videos MP4"
    
    # Iniciar la descarga
    descargar_videos_mp4(url_video, ruta_destino, ffmpeg_path)