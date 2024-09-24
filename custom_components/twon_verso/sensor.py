from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up 2N Verso sensor based on a config entry."""
    verso_data = hass.data[DOMAIN][entry.entry_id]
    system_info = verso_data["system_info"]
    system_status = verso_data["system_status"]
    switch_status = verso_data["switch_status"]
    call_status = verso_data["call_status"]
    camera_caps = verso_data["camera_caps"]
    async_add_entities([
        VersoSystemInfoSensor(system_info),
        VersoSystemStatusSensor(system_status),
        VersoSwitchStatusSensor(switch_status),
        VersoCallStatusSensor(call_status),
        VersoCameraCapsSensor(camera_caps)
    ])

class VersoSystemInfoSensor(SensorEntity):
    """Representation of a 2N Verso system info sensor."""

    def __init__(self, system_info):
        self._system_info = system_info
        self._name = system_info["result"]["deviceName"]
        self._state = system_info["result"]["swVersion"]

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} Firmware Version"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "device_type": self._system_info["result"]["devType"],
            "serial_number": self._system_info["result"]["serialNumber"],
            "mac_address": self._system_info["result"]["macAddr"],
            "hardware_version": self._system_info["result"]["hwVersion"],
            "firmware_package": self._system_info["result"]["firmwarePackage"],
            "build_type": self._system_info["result"]["buildType"],
        }

class VersoSystemStatusSensor(SensorEntity):
    """Representation of a 2N Verso system status sensor."""

    def __init__(self, system_status):
        self._system_status = system_status
        self._name = "2N Verso System Status"
        self._state = system_status["result"]["systemTime"]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "up_time": self._system_status["result"]["upTime"]
        }

class VersoSwitchStatusSensor(SensorEntity):
    """Representation of a 2N Verso switch status sensor."""

    def __init__(self, switch_status):
        self._switch_status = switch_status
        self._name = "2N Verso Switch Status"
        self._state = switch_status["result"]["switches"]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {}
        for switch in self._state:
            attributes[f"switch_{switch['switch']}_active"] = switch["active"]
            attributes[f"switch_{switch['switch']}_locked"] = switch["locked"]
            attributes[f"switch_{switch['switch']}_held"] = switch["held"]
        return attributes

class VersoCallStatusSensor(SensorEntity):
    """Representation of a 2N Verso call status sensor."""

    def __init__(self, call_status):
        self._call_status = call_status
        self._name = "2N Verso Call Status"
        self._state = call_status["result"]["sessions"]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {}
        for session in self._state:
            attributes[f"session_{session['session']}_direction"] = session["direction"]
            attributes[f"session_{session['session']}_state"] = session["state"]
        return attributes

class VersoCameraCapsSensor(SensorEntity):
    """Representation of a 2N Verso camera capabilities sensor."""

    def __init__(self, camera_caps):
        self._camera_caps = camera_caps
        self._name = "2N Verso Camera Capabilities"
        self._state = "available"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "jpeg_resolutions": self._camera_caps["result"]["jpegResolution"],
            "sources": self._camera_caps["result"]["sources"]
        }
