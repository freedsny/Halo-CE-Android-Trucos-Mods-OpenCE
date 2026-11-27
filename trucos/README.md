# Carpeta `trucos/` (rama `pruebas-goat`)

Aquí están los cambios que se le aplican al código de [GOAT H1](https://github.com/OpenH1/goath1) para compilar **Halo C.E con trucos sobre GOAT H1** (GOAT PRUEBA).

| Archivo | Para qué sirve |
|---|---|
| `trucos.patch` | Los cambios al código de GOAT H1: trucos, flecha guía, HUD movible, HUD moderno, radar redondo, la pestaña TRUCOS y los controles táctiles |
| `regenerar_menus.py` | Genera los menús de GOAT H1 con la pestaña TRUCOS, registra sus títulos y pasa todos los menús al español |
| `es/menus.json` | Las traducciones de los menús de GOAT H1: cada texto en inglés y su texto en español (sin tildes ni eñes) |
| `header_*.png` | Los títulos TRUCOS, HUD, AJUSTES y GUIA |
| `textos_es.py`, `menu_es.py` | Copias de la versión con OpenCE; esta rama todavía no los usa (`menu_es.py` servirá para dibujar los títulos en español) |

El workflow `.github/workflows/build-goat.yml` descarga GOAT H1, aplica `trucos.patch`, ejecuta `regenerar_menus.py` y compila el APK.

**Qué tiene esta versión está en el [README de la rama](../README.md).**
