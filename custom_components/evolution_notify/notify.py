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

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_INSTANCE): cv.string,
})

def get_service(hass, config, discovery_info=None):
    """Ottieni il servizio Evolution API."""
    return EvolutionNotificationService(
        config.get(CONF_URL).rstrip("/"),
        config.get(CONF_API_KEY),
        config.get(CONF_INSTANCE)
    )

class EvolutionNotificationService(BaseNotificationService):
    def __init__(self, base_url, api_key, instance):
        self._base_url = base_url
        self._api_key = api_key
        self._instance = instance
        self._headers = {"apikey": self._api_key}

    async def async_send_message(self, message="", **kwargs):
        target = kwargs.get("target")
        data = kwargs.get(ATTR_DATA) or {}
        
        if not target:
            _LOGGER.error("Target mancante")
            return

        number = target[0] if isinstance(target, list) else target
        # Evolution vuole solo numeri (senza @c.us di solito, lo aggiunge lei)
        clean_number = number.replace("@c.us", "").replace("@g.us", "")

        async with aiohttp.ClientSession() as session:
            # 1. GESTIONE IMMAGINE (Locale o URL)
            image_url = data.get("image") or data.get("file")
            file_path = data.get("path")

            if image_url or file_path:
                endpoint = f"{self._base_url}/message/sendMedia/{self._instance}"
                
                if file_path:
                    # Invio file locale come Multipart
                    if not os.path.isfile(file_path):
                        _LOGGER.error("File locale non trovato: %s", file_path)
                        return
                    
                    form_data = aiohttp.FormData()
                    form_data.add_field("number", clean_number)
                    form_data.add_field("mediatype", "image")
                    form_data.add_field("caption", message)
                    with open(file_path, 'rb') as f:
                        form_data.add_field("media", f.read(), filename=os.path.basename(file_path))
                    
                    payload = form_data
                else:
                    # Invio da URL
                    payload = {
                        "number": clean_number,
                        "mediatype": "image",
                        "media": image_url,
                        "caption": message
                    }

            # 2. GESTIONE TESTO SEMPLICE
            else:
                endpoint = f"{self._base_url}/message/sendText/{self._instance}"
                payload = {
                    "number": clean_number,
                    "text": message,
                    "delay": 1200,
                    "linkPreview": True
                }

            try:
                # Evolution API accetta JSON o FormData
                kwargs_request = {"headers": self._headers}
                if isinstance(payload, aiohttp.FormData):
                    kwargs_request["data"] = payload
                else:
                    kwargs_request["json"] = payload

                async with session.post(endpoint, **kwargs_request) as response:
                    if response.status >= 400:
                        res_text = await response.text()
                        _LOGGER.error("Errore Evolution API: %s", res_text)
            except Exception as e:
                _LOGGER.error("Errore connessione Evolution: %s", e)