import librosa
import csv

# ============================================================
# CONFIGURACION
# ============================================================

ARCHIVO = "pistas/htdemucs_6s/mi_cancion/guitar.wav"
SALIDA = "notas.csv"

# Confianza mínima de pYIN
PROB_MIN = 0.30

# Duración mínima que debe tener una nota para conservarla
MIN_DURACION = 0.08

# Pequeño hueco permitido entre frames de la misma nota
MAX_SILENCIO = 0.08


# ============================================================
# FUNCIONES
# ============================================================

def frecuencia_a_nota(frecuencia):
    """Convierte una frecuencia en Hz a nombre de nota."""

    midi = librosa.hz_to_midi(frecuencia)
    midi_redondeado = round(midi)

    return librosa.midi_to_note(
        midi_redondeado,
        octave=True,
        unicode=False
    )


# ============================================================
# CARGAR AUDIO
# ============================================================

print("Cargando:", ARCHIVO)

y, sr = librosa.load(
    ARCHIVO,
    sr=None,
    mono=True
)

duracion = len(y) / sr

print(f"Frecuencia de muestreo: {sr} Hz")
print(f"Duración: {duracion:.2f} segundos")


# ============================================================
# pYIN
# ============================================================

print()
print("Analizando frecuencia fundamental con pYIN...")

f0, voiced_flag, voiced_prob = librosa.pyin(
    y,
    fmin=librosa.note_to_hz("E2"),
    fmax=librosa.note_to_hz("E6"),
    sr=sr
)

tiempos = librosa.times_like(f0, sr=sr)


# ============================================================
# CONVERTIR FRAMES A NOTAS
# ============================================================

frames = []

for tiempo, frecuencia, probabilidad in zip(
    tiempos,
    f0,
    voiced_prob
):

    if frecuencia is None:
        frames.append(None)
        continue

    if probabilidad is None:
        frames.append(None)
        continue

    if not librosa.util.valid_audio(y):
        raise ValueError("El audio no es válido")

    if not (frecuencia > 0):
        frames.append(None)
        continue

    if probabilidad < PROB_MIN:
        frames.append(None)
        continue

    nota = frecuencia_a_nota(frecuencia)

    frames.append({
        "tiempo": tiempo,
        "nota": nota,
        "frecuencia": frecuencia,
        "probabilidad": probabilidad
    })


# ============================================================
# AGRUPAR NOTAS
# ============================================================

eventos = []

actual = None

for frame in frames:

    # --------------------------------------------------------
    # Frame sin nota
    # --------------------------------------------------------

    if frame is None:

        if actual is not None:
            actual["ultimo_frame"] = actual["ultimo_frame"]

        continue

    # --------------------------------------------------------
    # No hay evento actual
    # --------------------------------------------------------

    if actual is None:

        actual = {
            "inicio": frame["tiempo"],
            "fin": frame["tiempo"],
            "nota": frame["nota"],
            "frecuencia_suma": frame["frecuencia"],
            "confianza_suma": frame["probabilidad"],
            "cantidad": 1,
            "ultimo_frame": frame["tiempo"]
        }

        continue

    # --------------------------------------------------------
    # ¿Es la misma nota?
    # --------------------------------------------------------

    misma_nota = frame["nota"] == actual["nota"]

    diferencia = frame["tiempo"] - actual["ultimo_frame"]

    hueco_pequeno = diferencia <= MAX_SILENCIO

    if misma_nota and hueco_pequeno:

        actual["fin"] = frame["tiempo"]

        actual["frecuencia_suma"] += frame["frecuencia"]
        actual["confianza_suma"] += frame["probabilidad"]

        actual["cantidad"] += 1

        actual["ultimo_frame"] = frame["tiempo"]

    else:

        # Cerramos el evento anterior
        duracion_evento = (
            actual["fin"] - actual["inicio"]
        )

        if duracion_evento >= MIN_DURACION:

            eventos.append(actual)

        # Comenzamos uno nuevo
        actual = {
            "inicio": frame["tiempo"],
            "fin": frame["tiempo"],
            "nota": frame["nota"],
            "frecuencia_suma": frame["frecuencia"],
            "confianza_suma": frame["probabilidad"],
            "cantidad": 1,
            "ultimo_frame": frame["tiempo"]
        }


# ============================================================
# CERRAR ULTIMO EVENTO
# ============================================================

if actual is not None:

    duracion_evento = (
        actual["fin"] - actual["inicio"]
    )

    if duracion_evento >= MIN_DURACION:
        eventos.append(actual)


# ============================================================
# PREPARAR RESULTADOS
# ============================================================

resultados = []

for evento in eventos:

    frecuencia_media = (
        evento["frecuencia_suma"] /
        evento["cantidad"]
    )

    confianza_media = (
        evento["confianza_suma"] /
        evento["cantidad"]
    )

    resultados.append({
        "inicio": evento["inicio"],
        "fin": evento["fin"],
        "duracion": evento["fin"] - evento["inicio"],
        "nota": evento["nota"],
        "frecuencia": frecuencia_media,
        "confianza": confianza_media
    })


# ============================================================
# GUARDAR CSV
# ============================================================

with open(
    SALIDA,
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    escritor = csv.writer(archivo)

    escritor.writerow([
        "inicio",
        "fin",
        "duracion",
        "nota",
        "frecuencia_hz",
        "confianza"
    ])

    for resultado in resultados:

        escritor.writerow([
            f"{resultado['inicio']:.3f}",
            f"{resultado['fin']:.3f}",
            f"{resultado['duracion']:.3f}",
            resultado["nota"],
            f"{resultado['frecuencia']:.2f}",
            f"{resultado['confianza']:.3f}"
        ])


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

print()
print("=" * 70)
print("RESULTADOS")
print("=" * 70)

print(f"Eventos detectados: {len(resultados)}")
print(f"Archivo generado:   {SALIDA}")

print()
print(
    f"{'Inicio':>8} "
    f"{'Fin':>8} "
    f"{'Dur.':>7} "
    f"{'Nota':>6} "
    f"{'Hz':>9} "
    f"{'Conf.':>7}"
)

print("-" * 70)

for resultado in resultados[:100]:

    print(
        f"{resultado['inicio']:8.2f} "
        f"{resultado['fin']:8.2f} "
        f"{resultado['duracion']:7.2f} "
        f"{resultado['nota']:>6} "
        f"{resultado['frecuencia']:9.2f} "
        f"{resultado['confianza']:7.3f}"
    )

if len(resultados) > 100:
    print()
    print(f"... y {len(resultados) - 100} eventos más.")