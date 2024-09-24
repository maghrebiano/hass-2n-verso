from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up 2N Verso switch based on a config entry."""
    verso = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VersoSwitch(verso)])

class VersoSwitch(SwitchEntity):
    """Representation of a 2N Verso switch."""

    def __init__(self, verso):
        self._verso = verso
        self._is_on = False

    @property
    def name(self):
        """Return the name of the switch."""
        return "2N Verso Switch"

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self._verso.turn_on()
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self._verso.turn_off()
        self._is_on = False
        self.async_write_ha_state()
