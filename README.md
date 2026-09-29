# Taximeter - Prototype 1

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
