from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTime
from .const import CONF_LAST_CHECK_VAR
sensors_binary = {
        # Sensor Name: [name,device class, Unit]
        "state": ["status", BinarySensorDeviceClass.CONNECTIVITY, None],
        "response_time":  ["response time", None, UnitOfTime.SECONDS],
        "response_status":  ["response status", None, None],
        "last_check":  ["last check", SensorDeviceClass.TIMESTAMP, None]
}

# Sensors created only when enabled by the user (Sensor Name: config key)
optional_sensors = {
        "last_check": CONF_LAST_CHECK_VAR
}
