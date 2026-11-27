"""Halo C.E con trucos sobre GOAT H1: genera los menus de ajustes de GOAT H1 con la
pestana TRUCOS (tools/port_settings.py ya la trae, de trucos.patch), registra sus
paginas nuevas y sus titulos, y pone las palabras de guide.mode en port_config.c.
Se ejecuta desde la raiz del codigo de GOAT H1, despues de aplicar trucos.patch.

Si algo que busca no esta (GOAT H1 cambio), se detiene con un error: mejor una
compilacion que falla que un menu roto."""
import json
import pathlib
import shutil
import subprocess
import sys

aqui = pathlib.Path(__file__).resolve().parent
menus = pathlib.Path("port/assets/menus")
ce = menus / "ce"

sys.path.insert(0, "tools")
import port_settings as ps  # noqa: E402

pe = ps.PE


def falla(texto):
    sys.exit("ERROR (trucos): " + texto)


# 1) las paginas de TRUCOS, las de la version de OpenCE
paginas = [carpeta for carpeta in ps.PAGES if carpeta == "network_setup/cheats" or
           carpeta in getattr(ps, "TRUCOS_PAGES", {})]
if "network_setup/cheats" not in ps.PAGES or len(paginas) < 2:
    falla("tools/port_settings.py no trae la pestana TRUCOS (trucos.patch)")
if ps.PAGES["network_setup/cheats"].get("tab") != "TRUCOS":
    falla("la pagina network_setup/cheats no es la pestana TRUCOS")

# 2) los menus de ajustes, con la herramienta de GOAT H1 (escribe port/assets/menus/ce
# y model; los de antes los deja igual, salvo la barra de pestanas, que ahora tiene una mas)
antes = {str(p.relative_to(menus)) for p in menus.rglob("*") if p.is_file()}
subprocess.run([sys.executable, "tools/port_settings.py"], check=True)
nuevos = sorted(str(p.relative_to(menus)) for p in menus.rglob("*") if p.is_file()
                and str(p.relative_to(menus)) not in antes)
for nombre in nuevos:
    if "network_setup.cheats" not in nombre:
        falla("la herramienta de menus escribio un archivo que no es de TRUCOS: " + nombre)
for carpeta in paginas:
    archivo = "ce/" + f"{pe}/{carpeta}".replace("/", ".") + ".xml"
    if not (menus / archivo).exists():
        falla("no se escribio la pagina " + archivo)

# 3) los titulos (TRUCOS, HUD, AJUSTES, GUIA): los dibujos de trucos/, uno por pagina,
# donde GOAT H1 busca el de cada pagina (header_<pantalla>)
dibujos = {"TRUCOS": "header_trucos.png", "HUD": "header_hud.png", "AJUSTES": "header_ajustes.png",
           "GUIA": "header_guia.png"}
bitmaps_xml = ce / "bitmaps.xml"
texto = bitmaps_xml.read_text(encoding="utf-8")
if "</menus>" not in texto:
    falla("no se encontro el final de ce/bitmaps.xml")
pngs = []
for carpeta in paginas:
    pagina = ps.PAGES[carpeta]
    if "title" not in pagina:
        continue
    pantalla = pagina["screen"][:-len("_screen")]
    nombre = f"{pe}/{carpeta}/header_{pantalla}"
    png = f"ce/port/{pe}/{carpeta}/header_{pantalla}.png"
    destino = menus / png
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(aqui / dibujos[pagina["title"]], destino)
    pngs.append(png)
    if f'name="{nombre}"' not in texto:
        entrada = (f'\t<bitmap name="{nombre}">\n'
                   f'\t\t<frame png="{png}" width="512" height="64"/>\n'
                   f'\t</bitmap>\n')
        fin = texto.rindex("</menus>")
        texto = texto[:fin] + entrada + texto[fin:]
bitmaps_xml.write_text(texto, encoding="utf-8", newline="")

# 4) menus.json: cada archivo nuevo despues del que mas se le parece (la lista va por grupos)
mj = menus / "menus.json"
crudo = mj.read_text(encoding="utf-8")
datos = json.loads(crudo)
archivos = datos["files"]


def parecido(a, b):
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    return n


for nombre in nuevos + pngs:
    if nombre in archivos:
        continue
    mejor = max(range(len(archivos)), key=lambda i: (parecido(archivos[i], nombre), i))
    archivos.insert(mejor + 1, nombre)
mj.write_text(json.dumps(datos, indent=1, ensure_ascii=False) + ("\n" if crudo.endswith("\n") else ""),
              encoding="utf-8")

# 5) las palabras de guide.mode (TRUCOS, GUIA) en la lista de port_config.c, como en OpenCE
config_c = pathlib.Path("port/linux/src/port_config.c")
fuente_c = config_c.read_text(encoding="utf-8")
palabras = '\t{ "guide.mode", { "off", "auto", "objective", "ally", "enemy", NULL }, NULL },\n'
if '"guide.mode", {' not in fuente_c:
    punto = "config_words[] =\n{\n"
    i = fuente_c.find(punto)
    if i == -1:
        falla("no se encontro la lista config_words de port_config.c")
    i += len(punto)
    config_c.write_text(fuente_c[:i] + palabras + fuente_c[i:], encoding="utf-8", newline="")


# 6) todo en espanol: cada texto que se ve en los menus (de GOAT H1 y del juego), con
# trucos/es/menus.json (ingles -> espanol, sin tildes ni enes: la fuente del juego).
# Si un texto que se ve no esta traducido (GOAT H1 agrego uno), se detiene y lo dice
import html
import re

traducciones = json.loads((aqui / "es" / "menus.json").read_text(encoding="utf-8"))
ya_espanol = set(traducciones.values())
ENTEROS = ("text", "help", "title", "label")      # un texto entero
LISTAS = ("strings", "items", "shown")            # palabras separadas por |
RUTAS = ("crumb",)                                 # partes separadas por " › "
TILDES = re.compile(r"[áéíóúÁÉÍÓÚñÑ¿¡]")
sin_traducir = {}


def traducir_texto(texto, archivo):
    if texto in traducciones:
        return traducciones[texto]
    if texto in ya_espanol or not re.search(r"[A-Za-z]", html.unescape(texto)):
        return texto
    sin_traducir.setdefault(texto, archivo)
    return texto


def traducir_atributo(m, archivo):
    nombre, valor = m.group(1), m.group(2)
    if nombre in ENTEROS:
        nuevo = traducir_texto(valor, archivo)
    elif nombre in LISTAS:
        nuevo = "|".join(traducir_texto(v, archivo) for v in valor.split("|"))
    else:
        nuevo = " › ".join(traducir_texto(v, archivo) for v in valor.split(" › "))
    return f' {nombre}="{nuevo}"'


patron = re.compile(r' (' + "|".join(ENTEROS + LISTAS + RUTAS) + r')="([^"]*)"')
cambiados = 0
for ruta in sorted(list(ce.glob("*.xml")) + list((menus / "model").rglob("*.xml"))):
    if ruta.name == "bitmaps.xml":
        continue
    contenido = ruta.read_text(encoding="utf-8")
    nuevo = patron.sub(lambda m: traducir_atributo(m, ruta.name), contenido)
    if nuevo != contenido:
        ruta.write_text(nuevo, encoding="utf-8", newline="")
        cambiados += 1
malos = [t for t in traducciones.values() if TILDES.search(t)]
if malos:
    falla("traducciones con tildes o enes (la fuente del juego no las tiene): " + "; ".join(malos[:5]))
if sin_traducir:
    falla(f"{len(sin_traducir)} textos de los menus sin traducir (agregarlos a trucos/es/menus.json): " +
          "; ".join(f"{t!r} ({a})" for t, a in list(sin_traducir.items())[:15]))
print("menus en espanol:", cambiados, "archivos")

print("TRUCOS en GOAT H1:", len(paginas), "paginas,", len(nuevos), "archivos de menu nuevos,", len(pngs), "titulos")
