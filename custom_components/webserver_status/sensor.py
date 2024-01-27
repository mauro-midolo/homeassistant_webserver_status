"""Support for monitoring the status of a WebServer."""
import logging
import requests
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .Ping import ConnectionStatus
from .const import DOMAIN
from homeassistant.helpers.entity import DeviceInfo
_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta
SCAN_INTERVAL = timedelta(minutes=5)
import time
from .sensorlist import sensors_binary

class WebServerStatusDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching WebServer data."""
    def __init__(self, hass, hostname_alis, hostname):
        """Initialize the coordinator."""
        self.data : ConnectionStatus = ConnectionStatus(hostname_alis, hostname, None, None)
        super().__init__(hass, _LOGGER, name=hostname_alis, update_method=self._async_update_data)

    async def _async_update_data(self):
        try:
            start_time = time.time()
            response = requests.get(self.data._hostname, timeout=5)
            end_time = time.time()

            if response.status_code == 200:
                self.data._data["state"] = "online"
            else:
                self.data._data["state"] = "offline"
            self.data._data["response_time"] = end_time - start_time
        except requests.RequestException as e:
            _LOGGER.error(f"Error updating WebServer Status sensor: {e}")
            self.data._data["state"] = "offline"
            self.data._data["response_time"] = None


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    hostname_alis = entry.data.get('webserver_name', 'WebServer')
    webserver_url = entry.data.get('webserver_url', '')
    coordinator = WebServerStatusDataCoordinator(hass, hostname_alis, webserver_url);
    await coordinator.async_config_entry_first_refresh()
    for sensor_name in sensors_binary:
        async_add_entities([WebServerStatusSensor(sensor_name, coordinator)], True)

class WebServerStatusSensor(Entity):
    """Representation of a WebServer Status sensor."""

    def __init__(self, sensor_name, coordinator: WebServerStatusDataCoordinator):
        """Initialize the sensor."""
        self._sensor_name = sensor_name
        self._coordinator = coordinator

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self._coordinator.data._hostname_alis}-{self._sensor_name}"


    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._coordinator.data._hostname_alis}-{self._sensor_name}"

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
            name=self._coordinator.data._hostname_alis,
            identifiers={(DOMAIN, self._coordinator.data._hostname)}
            )