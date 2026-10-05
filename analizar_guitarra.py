import librosa
import numpy as np

ARCHIVO = "pistas/htdemucs_6s/mi_cancion/guitar.wav"

print(f"Cargando: {ARCHIVO}")

# Cargar audio
y, sr = librosa.load(ARCHIVO, sr=None, mono=True)

print(f"Frecuencia de muestreo: {sr} Hz")
print(f"Duración: {len(y) / sr:.2f} segundos")
print("Analizando notas...")

# Detección de frecuencia fundamental mediante pYIN
f0, voiced_flag, voiced_prob = librosa.pyin(
    y,
    fmin=librosa.note_to_hz("E2"),
    fmax=librosa.note_to_hz("E6"),
    sr=sr
)

# Convertimos las frecuencias a números MIDI
midi = np.full(len(f0), np.nan)

validas = ~np.isnan(f0)

midi[validas] = librosa.hz_to_midi(f0[validas])

# Redondeamos al semitono más cercano
notas_midi = np.full(len(midi), np.nan)
notas_midi[validas] = np.round(midi[validas])

# Convertimos MIDI a nombre de nota
nombres = []

for nota in notas_midi:
    if np.isnan(nota):
        nombres.append(None)
    else:
        nombres.append(librosa.midi_to_note(nota))

# Tiempo de cada frame
tiempos = librosa.times_like(f0, sr=sr)

# Mostrar algunas detecciones
print()
print("===== ESTADÍSTICAS DEL DETECTOR =====")

validas_f0 = ~np.isnan(f0)

print(f"Frames totales:              {len(f0)}")
print(f"Frames con frecuencia:       {np.sum(validas_f0)}")
print(f"Frames sin frecuencia:       {np.sum(~validas_f0)}")

if np.any(validas_f0):
    print(f"Frecuencia mínima:            {np.nanmin(f0):.2f} Hz")
    print(f"Frecuencia máxima:            {np.nanmax(f0):.2f} Hz")

validas_prob = ~np.isnan(voiced_prob)

if np.any(validas_prob):
    print(f"Probabilidad máxima:          {np.nanmax(voiced_prob):.3f}")
    print(f"Probabilidad media:           {np.nanmean(voiced_prob):.3f}")

    for umbral in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
        cantidad = np.sum(voiced_prob >= umbral)
        print(
            f"Frames con prob >= {umbral:.1f}: "
            f"{cantidad}"
        )

print("====================================")
print("Primeras detecciones:")
print("--------------------------------")

ultima_nota = None
inicio = None

for tiempo, nota, prob in zip(tiempos, nombres, voiced_prob):

    # Ignoramos segmentos con poca confianza
    if nota is None or prob < 0.30:
        nota = None

    if nota != ultima_nota:

        if ultima_nota is not None:
            print(
                f"{inicio:7.2f}s - {tiempo:7.2f}s   "
                f"{ultima_nota}"
            )

        if nota is not None:
            inicio = tiempo

        ultima_nota = nota

# Última nota
if ultima_nota is not None:
    print(
        f"{inicio:7.2f}s - {tiempos[-1]:7.2f}s   "
        f"{ultima_nota}"
    )

print("--------------------------------")
print("Análisis terminado.")