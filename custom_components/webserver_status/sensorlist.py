from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import UnitOfTime
sensors_binary = {
        # Sensor Name: [name,device class, Unit]
        "state": ["status", BinarySensorDeviceClass.CONNECTIVITY, None],
        "response_time":  ["response time", None, UnitOfTime.SECONDS],
        "response_status":  ["response status", None, None]
}