import os
import hashlib

def obtener_hash_archivo(archivo):
    """Genera un hash MD5 del archivo para compararlo."""
    hash_md5 = hashlib.md5()
    with open(archivo, 'rb') as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloque)
    return hash_md5.hexdigest()

def obtener_archivos_mp3(ruta):
    """Obtiene todos los archivos .mp3 en la carpeta especificada."""
    archivos_mp3 = []
    for root, dirs, files in os.walk(ruta):
        for file in files:
            if file.lower().endswith(".mp3"):
                archivos_mp3.append(os.path.join(root, file))
    return archivos_mp3

def listar_archivos_duplicados(ruta):
    """Lista los archivos mp3 duplicados en la carpeta sin eliminarlos."""
    archivos_mp3 = obtener_archivos_mp3(ruta)
    hashes = {}
    archivos_duplicados = []

    for archivo in archivos_mp3:
        archivo_hash = obtener_hash_archivo(archivo)
        if archivo_hash in hashes:
            archivos_duplicados.append(archivo)
        else:
            hashes[archivo_hash] = archivo
    
    # Mostrar los archivos duplicados
    if archivos_duplicados:
        print("Archivos duplicados encontrados:")
        for archivo in archivos_duplicados:
            print(archivo)
    else:
        print("No se encontraron archivos duplicados.")

# Ruta de la carpeta donde están los archivos MP3
ruta_carpeta = r"F:\Music MP3"  # Reemplaza con la ruta de tu carpeta

listar_archivos_duplicados(ruta_carpeta)
