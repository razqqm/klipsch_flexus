"""Config flow for Klipsch Flexus."""

from __future__ import annotations

from urllib.parse import urlparse

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.ssdp import SsdpServiceInfo
from homeassistant.const import CONF_HOST
from homeassistant.core import callback

from .api import KlipschAPI
from .const import CONF_SCAN_INTERVAL, DOMAIN, SCAN_INTERVAL_SECONDS


class KlipschFlexusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Klipsch Flexus."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._discovered_host: str | None = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return KlipschOptionsFlow(config_entry)

    async def async_step_ssdp(self, discovery_info: SsdpServiceInfo) -> config_entries.ConfigFlowResult:
        """Handle SSDP discovery."""
        host = urlparse(discovery_info.ssdp_location or "").hostname
        if not host:
            return self.async_abort(reason="no_host")

        await self.async_set_unique_id(host)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        self._discovered_host = host
        self.context["title_placeholders"] = {"host": host}
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None) -> config_entries.ConfigFlowResult:
        """Confirm SSDP discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title=f"Klipsch Flexus ({self._discovered_host})",
                data={CONF_HOST: self._discovered_host},
            )

        return self.async_show_form(
            step_id="confirm",
            description_placeholders={"host": self._discovered_host},
        )

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
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
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input=None):
        """Handle reconfiguration (change IP address)."""
        errors = {}
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            host = user_input[CONF_HOST]
            api = KlipschAPI(host)
            try:
                status = await api.get_status()
                if status.get("online"):
                    return self.async_update_reload_and_abort(
                        entry,
                        data={CONF_HOST: host},
                        title=f"Klipsch Flexus ({host})",
                    )
                else:
                    errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"
            finally:
                await api.close()

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=entry.data.get(CONF_HOST, "")): str,
                }
            ),
            errors=errors,
        )


class KlipschOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Klipsch Flexus."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self._entry.options.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL_SECONDS),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=120)),
                }
            ),
        )
