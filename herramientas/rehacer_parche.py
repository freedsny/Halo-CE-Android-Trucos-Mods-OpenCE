"""Rehace el archivo del parche a partir de dos copias del codigo de arriba.

BASE es la version de arriba tal cual (por ejemplo, el tag build-144) y TRABAJO
es esa misma version con el parche aplicado y arreglado a mano. Escribe en
SALIDA un diff unificado de cada archivo cambiado, nuevo o borrado, en el mismo
formato que lee la compilacion (patch -p1 -l).

Uso: python3 herramientas/rehacer_parche.py BASE TRABAJO SALIDA
"""
import filecmp
import os
import subprocess
import sys

# Lo que no es codigo: el historial de git, lo que dejan patch y Python, y lo
# que deja una compilacion hecha en la copia
CARPETAS_IGNORADAS = {".git", "__pycache__", "build", ".ccache"}
SUFIJOS_IGNORADOS = (".orig", ".rej", ".pyc")
NOMBRES_IGNORADOS = {"build.ninja", "compile_commands.json"}


def archivos(raiz):
    """Las rutas relativas de los archivos de `raiz`, sin los ignorados."""
    encontrados = set()
    for carpeta, subcarpetas, nombres in os.walk(raiz):
        subcarpetas[:] = [s for s in subcarpetas if s not in CARPETAS_IGNORADAS]
        for nombre in nombres:
            if nombre.endswith(SUFIJOS_IGNORADOS) or nombre in NOMBRES_IGNORADOS or nombre.startswith(".ninja_"):
                continue
            encontrados.add(os.path.relpath(os.path.join(carpeta, nombre), raiz))
    return encontrados


def diff_de(base, trabajo, ruta):
    """El diff unificado de `ruta`; /dev/null del lado que no la tiene."""
    antes = os.path.join(base, ruta)
    despues = os.path.join(trabajo, ruta)
    # (un nombre con espacios: un tabulador despues, donde patch termina el nombre)
    tab = "\t" if " " in ruta else ""
    etiqueta_antes = "a/" + ruta + tab if os.path.exists(antes) else "/dev/null"
    etiqueta_despues = "b/" + ruta + tab if os.path.exists(despues) else "/dev/null"
    resultado = subprocess.run(
        ["diff", "-u", "--label", etiqueta_antes, "--label", etiqueta_despues,
         antes if os.path.exists(antes) else "/dev/null",
         despues if os.path.exists(despues) else "/dev/null"],
        capture_output=True, text=True, errors="surrogateescape")
    if resultado.returncode > 1 or resultado.stdout.startswith("Binary files"):
        sys.exit(f"ERROR: {ruta} no se puede poner en el parche (binario o ilegible)")
    return resultado.stdout.rstrip("\n")


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    base, trabajo, salida = sys.argv[1:]
    en_base, en_trabajo = archivos(base), archivos(trabajo)
    cambiados = sorted(
        ruta for ruta in en_base | en_trabajo
        if ruta not in en_base or ruta not in en_trabajo
        or not filecmp.cmp(os.path.join(base, ruta), os.path.join(trabajo, ruta), shallow=False))
    # (lo que el parche anterior cambiaba y este ya no: puede ser a proposito,
    # porque arriba ya lo arreglaron, o un archivo que se quedo sin copiar)
    if os.path.exists(salida):
        with open(salida, encoding="utf-8", errors="surrogateescape") as archivo:
            anteriores = {linea[6:].rstrip("\n").rstrip("\t") for linea in archivo if linea.startswith("+++ b/")}
        for ruta in sorted(anteriores - set(cambiados)):
            print(f"AVISO: ya no esta en el parche: {ruta}")
    with open(salida, "w", encoding="utf-8", errors="surrogateescape") as archivo:
        archivo.write("\n".join(diff_de(base, trabajo, ruta) for ruta in cambiados) + "\n")
    for ruta in cambiados:
        estado = "nuevo" if ruta not in en_base else "borrado" if ruta not in en_trabajo else "cambiado"
        print(f"{estado}: {ruta}")
    print(f"{len(cambiados)} archivos en {salida}")


if __name__ == "__main__":
    main()
