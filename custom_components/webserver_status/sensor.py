"""Support for monitoring the status of a WebServer."""
import logging
import asyncio
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity

from .http.httpclient import HttpClient

from .const import CONF_ALIAS_VAR, CONF_SCAN_INTERVAL, CONF_URL_VAR, DEFAULT_SCAN_INTERVAL, DOMAIN
from homeassistant.helpers.entity import DeviceInfo
_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import time
from .sensorlist import sensors_binary
from homeassistant.helpers.update_coordinator import CoordinatorEntity

class WebServerStatusDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching WebServer data."""
    def __init__(self, hass, hostname, update_interval):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name=hostname, update_interval=update_interval)
        self._hostname = hostname
 
    async def _async_update_data(self):
        http_client : HttpClient = HttpClient()
        await asyncio.to_thread(http_client.get_request, self._hostname)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    webserver_url = entry.data.get(CONF_URL_VAR, '')
    if entry.options.get(CONF_SCAN_INTERVAL):
        update_interval = timedelta(seconds=entry.options[CONF_SCAN_INTERVAL])
    else:
        update_interval = timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    coordinator = WebServerStatusDataCoordinator(hass, webserver_url, update_interval)
    await coordinator.async_config_entry_first_refresh()
    for sensor_name in sensors_binary:
        async_add_entities([WebServerStatusSensor(entry, sensor_name, coordinator)], True)

class WebServerStatusEntity(CoordinatorEntity):
    def __init__(self, entry: ConfigEntry, sensor_name, coordinator: WebServerStatusDataCoordinator):
        super().__init__(coordinator)
        self._entry = entry
        self._sensor_name = sensor_name


    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self._entry.data.get(CONF_ALIAS_VAR)}-{self._sensor_name}"


    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._entry.data.get(CONF_ALIAS_VAR)} {sensors_binary[self._sensor_name][0]}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data._data[self._sensor_name]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return sensors_binary[self._sensor_name][2]
    
    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return sensors_binary[self._sensor_name][1]

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            name=self._entry.data.get(CONF_ALIAS_VAR),
            identifiers={(DOMAIN, self._entry.data.get(CONF_URL_VAR))}
            )


class WebServerStatusSensor(WebServerStatusEntity, SensorEntity):
    """Representation of a WebServer Status sensor."""