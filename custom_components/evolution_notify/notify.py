import logging
import aiohttp
import os
import base64
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import CONF_URL, CONF_API_KEY
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_INSTANCE = "instance"
CONF_VERSION = "version"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_INSTANCE): cv.string,
    vol.Optional(CONF_VERSION, default=1): vol.Coerce(int),
})

def get_service(hass, config, discovery_info=None):
    """Passiamo hass al servizio per gestire le chiamate bloccanti."""
    return EvolutionNotificationService(
        hass,
        config.get(CONF_URL).rstrip("/"),
        config.get(CONF_API_KEY),
        config.get(CONF_INSTANCE),
        config.get(CONF_VERSION)
    )

class EvolutionNotificationService(BaseNotificationService):
    def __init__(self, hass, base_url, api_key, instance, version):
        self.hass = hass
        self._base_url = base_url
        self._api_key = api_key
        self._instance = instance
        self._version = version
        self._headers = {
            "apikey": self._api_key,
            "Content-Type": "application/json"
        }

    async def async_send_message(self, message="", **kwargs):
        target = kwargs.get("target")
        data = kwargs.get(ATTR_DATA) or {}
        
        if not target:
            _LOGGER.error("Target mancante")
            return

        number = target[0] if isinstance(target, list) else target
        clean_number = str(number).replace("@c.us", "").replace("@g.us", "").replace("+", "").strip()

        async with aiohttp.ClientSession() as session:
            image_url = data.get("image") or data.get("file")
            file_path = data.get("path")

            # --- LOGICA MEDIA ---
            if image_url or file_path:
                endpoint = f"{self._base_url}/message/sendMedia/{self._instance}"
                media_payload = None

                if file_path:
                    # Verifica file senza bloccare il loop
                    if not await self.hass.async_add_executor_job(os.path.isfile, file_path):
                        _LOGGER.error("File locale non trovato: %s", file_path)
                        return
                    
                    # Lettura file in Base64 senza bloccare il loop
                    def read_base64_file(path):
                        with open(path, "rb") as f:
                            return base64.b64encode(f.read()).decode("utf-8")

                    media_payload = await self.hass.async_add_executor_job(read_base64_file, file_path)
                else:
                    media_payload = image_url

                # Payload differenziato per versione
                if self._version == 1:
                    payload = {
                        "number": clean_number,
                        "mediaMessage": {
                            "mediatype": "image",
                            "caption": message,
                            "media": media_payload  # Solo stringa base64 o URL
                        }
                    }
                else: # v2
                    payload = {
                        "number": clean_number,
                        "mediatype": "image",
                        "media": media_payload,
                        "caption": message
                    }

                try:
                    async with session.post(endpoint, json=payload, headers=self._headers) as response:
                        res_text = await response.text()
                        if response.status >= 400:
                            _LOGGER.error("Errore Evolution Media (v%s): %s", self._version, res_text)
                except Exception as e:
                    _LOGGER.error("Errore connessione Evolution Media: %s", e)

            # --- LOGICA TESTO ---
            else:
                endpoint = f"{self._base_url}/message/sendText/{self._instance}"
                if self._version == 2:
                    payload = {"number": clean_number, "text": message}
                else:
                    payload = {
                        "number": clean_number,
                        "textMessage": {"text": message}
                    }

                try:
                    async with session.post(endpoint, json=payload, headers=self._headers) as response:
                        if response.status >= 400:
                            res_text = await response.text()
                            _LOGGER.error("Errore Evolution Text (v%s): %s", self._version, res_text)
                except Exception as e:
                    _LOGGER.error("Errore connessione Evolution Text: %s", e)
