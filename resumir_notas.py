import csv


ARCHIVO = "notas.csv"


# ============================================================
# CARGAR NOTAS
# ============================================================

with open(ARCHIVO, encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    notas = list(lector)


# Convertir valores numéricos

for n in notas:
    n["inicio"] = float(n["inicio"])
    n["fin"] = float(n["fin"])
    n["duracion"] = float(n["duracion"])
    n["frecuencia"] = float(n["frecuencia_hz"])
    n["confianza"] = float(n["confianza"])


# ============================================================
# MOSTRAR TODAS LAS NOTAS
# ============================================================

print()
print("=" * 80)
print("SECUENCIA DE NOTAS")
print("=" * 80)

for i, n in enumerate(notas, 1):

    print(
        f"{i:3d}  "
        f"{n['inicio']:7.2f} - "
        f"{n['fin']:7.2f}   "
        f"{n['nota']:>4}   "
        f"{n['frecuencia']:7.2f} Hz   "
        f"conf={n['confianza']:.3f}"
    )


# ============================================================
# SOLO NOTAS
# ============================================================

print()
print("=" * 80)
print("SECUENCIA MUSICAL")
print("=" * 80)

for n in notas:
    print(n["nota"], end=" → ")

print("FIN")


# ============================================================
# AGRUPAR POR BLOQUES DE TIEMPO
# ============================================================

BLOQUE = 20.0

print()
print("=" * 80)
print("SECUENCIA POR BLOQUES DE 20 SEGUNDOS")
print("=" * 80)

bloque_actual = -1

for n in notas:

    bloque = int(n["inicio"] // BLOQUE)

    if bloque != bloque_actual:

        bloque_actual = bloque

        inicio_bloque = bloque * BLOQUE
        fin_bloque = inicio_bloque + BLOQUE

        print()
        print(
            f"[ {inicio_bloque:6.1f} - "
            f"{fin_bloque:6.1f} segundos ]"
        )

        print("-" * 50)

    print(
        f"{n['inicio']:7.2f}  "
        f"{n['nota']:>4}  "
        f"{n['duracion']:5.2f}s"
    )


# ============================================================
# CONTAR NOTAS
# ============================================================

conteo = {}

for n in notas:

    nota = n["nota"]

    if nota not in conteo:
        conteo[nota] = 0

    conteo[nota] += 1


print()
print("=" * 80)
print("NOTAS MÁS FRECUENTES")
print("=" * 80)

ordenadas = sorted(
    conteo.items(),
    key=lambda x: x[1],
    reverse=True
)

for nota, cantidad in ordenadas:

    print(
        f"{nota:>4} : "
        f"{cantidad:3d} veces"
    )


# ============================================================
# INTERVALOS ENTRE NOTAS
# ============================================================

print()
print("=" * 80)
print("INTERVALOS ENTRE NOTAS")
print("=" * 80)

for anterior, actual in zip(notas, notas[1:]):

    intervalo = actual["inicio"] - anterior["inicio"]

    print(
        f"{anterior['nota']:>4} → "
        f"{actual['nota']:>4}   "
        f"{intervalo:6.2f}s"
    )