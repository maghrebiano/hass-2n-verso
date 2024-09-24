"""Support for 2N Verso switch."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from py2n.exceptions import Py2NError

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the 2N Verso switch."""
    verso = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VersoDoorSwitch(verso)], True)

class VersoDoorSwitch(SwitchEntity):
    """Representation of a 2N Verso door switch."""

    def __init__(self, verso):
        """Initialize the switch."""
        self._verso = verso
        self._is_on = False
        self._attr_name = "2N Verso Door"
        self._attr_unique_id = f"{self._verso.serial_number}_door_switch"

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        try:
            await self._verso.switch.control(1, True)  # 1 is typically the ID for the main door switch
            self._is_on = True
        except Py2NError as err:
            _LOGGER.error("Failed to turn on switch: %s", err)

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        try:
            await self._verso.switch.control(1, False)
            self._is_on = False
        except Py2NError as err:
            _LOGGER.error("Failed to turn off switch: %s", err)

    async def async_update(self):
        """Update switch status."""
        try:
            status = await self._verso.switch.get_status(1)
            self._is_on = status.active
        except Py2NError as err:
            _LOGGER.error("Failed to update switch status: %s", err)
