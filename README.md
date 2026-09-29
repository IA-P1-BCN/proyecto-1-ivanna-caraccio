# Taximeter - Prototype 1

## Interfaz gráfica — Decisión técnica (US-09.1)

Opciones evaluadas para la interfaz visual con botones grandes:

| Opción | Ventajas | Inconvenientes |
|---|---|---|
| **Tkinter** | Incluido en Python (stdlib), sin dependencias nuevas, maduro y suficiente para botones táctiles e importe en tiempo real | Estética básica |
| PySimpleGUI | Sintaxis compacta | Dependencia externa; desde 2022 su licencia/comercial genera problemas para uso libre |
| Kivy | Diseño táctil/responsive de verdad | Dependencia pesada y curva de aprendizaje desproporcionada para un prototipo |

**Decisión: Tkinter.** Cumple los criterios de US-09 (botones grandes, importe
y estado en tiempo real, ventana usable en tablet) sin añadir dependencias al
proyecto, manteniendo el enfoque stdlib del prototipo y las restricciones de
SOLID/DRY de AGENTS.md.

### Cómo ejecutar la interfaz gráfica

```bash
python src/main.py --gui   # interfaz gráfica (Tkinter)
python src/main.py         # interfaz de terminal (CLI), por defecto
```

Ambas interfaces piden la contraseña al arrancar (US-08).

## Acceso con contraseña

El sistema requiere contraseña al arrancar para proteger las funciones
sensibles (iniciar/finalizar carrera, ver histórico).

- Contraseña por defecto: `taxi123`
- Se almacena hasheada (SHA-256) en `config/auth.json`; nunca en texto plano.

Para cambiar la contraseña, genera una nueva huella y actualiza
`config/auth.json`:

```bash
python -c "import hashlib; print(hashlib.sha256('NUEVA'.encode('utf-8')).hexdigest())"
```
