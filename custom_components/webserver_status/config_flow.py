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
    CONF_TIMEOUT,
    DEFAULT_TIMEOUT,
    CONF_ALIAS_VAR,
    CONF_URL_VAR,
    CONF_SLL_CHECK_VAR,
    CONF_LINK_URL_VAR,
    CONF_LAST_CHECK_VAR,
)


class WebServerStatusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """WebServer Status configuration flow."""
    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get the options flow for this handler."""
        return WebServerStatusOptionsFlowHandler()
        
    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        self._errors = {}
        if user_input is not None:
            if not is_valid_url(user_input[CONF_URL_VAR]):
                self._errors["base"] = "invalid_url"
                return await self._show_config_form(user_input)
            link_url = user_input.get(CONF_LINK_URL_VAR, "").strip()
            if link_url and not is_valid_url(link_url):
                self._errors["base"] = "invalid_link_url"
                return await self._show_config_form(user_input)

            return self.async_create_entry(
                title=user_input[CONF_ALIAS_VAR],
                data={
                    CONF_ALIAS_VAR: user_input[CONF_ALIAS_VAR],
                    CONF_URL_VAR: user_input[CONF_URL_VAR],
                    CONF_SLL_CHECK_VAR: user_input[CONF_SLL_CHECK_VAR],
                    CONF_LINK_URL_VAR: link_url,
                    CONF_LAST_CHECK_VAR: user_input.get(CONF_LAST_CHECK_VAR, False),
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
                    vol.Optional(CONF_LINK_URL_VAR): str,
                    vol.Optional(CONF_LAST_CHECK_VAR, default=False): bool,
                }
            ),
            errors=self._errors,
        )


def is_valid_url(url):
    """Check if the provided string is a valid URL."""
    return HttpValidator().is_valid(url)


class WebServerStatusOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for Webserver Status."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            # Il campo svuotato non viene inviato: lo salvo come stringa vuota
            link_url = user_input.get(CONF_LINK_URL_VAR, "").strip()
            if link_url and not is_valid_url(link_url):
                errors["base"] = "invalid_link_url"
            else:
                # Parto dalle opzioni esistenti e applico le modifiche
                options = dict(self.config_entry.options)
                options.update(user_input)
                options[CONF_LINK_URL_VAR] = link_url

                return self.async_create_entry(
                    title=self.config_entry.data.get(CONF_ALIAS_VAR),
                    data=options,
                )

        # Default value: prendo dalle options o dal default
        default_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        default_timeout = self.config_entry.options.get(
            CONF_TIMEOUT, DEFAULT_TIMEOUT
        )
        current_link_url = self.config_entry.options.get(
            CONF_LINK_URL_VAR, self.config_entry.data.get(CONF_LINK_URL_VAR, "")
        )
        current_last_check = self.config_entry.options.get(
            CONF_LAST_CHECK_VAR, self.config_entry.data.get(CONF_LAST_CHECK_VAR, False)
        )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=default_interval,
                    ): cv.positive_int,
                    vol.Optional(
                        CONF_TIMEOUT,
                        default=default_timeout,
                    ): vol.All(vol.Coerce(int), vol.Range(min=1)),
                    vol.Optional(
                        CONF_LINK_URL_VAR,
                        description={"suggested_value": current_link_url},
                    ): str,
                    vol.Optional(
                        CONF_LAST_CHECK_VAR,
                        default=current_last_check,
                    ): bool,
                }
            ),
            errors=errors,
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_ALIAS_VAR), data=self.options
        )
