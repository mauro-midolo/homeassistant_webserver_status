import time
import logging
import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .connectionresult import ConnectionStatus

_LOGGER = logging.getLogger(__name__)

class HttpClient:
    async def get_request(self, hass, url, ssl_check=True, timeout=5) -> ConnectionStatus:
        session = async_get_clientsession(hass)
        try:
            start = time.monotonic()
            async with session.get(
                url,
                allow_redirects=False,
                timeout=aiohttp.ClientTimeout(total=timeout),
                ssl=ssl_check,
            ) as resp:
                duration = round(time.monotonic() - start, 2)
                return ConnectionStatus(url, "online", duration, resp.status)
        except TimeoutError:
            error = f"No response within {timeout} seconds"
        except Exception as err:
            # e.g. "Cannot connect to host example.com:443 ssl:default [Network is unreachable]"
            error = str(err) or type(err).__name__
        _LOGGER.debug("%s is offline: %s", url, error)
        return ConnectionStatus(url, "offline", None, None, error)
