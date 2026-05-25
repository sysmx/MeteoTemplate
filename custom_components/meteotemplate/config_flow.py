"""Config flow for Meteotemplate."""
from __future__ import annotations

from typing import Any

import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL, CONF_URL
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_NAME, DEFAULT_SCAN_INTERVAL, DOMAIN, MIN_SCAN_INTERVAL


async def _validate_url(hass, url: str) -> str | None:
    """Return None if OK, otherwise an error key."""
    session = async_get_clientsession(hass)
    try:
        async with async_timeout.timeout(20):
            resp = await session.get(url)
            resp.raise_for_status()
            data = await resp.json(content_type=None)
    except Exception:  # noqa: BLE001
        return "cannot_connect"
    if not isinstance(data, dict) or "current_conditions" not in data:
        return "invalid_data"
    return None


class MeteotemplateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            url = user_input[CONF_URL].strip()
            await self.async_set_unique_id(url)
            self._abort_if_unique_id_configured()

            error = await _validate_url(self.hass, url)
            if error is None:
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME) or DEFAULT_NAME,
                    data={
                        CONF_URL: url,
                        CONF_NAME: user_input.get(CONF_NAME) or DEFAULT_NAME,
                        CONF_SCAN_INTERVAL: user_input.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    },
                )
            errors["base"] = error

        schema = vol.Schema(
            {
                vol.Required(CONF_URL): str,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL)),
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "MeteotemplateOptionsFlow":
        return MeteotemplateOptionsFlow(config_entry)


class MeteotemplateOptionsFlow(config_entries.OptionsFlow):
    """Allow changing the poll interval after setup."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        schema = vol.Schema(
            {
                vol.Optional(CONF_SCAN_INTERVAL, default=current): vol.All(
                    int, vol.Range(min=MIN_SCAN_INTERVAL)
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
