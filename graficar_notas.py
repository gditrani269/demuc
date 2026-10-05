import csv
import matplotlib.pyplot as plt


ARCHIVO = "notas.csv"


# ============================================================
# CARGAR CSV
# ============================================================

tiempos = []
frecuencias = []
notas = []
confianzas = []

with open(ARCHIVO, encoding="utf-8") as archivo:

    lector = csv.DictReader(archivo)

    for fila in lector:

        tiempos.append(float(fila["inicio"]))
        frecuencias.append(float(fila["frecuencia_hz"]))
        notas.append(fila["nota"])
        confianzas.append(float(fila["confianza"]))


# ============================================================
# GRAFICO
# ============================================================

plt.figure(figsize=(16, 7))

plt.scatter(
    tiempos,
    frecuencias,
    s=50,
    alpha=0.8
)

# Etiqueta de cada nota
for tiempo, frecuencia, nota in zip(
    tiempos,
    frecuencias,
    notas
):

    plt.annotate(
        nota,
        (tiempo, frecuencia),
        xytext=(0, 7),
        textcoords="offset points",
        ha="center",
        fontsize=8
    )


plt.xlabel("Tiempo (segundos)")
plt.ylabel("Frecuencia (Hz)")

plt.title(
    "Notas de guitarra detectadas por pYIN"
)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "notas_guitarra.png",
    dpi=150
)

print("Gráfico generado: notas_guitarra.png")