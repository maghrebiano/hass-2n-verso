import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from .api import VersoAPI

@callback
def configured_instances(hass):
    """Return a set of configured 2N Verso instances."""
    return set(entry.data[CONF_HOST] for entry in hass.config_entries.async_entries(DOMAIN))

class VersoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for 2N Verso."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            if host in configured_instances(self.hass):
                errors["base"] = "already_configured"
            else:
                try:
                    session = async_get_clientsession(self.hass)
                    verso_api = VersoAPI(host, username, password)
                    await verso_api.get_system_info()
                    await verso_api.close()

                    return self.async_create_entry(title=host, data=user_input)
                except Exception:
                    errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_import(self, user_input=None):
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VersoOptionsFlowHandler(config_entry)

class VersoOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for 2N Verso."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=self.config_entry.data[CONF_HOST]): str,
            vol.Required(CONF_USERNAME, default=self.config_entry.data[CONF_USERNAME]): str,
            vol.Required(CONF_PASSWORD, default=self.config_entry.data[CONF_PASSWORD]): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
