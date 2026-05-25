"""DataUpdateCoordinator for Meteotemplate."""
from __future__ import annotations

import logging
from datetime import timedelta

import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MeteotemplateCoordinator(DataUpdateCoordinator):
    """Fetch and cache the Meteotemplate Station Feed payload."""

    def __init__(
        self, hass: HomeAssistant, url: str, update_interval: timedelta
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self._url = url
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict:
        try:
            async with async_timeout.timeout(20):
                resp = await self._session.get(self._url)
                resp.raise_for_status()
                # content_type=None: the PHP plugin sometimes serves JSON as
                # text/html, which would otherwise make aiohttp refuse to parse.
                data = await resp.json(content_type=None)
        except Exception as err:  # noqa: BLE001 - surface any failure to HA
            raise UpdateFailed(f"Error fetching Meteotemplate data: {err}") from err

        if not isinstance(data, dict) or "current_conditions" not in data:
            raise UpdateFailed("Unexpected response: no 'current_conditions' block")

        return data
