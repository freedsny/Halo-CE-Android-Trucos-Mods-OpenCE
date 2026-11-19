# Notas para Claude: cómo arreglar la compilación de Halo C.E con trucos (OpenCE)

## Cómo funciona

- Arriba está el código de OpenCE: https://github.com/OpenCommunityEdition/OpenCE (tags `build-N`).
- `trucos/trucos.patch` se aplica sobre ese código con `patch -p1 -l` (en la carpeta del código).
- Después, en la misma carpeta, `python3 ../repo/trucos/regenerar_menus.py` genera y registra las pantallas del menú y las pasa al español (`trucos/textos_es.py`, `trucos/menu_es.py`).
- `.github/workflows/build-android.yml` compila el APK:
  - En `main` sale la versión oficial (Release "Latest", `Halo C.E con trucos - OpenCE build-N (#n)`, paquete `com.halo.decomp`).
  - En `pruebas` sale un borrador privado (`PRUEBA (pruebas) - OpenCE ...`, paquete `com.halo.decomp.pruebas`). Sin versión indicada, usa el último tag de arriba.
- `.github/workflows/vigilar-opence.yml` está programado todos los días a las 6:17 a. m. de Colombia, pero GitHub suele lanzarlo horas después (en noviembre de 2026, hacia las 2 p. m.). Si arriba hay una versión nueva, lanza `build-android.yml` en `main` con esa versión.
- Si una compilación falla, se abre el issue **"La compilacion fallo"**. Mientras esté abierto, el vigilante no lanza nada.

## Reglas

- Los arreglos van a la rama `pruebas`. **Nunca a `main`** hasta que Freed pruebe el APK de pruebas y diga "pásala".
- Los textos del juego en español van sin tildes ni eñes: las fuentes del juego no las tienen.
- Nada de datos de Bungie ni de Microsoft en el repositorio: ni mapas, ni la ISO, ni archivos del juego.
- Los secretos de firma (`ANDROID_KEYSTORE_*`) nunca se escriben, se muestran ni se guardan.
- Nunca quitar ni aflojar los controles de `regenerar_menus.py` para que algo pase.
- Un archivo del parche tiene un espacio en la ruta (`source/saved games/game_state.c`); `herramientas/rehacer_parche.py` lo escribe bien.
- Mensajes de commit en español, sin tildes, explicando qué se arregló.
- GitHub GraphQL no funciona en estas sesiones: usar `gh api` (REST).
  - `gh release download` y `gh run view` no sirven.
  - Para el log: `gh api repos/freedsny/Halo-CE-Android-Trucos-Mods-OpenCE/actions/runs/<id>/jobs` y luego `gh api repos/freedsny/Halo-CE-Android-Trucos-Mods-OpenCE/actions/jobs/<job_id>/logs`.

## Si la compilación falla

1. **Leer el log** de la ejecución que falló (el enlace está en el issue) y ver en qué paso falló:
   - **"Aplicar los trucos", en `patch`:** el parche ya no entra en la versión nueva de arriba. Ver el paso 2.
   - **"Aplicar los trucos", en `regenerar_menus.py`:** un texto en inglés cambió arriba, o un control rechazó una traducción. Ver el paso 3.
   - **Al compilar (cmake, ninja, gradle):** el código del parche ya no compila con la versión nueva. Ver el paso 2 y corregir el código.
   - **Error de red o del runner:** volver a lanzar la ejecución (`gh api -X POST .../actions/runs/<id>/rerun`) antes de tocar nada.
2. **Rehacer el parche sobre la versión nueva.** VIEJA es la versión de la última Release oficial y NUEVA la de la compilación que falló:
   ```
   git clone --depth 1 --branch build-VIEJA https://github.com/OpenCommunityEdition/OpenCE.git vieja
   cp -r vieja vieja-trucos && (cd vieja-trucos && patch -p1 -l < ../repo/trucos/trucos.patch)
   git clone --depth 1 --branch build-NUEVA https://github.com/OpenCommunityEdition/OpenCE.git nueva
   cp -r nueva nueva-trucos && (cd nueva-trucos && patch -p1 -l --merge < ../repo/trucos/trucos.patch)
   ```
   - Resolver a mano cada conflicto: los marcadores `<<<<<<<` que deja `--merge`, o los archivos `.rej`.
   - Para cada conflicto, mirar qué cambió arriba (`diff -u vieja/ARCHIVO nueva/ARCHIVO`) y qué hacía el parche (`vieja-trucos/ARCHIVO`), y llevar la misma intención al código nuevo.
   - Si arriba ya arreglaron lo mismo que un trozo del parche, quitar ese trozo.
   - Luego: `python3 repo/herramientas/rehacer_parche.py nueva nueva-trucos repo/trucos/trucos.patch`. Avisa si un archivo dejó de estar en el parche: confirmar que es a propósito.
3. **Traducciones:**
   - Si arriba cambió un menú o un texto que el parche o `regenerar_menus.py` buscan, actualizar `trucos/regenerar_menus.py`, `trucos/textos_es.py` o `trucos/menu_es.py`.
4. **Comprobar antes de subir:**
   - En una copia limpia de `nueva`, aplicar `patch -p1 -l < repo/trucos/trucos.patch` sin errores.
   - En esa misma copia, correr `python3 ../repo/trucos/regenerar_menus.py`. Necesita `pip install --break-system-packages pillow numpy scipy`. Tiene que terminar sin errores.
5. **Subir a `pruebas`** y esperar la compilación de pruebas en Actions. Si sale bien, revisar el APK del borrador:
   - Bajarlo con `gh api -H 'Accept: application/octet-stream' repos/.../releases/assets/<id>`.
   - Paquete `com.halo.decomp.pruebas`, por ejemplo con androguard.
   - Los textos en español (por ejemplo `TRUCOS`) dentro de `assets/halo_guest.elf`.
6. **Comentar en el issue** qué falló y qué se cambió. **No cerrarlo:** se cierra cuando Freed diga "pásala" y la versión oficial compile bien. Si se cierra antes, el vigilante vuelve a compilar `main` con el parche viejo y falla otra vez.
