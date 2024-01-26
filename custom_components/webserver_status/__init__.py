"""The WebServer Status integration."""
from .const import DOMAIN
from homeassistant.config_entries import SOURCE_IMPORT

async def async_setup(hass, config):
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
        )
    )
    return True