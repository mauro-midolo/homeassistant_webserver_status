
import time
import asyncio
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .connectionresult import ConnectionStatus

class HttpClient:
    async def get_request(self, hass, url, ssl_check=True) -> ConnectionStatus:
        session = async_get_clientsession(hass)
        try:
            start = time.monotonic()
            async with session.get(
                url,
                allow_redirects=False,
                timeout=5,
                ssl=ssl_check,   # in aiohttp è ssl, non verify
            ) as resp:
                duration = round(time.monotonic() - start, 2)
                return ConnectionStatus(url, "online", duration, resp.status)
        except (asyncio.TimeoutError, Exception):
            return ConnectionStatus(url, "offline", None, None)
