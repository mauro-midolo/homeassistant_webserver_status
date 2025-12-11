"""The WebServer Status integration."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import PLATFORMS
from .config_flow import WebServerStatusOptionsFlowHandler


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_get_options_flow(config_entry: ConfigEntry):
    """Return the options flow for this handler."""
    return WebServerStatusOptionsFlowHandler(config_entry)
