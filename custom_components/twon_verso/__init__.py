"""The 2N Verso integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from .api import VersoAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the 2N Verso component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up 2N Verso from a config entry."""
    host = entry.data[CONF_HOST]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    verso_api = VersoAPI(host, username, password)
    
    try:
        system_info = await verso_api.get_system_info()
        system_status = await verso_api.get_system_status()
        switch_status = await verso_api.get_switch_status()
        call_status = await verso_api.get_call_status()
        camera_caps = await verso_api.get_camera_caps()
        hass.data[DOMAIN][entry.entry_id] = {
            "api": verso_api,
            "system_info": system_info,
            "system_status": system_status,
            "switch_status": switch_status,
            "call_status": call_status,
            "camera_caps": camera_caps
        }

        async def handle_dial_call(call):
            """Handle the service call."""
            number = call.data.get("number")
            users = call.data.get("users")
            response = await verso_api.dial_call(number=number, users=users)
            _LOGGER.info("Dial call response: %s", response)

        async def handle_answer_call(call):
            """Handle the service call."""
            session = call.data.get("session")
            response = await verso_api.answer_call(session=session)
            _LOGGER.info("Answer call response: %s", response)

        async def handle_hangup_call(call):
            """Handle the service call."""
            session = call.data.get("session")
            reason = call.data.get("reason", "normal")
            response = await verso_api.hangup_call(session=session, reason=reason)
            _LOGGER.info("Hangup call response: %s", response)

        async def handle_camera_snapshot(call):
            """Handle the service call."""
            width = call.data.get("width")
            height = call.data.get("height")
            source = call.data.get("source")
            fps = call.data.get("fps")
            time = call.data.get("time")
            response = await verso_api.get_camera_snapshot(width=width, height=height, source=source, fps=fps, time=time)
            _LOGGER.info("Camera snapshot response: %s", response)

        hass.services.async_register(DOMAIN, "dial_call", handle_dial_call)
        hass.services.async_register(DOMAIN, "answer_call", handle_answer_call)
        hass.services.async_register(DOMAIN, "hangup_call", handle_hangup_call)
        hass.services.async_register(DOMAIN, "camera_snapshot", handle_camera_snapshot)

        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except Exception as err:
        _LOGGER.error("Error setting up 2N Verso: %s", err)
        return False

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
