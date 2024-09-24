"""The 2N Verso integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from py2n import Py2NDevice, Py2NConnectionData
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "camera", "sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the 2N Verso component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up 2N Verso from a config entry."""
    host = entry.data[CONF_HOST]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    websession = async_get_clientsession(hass)
    
    try:
        verso = await Py2NDevice.create(
            websession,
            Py2NConnectionData(
                host=host,
                username=username,
                password=password,
            ),
        )
        hass.data[DOMAIN][entry.entry_id] = verso
        hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    except Exception as err:
        _LOGGER.error("Error setting up 2N Verso: %s", err)
        return False

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "switch")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Remove a config entry."""
    _LOGGER.info("Removing 2N Verso entry: %s", entry.entry_id)
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)
