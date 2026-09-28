import json
from pathlib import Path

from domain.rates import Rates

REQUIRED_KEYS = ("stopped", "moving")


class ConfigError(Exception):
    def __init__(self, message, user_message):
        super().__init__(message)
        self.user_message = user_message


class RatesConfig:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        data = self._read_json()
        return self._build_rates(data)

    def _read_json(self):
        if not self.path.is_file():
            raise ConfigError(
                f"Rates config file not found: {self.path}",
                f"No se encuentra el fichero de configuración: {self.path}",
            )

        try:
            with self.path.open(encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ConfigError(
                f"Rates config file is not valid JSON: {self.path} ({error})",
                f"El fichero de configuración no es un JSON válido: "
                f"{self.path}",
            ) from error
        except OSError as error:
            raise ConfigError(
                f"Rates config file could not be read: {self.path} ({error})",
                f"No se ha podido leer el fichero de configuración: "
                f"{self.path}",
            ) from error

        if not isinstance(data, dict):
            raise ConfigError(
                f"Rates config must be a JSON object: {self.path}",
                f"El contenido de {self.path} debe ser un objeto JSON con "
                f"las claves 'stopped' y 'moving'",
            )

        return data

    def _build_rates(self, data):
        missing = [key for key in REQUIRED_KEYS if key not in data]

        if missing:
            keys = ", ".join(f"'{key}'" for key in missing)
            raise ConfigError(
                f"Missing required key(s) {keys} in rates config: "
                f"{self.path}",
                f"Faltan las claves {keys} en el fichero de "
                f"configuración: {self.path}",
            )

        return Rates(stopped=data["stopped"], moving=data["moving"])
