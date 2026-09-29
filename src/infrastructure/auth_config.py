import json
import re
from pathlib import Path

from infrastructure.config_error import ConfigError

REQUIRED_KEY = "password_hash"
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class AuthConfig:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        data = self._read_json()
        return self._build_password_hash(data)

    def _read_json(self):
        if not self.path.is_file():
            raise ConfigError(
                f"Auth config file not found: {self.path}",
                f"No se encuentra el fichero de contraseñas: {self.path}",
            )

        try:
            with self.path.open(encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ConfigError(
                f"Auth config file is not valid JSON: {self.path} ({error})",
                f"El fichero de contraseñas no es un JSON válido: "
                f"{self.path}",
            ) from error
        except OSError as error:
            raise ConfigError(
                f"Auth config file could not be read: {self.path} ({error})",
                f"No se ha podido leer el fichero de contraseñas: "
                f"{self.path}",
            ) from error

        if not isinstance(data, dict):
            raise ConfigError(
                f"Auth config must be a JSON object: {self.path}",
                f"El contenido de {self.path} debe ser un objeto JSON con "
                f"la clave '{REQUIRED_KEY}'",
            )

        return data

    def _build_password_hash(self, data):
        if REQUIRED_KEY not in data:
            raise ConfigError(
                f"Missing required key '{REQUIRED_KEY}' in auth config: "
                f"{self.path}",
                f"Falta la clave '{REQUIRED_KEY}' en el fichero de "
                f"contraseñas: {self.path}",
            )

        value = data[REQUIRED_KEY]

        if not isinstance(value, str) or not HASH_PATTERN.match(value):
            raise ConfigError(
                f"Auth config key '{REQUIRED_KEY}' must be a SHA-256 hex "
                f"hash: {self.path} (got {value!r})",
                f"La clave '{REQUIRED_KEY}' de {self.path} debe ser una "
                f"huella SHA-256 válida en hexadecimal",
            )

        return value
