# Carpeta `trucos/`

Aquí están los cambios que se le aplican al código oficial de [OpenCE](https://github.com/OpenCommunityEdition/OpenCE) para compilar **Halo C.E con trucos**.

| Archivo | Para qué sirve |
|---|---|
| `trucos.patch` | Los cambios al código de OpenCE: trucos, flecha guía, HUD movible, HUD moderno, radar redondo y menús |
| `regenerar_menus.py` | Genera las pantallas del menú, las registra y las pasa al español |
| `textos_es.py` | Los textos en español de los menús |
| `menu_es.py` | Dibuja en español las palabras del menú principal y los títulos |
| `header_*.png` | Los títulos TRUCOS, HUD, AJUSTES y GUIA |

El workflow `.github/workflows/build-android.yml` descarga OpenCE, aplica `trucos.patch`, ejecuta `regenerar_menus.py` y compila el APK.

**Todo lo que hace cada truco y cada opción está en el [README principal](../README.md).**
