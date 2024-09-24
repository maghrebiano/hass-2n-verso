"""The 2N Verso integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from py2n import Py2NDevice, Py2NConnectionData
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch"]

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
    except Exception as err:
        _LOGGER.error("Failed to connect to 2N Verso: %s", err)
        return False

    hass.data[DOMAIN][entry.entry_id] = verso

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

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
