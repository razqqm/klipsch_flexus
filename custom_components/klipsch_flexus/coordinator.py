"""Data update coordinator for Klipsch Flexus."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import KlipschAPI
from .const import COMMAND_REFRESH_DELAY, DOMAIN, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class KlipschCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to poll Klipsch device status."""

    def __init__(
        self, hass: HomeAssistant, api: KlipschAPI, name: str, scan_interval: int = SCAN_INTERVAL_SECONDS
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{name}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api
        self.dirac_filters: list[dict] = []
        self.device_info: dict | None = None  # eureka_info from port 8008

    async def _async_update_data(self) -> dict:
        try:
            status = await self.api.get_status()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Klipsch: {err}") from err

        if not status.get("online"):
            return {"online": False}

        # Fetch device info once (eureka_info from Google Cast API)
        if self.device_info is None:
            try:
                self.device_info = await self.api.get_device_info()
            except Exception:
                _LOGGER.debug("Failed to fetch device info from port 8008")

        # Fetch Dirac filters once
        if not self.dirac_filters:
            try:
                self.dirac_filters = await self.api.get_dirac_filters()
            except Exception:
                self.dirac_filters = []

        # Fetch player/media data
        try:
            player = await self.api.get_player_data()
            if player:
                status["player"] = player
        except Exception:
            _LOGGER.debug("Failed to fetch player data")

        return status

    @callback
    def async_request_delayed_refresh(self, delay: float = COMMAND_REFRESH_DELAY) -> None:
        """Schedule a refresh after delay (non-blocking).

        Gives the soundbar time to process a command before we poll its state.
        """
        self.hass.loop.call_later(
            delay,
            lambda: self.hass.async_create_task(self.async_request_refresh()),
        )
