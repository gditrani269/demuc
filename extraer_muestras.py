import csv
import subprocess
import os

ARCHIVO_AUDIO = "pistas/htdemucs_6s/mi_cancion/guitar.wav"
ARCHIVO_CSV = "notas.csv"
DIRECTORIO = "muestras"

# Eventos que queremos escuchar
TIEMPOS = [
    22.93,
    35.67,
    74.32,
    106.79,
    129.44,
    214.87,
]

# Tiempo extra alrededor de la nota
PADDING = 0.5


# ------------------------------------------------------------
# Crear directorio
# ------------------------------------------------------------

os.makedirs(DIRECTORIO, exist_ok=True)


# ------------------------------------------------------------
# Leer notas.csv
# ------------------------------------------------------------

with open(ARCHIVO_CSV, encoding="utf-8") as archivo:
    notas = list(csv.DictReader(archivo))


# ------------------------------------------------------------
# Extraer muestras
# ------------------------------------------------------------

for tiempo_buscado in TIEMPOS:

    # Buscar la detección más cercana
    evento = min(
        notas,
        key=lambda x: abs(
            float(x["inicio"]) - tiempo_buscado
        )
    )

    inicio = float(evento["inicio"])
    fin = float(evento["fin"])
    nota = evento["nota"]

    # Agregar contexto
    inicio_audio = max(0, inicio - PADDING)
    fin_audio = fin + PADDING

    duracion = fin_audio - inicio_audio

    # Nombre seguro para el archivo
    nota_archivo = nota.replace("#", "s")

    salida = (
        f"{DIRECTORIO}/"
        f"{inicio:.2f}_{nota_archivo}.wav"
    )

    print()
    print(f"Nota detectada: {nota}")
    print(f"Tiempo:         {inicio:.2f} - {fin:.2f}")
    print(f"Confianza:      {evento['confianza']}")
    print(f"Generando:      {salida}")

    subprocess.run([
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-ss", str(inicio_audio),
        "-i", ARCHIVO_AUDIO,
        "-t", str(duracion),
        "-c:a", "pcm_s16le",
        salida
    ], check=True)


print()
print("=" * 60)
print("MUESTRAS GENERADAS")
print("=" * 60)

for archivo in sorted(os.listdir(DIRECTORIO)):
    if archivo.endswith(".wav"):
        print(f"  {DIRECTORIO}/{archivo}")