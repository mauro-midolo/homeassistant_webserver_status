"""Support for monitoring the status of a WebServer."""
import logging
import requests
from datetime import timedelta
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the WebServer Status sensor."""
    host = config.get('host')
    port = config.get('port', 80)
    name = config.get('name', 'WebServer Status')

    add_entities([WebServerStatusSensor(name, host, port)], True)

class WebServerStatusSensor(Entity):
    """Representation of a WebServer Status sensor."""

    def __init__(self, name, host, port):
        """Initialize the sensor."""
        self._name = name
        self._host = host
        self._port = port
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
            response = requests.get(f"http://{self._host}:{self._port}", timeout=5)
            if response.status_code == 200:
                self._state = "online"
            else:
                self._state = "offline"
        except requests.RequestException:
            self._state = "offline"
