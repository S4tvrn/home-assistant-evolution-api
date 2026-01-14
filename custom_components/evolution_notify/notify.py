import logging
import aiohttp
import os
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
    vol.Optional(CONF_VERSION, default=1): vol.Coerce(int), # Default a v1
})

def get_service(hass, config, discovery_info=None):
    """Ottieni il servizio Evolution API."""
    return EvolutionNotificationService(
        config.get(CONF_URL).rstrip("/"),
        config.get(CONF_API_KEY),
        config.get(CONF_INSTANCE),
        config.get(CONF_VERSION)
    )

class EvolutionNotificationService(BaseNotificationService):
    def __init__(self, base_url, api_key, instance, version):
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
                
                if file_path:
                    # Multipart (uguale per v1 e v2)
                    headers = {"apikey": self._api_key}
                    form_data = aiohttp.FormData()
                    form_data.add_field("number", clean_number)
                    form_data.add_field("mediatype", "image")
                    form_data.add_field("caption", message)
                    with open(file_path, 'rb') as f:
                        form_data.add_field("media", f.read(), filename=os.path.basename(file_path))
                    payload_args = {"data": form_data, "headers": headers}
                else:
                    # JSON Media URL
                    payload = {
                        "number": clean_number,
                        "mediatype": "image",
                        "media": image_url,
                        "caption": message
                    }
                    payload_args = {"json": payload, "headers": self._headers}

                try:
                    async with session.post(endpoint, **payload_args) as response:
                        if response.status >= 400:
                            res_text = await response.text()
                            _LOGGER.error("Errore Evolution Media (v%s): %s", self._version, res_text)
                except Exception as e:
                    _LOGGER.error("Errore connessione Evolution Media: %s", e)

            # --- LOGICA TESTO (DIFFERENZIATA PER VERSIONE) ---
            else:
                endpoint = f"{self._base_url}/message/sendText/{self._instance}"
                
                if self._version == 2:
                    # Struttura Evolution v2 (Piatta)
                    payload = {
                        "number": clean_number,
                        "text": message,
                        "delay": 1200
                    }
                else:
                    # Struttura Evolution v1 (Nested textMessage)
                    payload = {
                        "number": clean_number,
                        "options": {"delay": 1200, "presence": "composing", "linkPreview": True},
                        "textMessage": {"text": message}
                    }

                try:
                    async with session.post(endpoint, json=payload, headers=self._headers) as response:
                        if response.status >= 400:
                            res_text = await response.text()
                            _LOGGER.error("Errore Evolution Text (v%s): %s", self._version, res_text)
                except Exception as e:
                    _LOGGER.error("Errore connessione Evolution Text: %s", e)
