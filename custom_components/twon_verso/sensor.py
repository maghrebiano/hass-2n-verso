from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up 2N Verso sensor based on a config entry."""
    verso = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VersoSensor(verso)])

class VersoSensor(SensorEntity):
    """Representation of a 2N Verso sensor."""

    def __init__(self, verso):
        self._verso = verso
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "2N Verso Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await self._verso.get_sensor_state()
