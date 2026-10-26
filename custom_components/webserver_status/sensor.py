"""Support for monitoring the status of a WebServer."""

import logging
import asyncio
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from .http.httpclient import HttpClient
from homeassistant.const import EntityCategory
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .sensorlist import optional_sensors, sensors_binary
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)
from .const import (
    CONF_ALIAS_VAR,
    CONF_LINK_URL_VAR,
    CONF_SCAN_INTERVAL,
    CONF_SLL_CHECK_VAR,
    CONF_TIMEOUT,
    CONF_URL_VAR,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DOMAIN,
)


class WebServerStatusDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching WebServer data."""

    def __init__(self, hass, hostname, update_interval, ssl_checker, timeout):
        """Initialize the coordinator."""
        super().__init__(hass, _LOGGER, name=hostname, update_interval=update_interval)
        self._hostname = hostname
        self._ssl_checker = ssl_checker
        self._timeout = timeout

    async def _async_update_data(self):
        http_client = HttpClient()
        result = await http_client.get_request(
            self.hass, self._hostname, self._ssl_checker, self._timeout
        )
        return result._data


def get_unique_id(entry: ConfigEntry, sensor_name):
    return f"{entry.data.get(CONF_ALIAS_VAR)}-{sensor_name}"


def get_link_url(entry: ConfigEntry):
    """Return the URL to open for this webserver, defaulting to the monitored one."""
    link_url = entry.options.get(
        CONF_LINK_URL_VAR, entry.data.get(CONF_LINK_URL_VAR, "")
    )
    return link_url or entry.data.get(CONF_URL_VAR)


def is_sensor_enabled(entry: ConfigEntry, sensor_name):
    """Return whether the sensor is enabled; optional sensors are off by default."""
    conf_key = optional_sensors.get(sensor_name)
    if conf_key is None:
        return True
    return entry.options.get(conf_key, entry.data.get(conf_key, False))


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    webserver_url = entry.data.get(CONF_URL_VAR, "")
    if entry.options.get(CONF_SCAN_INTERVAL):
        update_interval = timedelta(seconds=entry.options[CONF_SCAN_INTERVAL])
    else:
        update_interval = timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    ssl_checker = entry.data.get(CONF_SLL_CHECK_VAR, True)
    timeout = entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
    coordinator = WebServerStatusDataCoordinator(
        hass, webserver_url, update_interval, ssl_checker, timeout
    )
    await coordinator.async_config_entry_first_refresh()
    registry = er.async_get(hass)
    for sensor_name in sensors_binary:
        if not is_sensor_enabled(entry, sensor_name):
            # Remove the entity left over from when the sensor was enabled
            entity_id = registry.async_get_entity_id(
                "sensor", DOMAIN, get_unique_id(entry, sensor_name)
            )
            if entity_id:
                registry.async_remove(entity_id)
            continue
        async_add_entities(
            [WebServerStatusSensor(entry, sensor_name, coordinator)], True
        )


class WebServerStatusEntity(CoordinatorEntity):
    def __init__(
        self,
        entry: ConfigEntry,
        sensor_name,
        coordinator: WebServerStatusDataCoordinator,
    ):
        super().__init__(coordinator)
        self._entry = entry
        self._sensor_name = sensor_name

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return get_unique_id(self._entry, self._sensor_name)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._entry.data.get(CONF_ALIAS_VAR)} {sensors_binary[self._sensor_name][0]}"

    @property
    def native_value(self):
        return self.coordinator.data.get(self._sensor_name)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return sensors_binary[self._sensor_name][2]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return sensors_binary[self._sensor_name][1]

    @property
    def entity_category(self):
        """Show the optional sensors in the diagnostic section of the device."""
        if self._sensor_name in optional_sensors:
            return EntityCategory.DIAGNOSTIC
        return None

    @property
    def extra_state_attributes(self):
        """Expose the webserver link and the last error on the status sensor."""
        if self._sensor_name == "state":
            return {
                "url": get_link_url(self._entry),
                "error": self.coordinator.data.get("error"),
            }
        return None

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            name=self._entry.data.get(CONF_ALIAS_VAR),
            identifiers={(DOMAIN, self._entry.data.get(CONF_URL_VAR))},
            configuration_url=get_link_url(self._entry),
        )


class WebServerStatusSensor(WebServerStatusEntity, SensorEntity):
    """Representation of a WebServer Status sensor."""
