import csv

ARCHIVO = "notas.csv"
SALIDA = "tab_guitarra_ascii.txt"

# Afinación estándar
# MIDI de cada cuerda al aire
CUERDAS = {
    6: 40,  # E2
    5: 45,  # A2
    4: 50,  # D3
    3: 55,  # G3
    2: 59,  # B3
    1: 64,  # E4
}

NOMBRES_NOTAS = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]

NOMBRE_CUERDA = {
    1: "e",
    2: "B",
    3: "G",
    4: "D",
    5: "A",
    6: "E"
}

# Cantidad de notas por bloque visual
NOTAS_POR_BLOQUE = 16


def nota_a_midi(nota):
    """
    Convierte, por ejemplo:
        B2  -> 47
        F#3 -> 54
    """

    nombre = nota[:-1]
    octava = int(nota[-1])

    indice = NOMBRES_NOTAS.index(nombre)

    return (octava + 1) * 12 + indice


def buscar_posicion(nota):
    """
    Busca una posición posible de la nota
    en una guitarra estándar.

    Devuelve:
        (cuerda, traste)

    o None si no es posible.
    """

    midi = nota_a_midi(nota)

    posiciones = []

    for cuerda, midi_aire in CUERDAS.items():

        traste = midi - midi_aire

        if 0 <= traste <= 24:
            posiciones.append((traste, cuerda))

    if not posiciones:
        return None

    # Preferimos el menor traste.
    # Si hay empate, preferimos la cuerda más grave.
    posiciones.sort(key=lambda x: (x[0], -x[1]))

    traste, cuerda = posiciones[0]

    return cuerda, traste


# ---------------------------------------------------------
# Leer notas
# ---------------------------------------------------------

eventos = []

with open(ARCHIVO, encoding="utf-8") as archivo:

    lector = csv.DictReader(archivo)

    for fila in lector:

        nota = fila["nota"]

        posicion = buscar_posicion(nota)

        eventos.append({
            "inicio": float(fila["inicio"]),
            "fin": float(fila["fin"]),
            "nota": nota,
            "posicion": posicion
        })


# ---------------------------------------------------------
# Generar bloques de TAB
# ---------------------------------------------------------

bloques = []

for inicio in range(0, len(eventos), NOTAS_POR_BLOQUE):

    bloques.append(
        eventos[inicio:inicio + NOTAS_POR_BLOQUE]
    )


# ---------------------------------------------------------
# Generar archivo
# ---------------------------------------------------------

with open(SALIDA, "w", encoding="utf-8") as salida:

    salida.write("TAB DE GUITARRA - NOTAS DETECTADAS\n")
    salida.write("Afinacion estandar: E A D G B E\n\n")

    for numero_bloque, bloque in enumerate(bloques, start=1):

        # -------------------------------------------------
        # Preparar las seis cuerdas
        # -------------------------------------------------

        lineas = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: []
        }

        for evento in bloque:

            posicion = evento["posicion"]

            if posicion is None:

                # Nota que no entra en la guitarra estándar
                # Dejamos un espacio equivalente.
                texto = "?"

                for cuerda in range(1, 7):
                    lineas[cuerda].append(texto)

            else:

                cuerda_nota, traste = posicion

                texto = str(traste)

                # Todas las cuerdas reciben un espacio
                # equivalente al ancho de la nota.
                for cuerda in range(1, 7):

                    if cuerda == cuerda_nota:
                        lineas[cuerda].append(texto)
                    else:
                        lineas[cuerda].append("")


        # -------------------------------------------------
        # Convertir cada bloque en texto
        # -------------------------------------------------

        salida.write(
            f"--- Bloque {numero_bloque} "
            f"(notas {((numero_bloque - 1) * NOTAS_POR_BLOQUE) + 1}"
            f"-{((numero_bloque - 1) * NOTAS_POR_BLOQUE) + len(bloque)}) ---\n"
        )

        for cuerda in range(1, 7):

            texto = NOMBRE_CUERDA[cuerda] + "|"

            for i, contenido in enumerate(lineas[cuerda]):

                # Cada nota ocupa 3 caracteres:
                #
                # 2--2--4--3--2
                #
                # Para trastes de dos dígitos ampliamos
                # automáticamente.

                if contenido == "":
                    texto += "---"

                elif len(contenido) == 1:
                    texto += contenido + "--"

                else:
                    texto += contenido + "-"

            texto += "|"

            salida.write(texto + "\n")

        salida.write("\n")


print(f"TAB generado: {SALIDA}")
print(f"Notas procesadas: {len(eventos)}")