# File: custom_components/webserver_status/config_flow.py
"""Config flow for WebServer Status integration."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

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
            if self._async_current_entries():
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "url_already_exists"},
                )

            # Configuration is valid, create an entry
            return self.async_create_entry(
                title=user_input['webserver_name'],
                data={"webserver_url": user_input['webserver_url']},
            )

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required('webserver_name', default="WebServer"): str,
                vol.Required('webserver_url', default=""): str,
            }),
        )

def is_valid_url(url):
    """Check if the provided string is a valid URL."""
    # Add your custom URL validation logic here
    return True  # Placeholder for validation

# Note: You may need to add translations for error messages in your language file.