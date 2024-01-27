"""Support for monitoring the status of a WebServer."""
import logging
import asyncio
import requests
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from .Ping import ConnectionStatus
from .const import DOMAIN
from homeassistant.helpers.entity import DeviceInfo
_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import time
from .sensorlist import sensors_binary
from homeassistant.helpers.update_coordinator import CoordinatorEntity

class WebServerStatusDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching WebServer data."""
    def __init__(self, hass, hostname):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name=hostname, update_method=self._async_update_data, update_interval=30)
        self._hostname = hostname
        _LOGGER.warning("DATA!:" + self.data );
 
    async def _async_update_data(self):
        try:
            start_time = time.time()
            response = response = await asyncio.to_thread(requests.get, self._hostname, timeout=5)
            end_time = time.time()
            state_result="offline"
            if response.status_code == 200:
                state_result = "online"
            duration_time = end_time - start_time
            return ConnectionStatus(self._hostname, state_result, duration_time)
        except requests.RequestException as e:
            return ConnectionStatus(self._hostname, "offline", None)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    webserver_url = entry.data.get('webserver_url', '')
    coordinator = WebServerStatusDataCoordinator(hass, webserver_url);
    await coordinator.async_config_entry_first_refresh();
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
        return f"{self.entry.data.get('webserver_name')}-{self._sensor_name}"


    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.entry.data.get('webserver_name')}-{self._sensor_name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._coordinator.data._data[self._sensor_name]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return None

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            name=self.entry.data.get('webserver_name'),
            identifiers={(DOMAIN, self._entry.data.get('webserver_url'))}
            )


class WebServerStatusSensor(WebServerStatusEntity, SensorEntity):
    """Representation of a WebServer Status sensor."""