# TaxiTech Solutions — Prototipo Taxímetro Software
## Backlog Criterios de Aceptación, Setup y Sub-issues
Link al repositorio: https://github.com/IA-P1-BCN/proyecto-1-ivanna-caraccio
Link a las issues: https://github.com/IA-P1-BCN/proyecto-1-ivanna-caraccio/issues
Link al proyecto: https://github.com/orgs/IA-P1-BCN/projects/13

---

## 🚀 TK-00 — Base structure

**Descripción:** Como equipo de desarrollo, necesitamos crear el repositorio Git y el esqueleto del proyecto en Python siguiendo la arquitectura modular definida (`domain/`, `application/`, `infrastructure/`, `interfaces/`), para poder empezar a implementar las historias de usuario sobre una base ordenada, versionada y configurada desde el primer commit.

**Criterios de aceptación:**
- Se crea el repositorio Git (remoto e inicializado localmente) con un `.gitignore` adecuado para Python (venv, `__pycache__`, logs, etc.).
- Se crea la estructura de carpetas exacta requerida:
  ```
  proyecto-1-ivanna-caraccio/
  ├── doc/
  ├── src/
  │   ├── domain/
  │   ├── application/
  │   └── infrastructure/
  |   └── interfaces/
  ├── config/
  ├── logs/
  └── tests/
  ```
- Se inicializa un entorno virtual de Python (venv) y un fichero `requirements.txt` (o `pyproject.toml`) para gestionar dependencias.
- Se crea un fichero `README.md` inicial con descripción del proyecto, cómo instalarlo y cómo ejecutarlo.
- Se configura el proyecto en Visual Studio Code: `.vscode/settings.json` con el intérprete de Python del entorno virtual, y recomendaciones de extensiones (`.vscode/extensions.json`).
- Se añade configuración base de calidad de código (linter tipo `flake8`/`ruff` y formateador tipo `black`), coherente con los principios SOLID/DRY exigidos.
- Se crea un fichero de configuración inicial en `taximeter/config` con las tarifas vigentes (0.02 €/s parado, 0.05 €/s en movimiento) como placeholder para US-07.
- Se deja preparada la carpeta `tests/` con un test dummy que se ejecute correctamente (para validar que el framework de testing, p. ej. `pytest`, está operativo).
- El commit inicial ("scaffolding") queda subido al repositorio remoto y es accesible por todo el equipo.

---

## US-01 — Iniciar carrera con un solo comando (Must)

**Historia:** Como taxista, quiero iniciar una carrera con un solo comando para empezar a cobrar desde el momento de arranque.

**Criterios de aceptación:**
- Al ejecutar el comando/acción de inicio, el sistema crea una nueva carrera con timestamp de inicio y estado inicial "parado".
- Desde el momento de inicio, el sistema empieza a acumular importe según la tarifa vigente para el estado "parado" (0.02 €/segundo).
- Si ya hay una carrera activa, el sistema impide iniciar una nueva y muestra un mensaje informativo.
- El importe acumulado se muestra en tiempo real (o con refresco periódico) desde el instante de inicio.

### Sub-issues

- **US-01.1 — Crear entidad de dominio `Carrera`**
  Modelar en `domain/` la clase `Carrera` con sus atributos esenciales (estado actual, timestamp de inicio, lista de tramos de tarifa). Es la base sobre la que se apoyan el resto de casos de uso relacionados con el ciclo de vida de una carrera.

- **US-01.2 — Implementar caso de uso `IniciarCarrera`**
  Crear en `application/` la clase/función que orquesta la creación de una nueva `Carrera`, delegando en el dominio la inicialización del estado y coordinando con la capa de infraestructura si hace falta persistencia o logging.

- **US-01.3 — Implementar comando/acción de arranque en `interfaces/`**
  Exponer al taxista el punto de entrada (comando CLI o botón, según se decida el canal) que invoca el caso de uso `IniciarCarrera`, manteniendo la interfaz desacoplada de la lógica de negocio.

- **US-01.4 — Validar que no exista carrera activa antes de iniciar**
  Añadir la comprobación de que no puede arrancarse una carrera si ya hay una en curso, devolviendo un mensaje claro al usuario en ese caso, evitando estados inconsistentes.

- **US-01.5 — Implementar acumulador de importe en tiempo real**
  Desarrollar el mecanismo (temporizador, hilo o cálculo bajo demanda basado en timestamps) que permite mostrar el importe acumulado mientras la carrera está en curso, sin bloquear el resto de la aplicación.

- **US-01.6 — Tests unitarios de inicio de carrera**
  Cubrir con `pytest` los casos: creación correcta de la carrera, estado inicial "parado" y aplicación de la tarifa correspondiente desde el segundo 0.

---

## US-02 — Cambiar estado entre "parado" y "en movimiento" (Must)

**Historia:** Como taxista, quiero cambiar el estado entre "parado" y "en movimiento" para que la tarifa se ajuste.

**Criterios de aceptación:**
- El taxista puede alternar el estado de la carrera activa entre "parado" y "en movimiento" mediante un comando/acción.
- Al cambiar a "en movimiento", el sistema aplica la tarifa de 0.05 €/segundo a partir de ese instante.
- Al cambiar a "parado", el sistema aplica la tarifa de 0.02 €/segundo a partir de ese instante.
- El cambio de estado no reinicia el importe ya acumulado; el cálculo es acumulativo por tramos.
- No se puede cambiar de estado si no hay una carrera activa.

### Sub-issues

- **US-02.1 — Añadir lógica de cambio de estado en la entidad `Carrera`**
  Extender el dominio con el método que cambia el estado de la carrera, validando internamente que exista una carrera activa antes de aplicar el cambio.

- **US-02.2 — Implementar caso de uso `CambiarEstadoCarrera`**
  Crear en `application/` el caso de uso que recibe la petición de cambio de estado desde la interfaz y la traslada al dominio, gestionando posibles errores de negocio.

- **US-02.3 — Implementar cálculo de importe por tramos**
  Guardar el timestamp de cada cambio de estado junto con la tarifa vigente en ese tramo, de forma que el importe total se calcule sumando correctamente cada segmento "parado"/"en movimiento".

- **US-02.4 — Exponer comando/acción de cambio de estado en `interfaces/`**
  Añadir el punto de entrada que el taxista usa para alternar el estado (botón o comando), conectado al caso de uso `CambiarEstadoCarrera`.

- **US-02.5 — Tests unitarios de cambio de estado y cálculo acumulado**
  Verificar con pruebas automatizadas secuencias tipo parado→movimiento→parado y que el importe acumulado por tramos es correcto.

- **US-02.6 — Test de error: cambio de estado sin carrera activa**
  Comprobar que el sistema rechaza correctamente un intento de cambio de estado cuando no existe ninguna carrera en curso.

---

## US-03 — Finalizar carrera y ver el total (Must)

**Historia:** Como taxista, quiero finalizar la carrera y ver el total en euros para cobrar al pasajero.

**Criterios de aceptación:**
- Al finalizar la carrera, el sistema deja de acumular importe y calcula el total final en euros.
- El total se muestra con 2 decimales y en formato moneda (€).
- El sistema registra la hora de fin y la duración total de la carrera.
- No se puede finalizar una carrera si no hay ninguna activa.
- Tras finalizar, la carrera queda guardada como parte del histórico del día (dependencia con US-05).

### Sub-issues

- **US-03.1 — Implementar caso de uso `FinalizarCarrera`**
  Desarrollar en `application/` la lógica que cierra el último tramo de tarifa activo y calcula el importe total sumando todos los tramos de la carrera.

- **US-03.2 — Implementar formateo de importe**
  Crear una utilidad de formateo que presente el total siempre con 2 decimales y el símbolo €, reutilizable en cualquier punto de la aplicación que muestre importes (DRY).

- **US-03.3 — Registrar hora de fin y duración total en `Carrera`**
  Ampliar la entidad de dominio para almacenar el timestamp de fin y calcular la duración total de la carrera una vez finalizada.

- **US-03.4 — Exponer comando/acción de finalización en `interfaces/`**
  Añadir el punto de entrada que permite al taxista finalizar la carrera y visualizar el total resultante.

- **US-03.5 — Validar que exista carrera activa antes de finalizar**
  Impedir la finalización si no hay ninguna carrera en curso, devolviendo un mensaje informativo al usuario.

- **US-03.6 — Tests unitarios de cálculo total**
  Probar combinaciones de tramos "parado" y "en movimiento" de distinta duración para asegurar que el total calculado es correcto en todos los casos.

---

## US-04 — Iniciar otra carrera sin cerrar el programa (Must)

**Historia:** Como taxista, quiero poder iniciar otra carrera sin cerrar el programa para no perder tiempo entre servicios.

**Criterios de aceptación:**
- Tras finalizar una carrera, el sistema permite iniciar una nueva sin reiniciar la aplicación.
- El estado de la aplicación se resetea correctamente (contador a cero, estado "parado") al iniciar la nueva carrera.
- El histórico de carreras previas del turno/día se conserva y no se pierde al iniciar una nueva carrera.

### Sub-issues

- **US-04.1 — Implementar reseteo de estado de aplicación tras finalizar**
  Asegurar que, al terminar una carrera, la aplicación queda lista para un nuevo ciclo: contador a cero y estado "parado", sin necesidad de reiniciar el programa.

- **US-04.2 — Verificar que el bucle principal soporta ciclos repetidos**
  Revisar el punto de entrada de la aplicación (bucle principal o sesión) para garantizar que el ciclo iniciar→cambiar→finalizar puede repetirse indefinidamente dentro de la misma ejecución.

- **US-04.3 — Integrar persistencia del histórico entre carreras consecutivas**
  Confirmar que cada carrera finalizada se añade al histórico (US-05) sin sobrescribir ni perder las carreras anteriores del mismo día.

- **US-04.4 — Tests de integración de ciclo completo**
  Simular 2 o más carreras consecutivas en una misma ejecución para validar que todo el flujo (inicio, cambios de estado, fin) funciona de forma repetida sin errores ni fugas de estado.

---

## US-05 — Ver histórico de carreras del día (Should)

**Historia:** Como responsable de flota, quiero ver el histórico de carreras del día para cuadrar caja.

**Criterios de aceptación:**
- El sistema permite consultar un listado de todas las carreras finalizadas en el día en curso.
- Cada entrada del histórico muestra al menos: hora de inicio, hora de fin, duración, importe total.
- El histórico permite calcular o visualizar el total recaudado en el día (suma de todas las carreras).
- El histórico persiste aunque se cierre y reabra la aplicación (no se pierde al reiniciar).

### Sub-issues

- **US-05.1 — Diseñar modelo de persistencia del histórico**
  Definir cómo se almacenarán las carreras finalizadas (fichero JSON/CSV o base de datos ligera tipo SQLite) dentro de `infrastructure/`, justificando la elección técnica.

- **US-05.2 — Implementar repositorio `HistoricoCarrerasRepository`**
  Crear la clase encargada de guardar cada carrera finalizada y recuperarlas posteriormente, siguiendo el patrón Repository para desacoplar el dominio del mecanismo de almacenamiento concreto.

- **US-05.3 — Implementar caso de uso `ConsultarHistoricoDelDia`**
  Desarrollar en `application/` la lógica que recupera del repositorio todas las carreras correspondientes al día en curso.

- **US-05.4 — Implementar cálculo de total recaudado en el día**
  Añadir la funcionalidad que suma los importes de todas las carreras del histórico diario para facilitar el cuadre de caja.

- **US-05.5 — Exponer comando/vista de histórico en `interfaces/`**
  Crear el punto de entrada que permite al responsable de flota consultar el listado de carreras del día y el total recaudado.

- **US-05.6 — Tests de persistencia y cálculo de total diario**
  Verificar que el histórico sobrevive a un reinicio de la aplicación y que el total diario calculado es correcto.

---

## US-06 — Logs de operación para diagnóstico (Should)

**Historia:** Como técnico, quiero que el sistema genere logs de operación para diagnosticar errores en producción.

**Criterios de aceptación:**
- El sistema registra en fichero de log los eventos clave: inicio de carrera, cambios de estado, fin de carrera, errores.
- Cada entrada de log incluye timestamp, nivel (INFO/WARNING/ERROR) y descripción del evento.
- Los logs se almacenan en la carpeta `taximeter/logs` según la estructura definida.
- Los errores no controlados (excepciones) quedan registrados sin interrumpir de forma abrupta la operación cuando sea posible.

### Sub-issues

- **US-06.1 — Configurar logger base con el módulo `logging`**
  Montar en `infrastructure/` la configuración central del logger de Python (handlers, niveles, rotación de ficheros si aplica) que usará el resto de la aplicación.

- **US-06.2 — Definir formato de log y ruta de salida**
  Establecer el formato estándar de cada línea de log (timestamp, nivel, mensaje) y asegurar que los ficheros se escriben en `taximeter/logs`.

- **US-06.3 — Instrumentar eventos clave del ciclo de vida de la carrera**
  Añadir llamadas de logging en los puntos relevantes: inicio, cambio de estado, fin de carrera y cualquier error de negocio.

- **US-06.4 — Manejar excepciones no controladas con registro en log**
  Implementar un mecanismo (try/except a nivel de aplicación o interfaz) que capture errores inesperados, los registre en el log y evite que la aplicación se cierre de forma abrupta cuando sea posible.

- **US-06.5 — Tests de generación de logs**
  Comprobar que cada evento relevante (inicio, cambio de estado, fin, error) genera efectivamente la entrada de log esperada con el formato correcto.

---

## US-07 — Cambiar tarifas por configuración sin redeployar (Should)

**Historia:** Como técnico, quiero poder cambiar las tarifas en un fichero de configuración sin redeployar.

**Criterios de aceptación:**
- Las tarifas (parado/en movimiento) se leen desde un fichero de configuración en `taximeter/config`, no están hardcodeadas.
- Un cambio en el fichero de configuración se refleja en la siguiente ejecución sin necesidad de modificar código ni redeployar.
- Si el fichero de configuración falta o tiene valores inválidos, el sistema informa del error de forma clara.

### Sub-issues

- **US-07.1 — Crear fichero de configuración de tarifas**
  Definir el formato del fichero (`.env`, `.ini` o `.json`) en `taximeter/config` que contendrá las tarifas de "parado" y "en movimiento".

- **US-07.2 — Implementar módulo de lectura de configuración**
  Desarrollar en `infrastructure/` un proveedor/repositorio de configuración que lea el fichero y exponga las tarifas al resto de la aplicación de forma desacoplada.

- **US-07.3 — Sustituir valores hardcodeados por lectura desde configuración**
  Revisar los casos de uso que aplican tarifas (US-01, US-02) para que obtengan los valores del módulo de configuración en lugar de tenerlos fijos en el código.

- **US-07.4 — Validar y manejar errores de configuración**
  Añadir comprobaciones para el caso de fichero ausente o con valores inválidos, informando claramente al usuario/técnico y evitando comportamientos inesperados.

- **US-07.5 — Tests de carga de configuración**
  Probar la carga correcta de tarifas desde un fichero válido y el comportamiento del sistema ante un fichero ausente o corrupto.

---

## US-08 — Protección con contraseña (Could)

**Historia:** Como responsable de flota, quiero que el sistema requiera contraseña para protegerlo de manipulaciones.

**Criterios de aceptación:**
- El sistema solicita una contraseña para acceder a funciones sensibles (iniciar/finalizar carrera, ver histórico, cambiar configuración).
- Un intento con contraseña incorrecta deniega el acceso y no expone información sensible.
- La contraseña no se almacena ni se muestra en texto plano en logs.

### Sub-issues

- **US-08.1 — Diseñar mecanismo de autenticación simple**
  Definir cómo se almacenará la contraseña (hasheada, en configuración) y qué esquema de verificación se usará, priorizando simplicidad para el prototipo pero sin exponer texto plano.

- **US-08.2 — Implementar caso de uso `ValidarAcceso`**
  Crear en `application/` la lógica que valida la contraseña introducida frente a la almacenada, devolviendo permitido/denegado.

- **US-08.3 — Integrar el check de contraseña en acciones sensibles**
  Añadir la validación de acceso antes de ejecutar inicio, fin de carrera, consulta de histórico y cambios de configuración.

- **US-08.4 — Asegurar que la contraseña no se loguea en texto plano**
  Revisar la instrumentación de logs (US-06) para garantizar que en ningún caso se registra la contraseña sin enmascarar u ofuscar.

- **US-08.5 — Tests de autenticación**
  Verificar el acceso correcto con contraseña válida y la denegación adecuada con contraseña incorrecta.

---

## US-09 — Interfaz visual con botones grandes (Could)

**Historia:** Como taxista, quiero una interfaz visual con botones grandes para usarlo fácilmente con el móvil o tablet.

**Criterios de aceptación:**
- Existe una interfaz gráfica (táctil-friendly) con botones de tamaño amplio para las acciones principales: iniciar, cambiar estado, finalizar.
- La interfaz muestra en pantalla el importe acumulado en tiempo real y el estado actual (parado/en movimiento).
- La interfaz es usable en pantallas de tamaño móvil/tablet (diseño responsive o adaptado).

### Sub-issues

- **US-09.1 — Elegir y justificar framework de interfaz gráfica**
  Evaluar opciones (Tkinter, PySimpleGUI u otras) y documentar en el proyecto la decisión técnica tomada, alineada con las restricciones del briefing.

- **US-09.2 — Diseñar layout con botones grandes**
  Maquetar la pantalla principal con botones amplios para iniciar, cambiar de estado y finalizar carrera, pensando en el uso táctil.

- **US-09.3 — Integrar la interfaz con los casos de uso de `application/`**
  Conectar los botones de la UI con los casos de uso ya existentes (`IniciarCarrera`, `CambiarEstadoCarrera`, `FinalizarCarrera`), sin incluir lógica de negocio en la capa de interfaz.

- **US-09.4 — Mostrar importe en tiempo real y estado actual**
  Añadir en la interfaz los elementos visuales que reflejan el importe acumulado y el estado actual de la carrera, actualizándose dinámicamente.

- **US-09.5 — Adaptar diseño para móvil/tablet**
  Ajustar el layout para que se vea y funcione correctamente en pantallas pequeñas, con un enfoque responsive o adaptado a táctil.

- **US-09.6 — Test manual/exploratorio de usabilidad**
  Realizar una sesión de prueba manual con los botones grandes para validar que son fácilmente usables en un dispositivo móvil/tablet real o simulado.

---
