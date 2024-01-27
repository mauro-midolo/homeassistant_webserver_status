"""The WebServer Status integration."""
from .const import DOMAIN
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta

from .const import PLATFORMS

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True