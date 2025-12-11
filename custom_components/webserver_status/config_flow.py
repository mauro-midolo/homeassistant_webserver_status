# File: custom_components/webserver_status/config_flow.py
"""Config flow for WebServer Status integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from .http.httpvalidator import HttpValidator
from .const import (
    DOMAIN,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    CONF_ALIAS_VAR,
    CONF_URL_VAR,
    CONF_SLL_CHECK_VAR,
)


class WebServerStatusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """WebServer Status configuration flow."""
    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get the options flow for this handler."""
        return WebServerStatusOptionsFlowHandler(config_entry)
        
    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        self._errors = {}
        if user_input is not None:
            if not is_valid_url(user_input[CONF_URL_VAR]):
                self._errors["base"] = "invalid_url"
                return await self._show_config_form(user_input)

            return self.async_create_entry(
                title=user_input[CONF_ALIAS_VAR],
                data={
                    CONF_ALIAS_VAR: user_input[CONF_ALIAS_VAR],
                    CONF_URL_VAR: user_input[CONF_URL_VAR],
                    CONF_SLL_CHECK_VAR: user_input[CONF_SLL_CHECK_VAR],
                },
            )

        # Show the form to the user
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ALIAS_VAR, default="WebServer"): str,
                    vol.Required(CONF_URL_VAR, default=""): str,
                    vol.Required(CONF_SLL_CHECK_VAR, default=True): bool,
                }
            ),
            errors=self._errors,
        )


def is_valid_url(url):
    """Check if the provided string is a valid URL."""
    return HttpValidator().is_valid(url)


class WebServerStatusOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for Electrolux Status."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): cv.positive_int,
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_ALIAS_VAR), data=self.options
        )
