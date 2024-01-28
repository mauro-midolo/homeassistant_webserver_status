# File: custom_components/webserver_status/config_flow.py
"""Config flow for WebServer Status integration."""
import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from .httpvalidator import HttpValidator
from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, CONF_ALIAS_VAR, CONF_URL_VAR


class WebServerStatusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """WebServer Status configuration flow."""

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is not None:
            # Validate the user input (e.g., URL format)
            if not is_valid_url(user_input['webserver_url']):
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "invalid_url"},
                )

            # Check if there's already an entry with the same URL
            #if self._async_current_entries():
            #    return self.async_show_form(
            #        step_id="user",
            #        errors={"base": "url_already_exists"},
            #    )

            # Configuration is valid, create an entry
            return self.async_create_entry(
                title=user_input['webserver_name'],
                data={CONF_ALIAS_VAR:user_input['webserver_name'], CONF_URL_VAR: user_input['webserver_url']},
            )

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_ALIAS_VAR, default="WebServer"): str,
                vol.Required(CONF_URL_VAR, default=""): str,
            }),
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

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
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