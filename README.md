# Halo C.E con trucos sobre GOAT H1 (versión de prueba)

Esta rama (**`pruebas-goat`**) arma **Halo: Combat Evolved para Android** sobre **[GOAT H1 (OpenH1)](https://github.com/OpenH1/goath1)**, con el **menú de trucos**, la **flecha guía** y el **HUD** de [Halo C.E con trucos](https://github.com/freedsny/Halo-CE-Android-Trucos-Mods-OpenCE), y con todo **en español**.

GOAT H1 es otro port de Halo CE para Android, con sus propios controles táctiles, soporte de control y gráficos con Vulkan. La versión normal de Halo C.E con trucos (rama `main`) sigue sobre OpenCE; esta es otra app, en pruebas.

**Creador: freddVelp ([@freedsny](https://github.com/freedsny)).**

> Proyecto no oficial de un aficionado. No tiene relación con Microsoft, Xbox Game Studios, Halo Studios, Activision ni Bungie. Halo y Halo: Combat Evolved son marcas de Microsoft Corporation. **No incluye el juego**: necesitas tu propia copia, como pide GOAT H1.

## Qué incluye

- **La pestaña TRUCOS** dentro de los ajustes de GOAT H1, con las mismas pantallas de la versión con OpenCE:

  | Pantalla | Qué tiene |
  |---|---|
  | **TRUCOS** | Munición infinita, sin recargar, súper salto, modo dios, matar de un golpe, medusa, jetpack, poseer al chocar, sentir el daño de otros |
  | **ARMAS, LINTERNA Y MAS** | Todas las armas, todos los vehículos, un arma, un vehículo, todos los powerups, sobrescudo infinito, camuflaje, luz infinita, linterna amplia, teletransporte |
  | **MAS TRUCOS** | Forzar punto de control, sin daño por caída, no caer del vehículo, traer armas de otras misiones, tercera persona |
  | **HUD: ESTILO** | HUD moderno (viene encendido) |
  | **HUD: RADAR, ESCUDO, VIDA, MUNICION, GRANADAS** | Radar redondo, su tamaño y el barrido, y mover cada parte del HUD |
  | **GUIA** | Flecha guía: apagada, auto, objetivo de la misión, aliado o enemigo cercano |
  | **AJUSTES** | Idioma del juego, desbloquear niveles, animaciones mejoradas, bots |

- **La flecha guía** con el modo **AUTO**: va al objetivo de la misión, a los enemigos que faltan (con **QUEDAN N**) o, si tu arma se queda sin balas, a un arma cercana (flecha verde). Avisa **SUBE** o **BAJA** cuando el objetivo está en otro piso, y muestra el **OBJETIVO** de la misión en un recuadro a la izquierda un rato y luego cada tanto.
- **El editor del HUD con el dedo** dentro de los controles táctiles de GOAT H1, y el botón **Ir** del teletransporte.

Cómo funciona cada truco y cada opción está explicado en el [README principal](https://github.com/freedsny/Halo-CE-Android-Trucos-Mods-OpenCE#readme).

### Lo que cambia frente a la versión con OpenCE
- **No tiene la pantalla GRAFICOS** ni las opciones de HDR: GOAT H1 dibuja con Vulkan y trae sus propios ajustes de video.
- **No tiene ESCOGER ARMAS AL EMPEZAR** (la pantalla ARMAS al empezar una misión) todavía.
- **No busca actualizaciones** por su cuenta: las versiones nuevas salen de esta rama.

## Todo en español

Se está pasando **todo** lo que está en inglés al español, por partes. Los textos del juego van sin tildes ni eñes, porque la fuente del juego no las tiene.

| Parte | Qué traduce | Estado |
|---|---|---|
| **1. Menús y ajustes** | Los 2.640 textos de los menús de GOAT H1: campaña, multijugador, sala, amigos, video, audio, controles, red y los mensajes de la partida. ON/OFF sale como SI/NO | **Hecho** (GOAT PRUEBA #4) |
| **2. Títulos y menú principal** | Los títulos dibujados de arriba de cada pantalla y los botones del menú principal, que son imágenes | Falta |
| **3. Controles táctiles y la app** | Los botones y ventanas de los controles táctiles (Options, Edit buttons layout, Save...), los avisos de la app y los textos que quedan en el código | Falta |

Si una versión nueva de GOAT H1 agrega un texto que no está traducido, la compilación se detiene y dice cuál es, para que nada quede en inglés sin que se note.

## Cómo conseguir el APK

1. En **Releases** sale como **borrador** con el nombre **GOAT PRUEBA - GOAT H1 build-N (#n)**. Es privado: solo lo ve el dueño del repositorio.
2. La app se llama **GOAT PRUEBA** (paquete `com.openh1.openh1.trucos.pruebas`). Se instala al lado de Halo C.E y de Halo C.E Evolved sin reemplazarlas, con su propia carpeta y sus propias partidas.
3. Va firmada con la misma llave que las otras versiones, así que cada APK nuevo se instala encima del anterior sin borrar la partida.

Se compila sola cada vez que se sube un cambio a esta rama, o a mano en **Actions > Compilar GOAT H1 con trucos (PRUEBA) > Run workflow** (por defecto con la última versión de GOAT H1; también se puede escribir una, por ejemplo `build-2552`).

## Cómo está hecha esta rama

No es un fork de GOAT H1: solo guarda los cambios, y GitHub Actions los aplica al código de GOAT H1 y compila el APK.

| Archivo | Para qué sirve |
|---|---|
| `.github/workflows/build-goat.yml` | Descarga GOAT H1, aplica los trucos y el español, compila y publica el borrador |
| `trucos/trucos.patch` | Los cambios al código de GOAT H1: trucos, flecha guía, HUD, la pestaña TRUCOS y los controles táctiles |
| `trucos/regenerar_menus.py` | Genera los menús de GOAT H1 con la pestaña TRUCOS, registra sus títulos y pasa todos los menús al español, con sus controles |
| `trucos/es/menus.json` | Las traducciones de los menús: cada texto en inglés y su texto en español |
| `trucos/header_*.png` | Los títulos TRUCOS, HUD, AJUSTES y GUIA |

## Créditos y licencia

- **GOAT H1**: [OpenH1/goath1](https://github.com/OpenH1/goath1), bajo la licencia **GNU AGPL v3**. Los cambios de esta rama se comparten bajo esa misma licencia (ver [LICENSE](LICENSE)).
- **OpenCE**: [OpenCommunityEdition/OpenCE](https://github.com/OpenCommunityEdition/OpenCE), de donde vienen los trucos de la versión principal.
- Trucos, flecha guía, HUD, traducción al español y compilación automática: **freddVelp** ([@freedsny](https://github.com/freedsny)).
- Halo: Combat Evolved © Microsoft Corporation.
