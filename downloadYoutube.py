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

def descargar_playlist_mp3(url_playlist, ruta_destino, ruta_ffmpeg=None):
    """
    Descarga todos los videos de una playlist de YouTube y los convierte a formato MP3.
    
    Args:
        url_playlist: URL de la playlist de YouTube
        ruta_destino: Ruta donde se guardarán los archivos MP3
        ruta_ffmpeg: Ruta al ejecutable ffmpeg (opcional)
    """
    try:
        # Crear la carpeta de destino si no existe
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)
            print(f"Carpeta '{ruta_destino}' creada con éxito.")
        
        # Opciones para yt-dlp optimizadas para extracción de audio en MP3
        opciones = {
            'format': 'bestaudio/best',  # Seleccionar la mejor calidad de audio disponible
            'extract_audio': True,        # Extraer solo el audio
            'audio_format': 'mp3',        # Convertir a formato mp3
            'audio_quality': '0',         # Mejor calidad (0 es la mejor, 9 es la peor)
            'outtmpl': os.path.join(ruta_destino, '%(title)s.%(ext)s'),  # Plantilla para nombres
            'ignoreerrors': True,         # Continuar si hay un error en un video
            'progress_hooks': [progress_hook],  # Función para mostrar el progreso
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Calidad en kbps
            }, {
                'key': 'FFmpegMetadata',    # Mantener los metadatos
            }],
            'quiet': False,
            'verbose': False,
        }
        
        # Agregar la ruta de ffmpeg si está especificada
        if ruta_ffmpeg:
            ffmpeg_dir = os.path.dirname(ruta_ffmpeg)
            opciones['ffmpeg_location'] = ffmpeg_dir
        
        # Mostrar información
        print(f"Descargando playlist: {url_playlist}")
        print(f"Los archivos MP3 se guardarán en: {ruta_destino}")
        print("Configurado para extraer audio en formato MP3 de alta calidad...")
        
        # Crear el downloader y descargar la playlist
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url_playlist, download=False)
            if 'entries' in info:
                playlist_title = info.get('title', 'Playlist Desconocida')
                total_videos = len(info['entries'])
                print(f"Título de la playlist: {playlist_title}")
                print(f"Número de pistas: {total_videos}")
                
                # Descargar y convertir a MP3
                ydl.download([url_playlist])
                
                print("\n¡Descarga y conversión a MP3 completada!")
                print(f"Los archivos MP3 se han guardado en: {ruta_destino}")
            else:
                print("No se pudo obtener información de la playlist.")
                
    except Exception as e:
        print(f"Error al procesar la playlist: {str(e)}")

def progress_hook(d):
    """Muestra el progreso de la descarga"""
    if d['status'] == 'downloading':
        video_title = d.get('filename', '').split(os.sep)[-1].split('.')[0]
        percent = d.get('_percent_str', 'Desconocido')
        speed = d.get('_speed_str', 'Desconocido')
        eta = d.get('_eta_str', 'Desconocido')
        print(f"\rDescargando: {video_title} | {percent} | Velocidad: {speed} | Tiempo restante: {eta}", end='')
    elif d['status'] == 'finished':
        print("\n✓ Descarga completada. Convirtiendo a MP3...")

def mostrar_instrucciones_ffmpeg():
    """Muestra instrucciones para instalar FFmpeg"""
    print("\n" + "="*80)
    print("INSTRUCCIONES PARA INSTALAR FFMPEG:")
    print("="*80)
    print("1. Descarga FFmpeg desde: https://ffmpeg.org/download.html")
    print("   - Para Windows, descarga el build de gyan.dev: https://www.gyan.dev/ffmpeg/builds/")
    print("   - Descarga la versión 'release essentials'")
    print("\n2. Extrae el archivo descargado")
    print("\n3. Mueve la carpeta 'ffmpeg' a una ubicación como 'C:\\ffmpeg'")
    print("\n4. Agrega la ruta 'C:\\ffmpeg\\bin' a las variables de entorno PATH:")
    print("   - Busca 'variables de entorno' en el menú de inicio")
    print("   - Haz clic en 'Variables de entorno...'")
    print("   - En 'Variables del sistema', selecciona 'Path' y haz clic en 'Editar'")
    print("   - Haz clic en 'Nuevo' y agrega 'C:\\ffmpeg\\bin'")
    print("   - Haz clic en 'Aceptar' en todas las ventanas")
    print("\n5. Reinicia cualquier ventana de comandos abierta")
    print("="*80)

if __name__ == "__main__":
    # Verificar si se tiene ffmpeg
    ffmpeg_path = buscar_ffmpeg()
    
    if not ffmpeg_path:
        print("ERROR: No se pudo encontrar FFmpeg en su sistema.")
        mostrar_instrucciones_ffmpeg()
        
        # Solicitar ruta manual
        print("\nPor favor, instale FFmpeg usando las instrucciones anteriores")
        print("o proporcione la ruta completa al ejecutable ffmpeg.")
        ruta_manual = input("\nRuta al ejecutable ffmpeg (o deje en blanco para salir): ")
        
        if not ruta_manual.strip():
            print("Saliendo del programa...")
            sys.exit(1)
        
        if not os.path.exists(ruta_manual):
            print(f"Error: La ruta '{ruta_manual}' no existe.")
            sys.exit(1)
            
        ffmpeg_path = ruta_manual
    
    print(f"Usando FFmpeg desde: {ffmpeg_path}")
    
    # Solicitar la URL de la playlist
    url_playlist = input("Introduce la URL de la playlist de YouTube: ")
    
    # Ruta donde se guardarán los archivos MP3
    ruta_destino = r"F:\Music"
    
    # Iniciar la descarga
    descargar_playlist_mp3(url_playlist, ruta_destino, ffmpeg_path)