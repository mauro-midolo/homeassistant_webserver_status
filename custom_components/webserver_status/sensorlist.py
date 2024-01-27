from homeassistant.components import UnitOfTime, BinarySensorDeviceClass

sensors_binary = {
        # Sensor Name: [name,device class, Unit]
        "state": ["status", BinarySensorDeviceClass.CONNECTIVITY, None],
        "response_time":  ["response time", None, UnitOfTime.SECONDS]
}