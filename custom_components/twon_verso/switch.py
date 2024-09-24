from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up 2N Verso switch based on a config entry."""
    verso_data = hass.data[DOMAIN][entry.entry_id]
    switch_status = verso_data["switch_status"]
    async_add_entities([VersoSwitch(switch) for switch in switch_status["result"]["switches"]])

class VersoSwitch(SwitchEntity):
    """Representation of a 2N Verso switch."""

    def __init__(self, switch):
        self._switch = switch
        self._name = f"2N Verso Switch {switch['switch']}"
        self._state = switch["active"]
        self._locked = switch["locked"]
        self._held = switch["held"]

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "locked": self._locked,
            "held": self._held
        }

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self._control_switch("on")

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self._control_switch("off")

    async def _control_switch(self, action):
        """Control the switch."""
        url = f"http://{self._host}/api/switch/ctrl"
        params = {
            'switch': self._switch['switch'],
            'action': action
        }
        async with self._session.get(url, params=params, auth=aiohttp.BasicAuth(self._username, self._password)) as response:
            if response.status == 200:
                result = await response.json()
                self._state = result["result"]["active"]
                self._locked = result["result"]["locked"]
                self._held = result["result"]["held"]
                self.async_write_ha_state()
            else:
                response.raise_for_status()
