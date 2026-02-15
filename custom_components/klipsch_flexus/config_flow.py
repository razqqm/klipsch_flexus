"""Config flow for Klipsch Flexus."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .api import KlipschAPI
from .const import DOMAIN


class KlipschFlexusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Klipsch Flexus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            # Test connection
            api = KlipschAPI(host)
            try:
                status = await api.get_status()
                if status.get("online"):
                    await self.async_set_unique_id(host)
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title=f"Klipsch Flexus ({host})",
                        data={CONF_HOST: host},
                    )
                else:
                    errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"
            finally:
                await api.close()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default="10.0.1.51"): str,
            }),
            errors=errors,
        )
