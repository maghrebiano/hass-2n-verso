"""Config flow for 2N Verso integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from py2n import Py2NDevice, Py2NConnectionData
from py2n.exceptions import Py2NError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class TwoNVersoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for 2N Verso."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                await self._test_credentials(
                    self.hass,
                    user_input[CONF_HOST],
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
            except Py2NError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    async def _test_credentials(hass: HomeAssistant, host: str, username: str, password: str) -> None:
        """Validate credentials."""
        websession = async_get_clientsession(hass)
        await Py2NDevice.create(
            websession,
            Py2NConnectionData(
                host=host,
                username=username,
                password=password,
            ),
        )
