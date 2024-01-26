"""Support for monitoring the status of a WebServer."""
import logging
import requests
from datetime import timedelta
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the WebServer Status sensor."""
    hostname = config.get('webserver_url')
    name = config.get('webserver_name', 'WebServer Status')

    add_entities([WebServerStatusSensor(name, hostname)], True)

class WebServerStatusSensor(Entity):
    """Representation of a WebServer Status sensor."""

    def __init__(self, name, hostname):
        """Initialize the sensor."""
        self._name = name
        self._hostname = hostname
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return None

    def update(self):
        """Update the sensor."""
        try:
            response = requests.get(self._hostname, timeout=5)
            if response.status_code == 200:
                self._state = "online"
            else:
                self._state = "offline"
        except requests.RequestException:
            self._state = "offline"
