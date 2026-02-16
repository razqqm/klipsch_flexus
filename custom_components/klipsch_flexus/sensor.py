"""Diagnostic sensors for Klipsch Flexus."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KlipschCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: KlipschCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            KlipschResponseTimeSensor(coordinator, entry),
            KlipschStatusSensor(coordinator, entry),
        ]
    )


class KlipschResponseTimeSensor(CoordinatorEntity[KlipschCoordinator], SensorEntity):
    """API response time (last request)."""

    _attr_has_entity_name = True
    _attr_translation_key = "response_time"
    _attr_icon = "mdi:timer-outline"
    _attr_native_unit_of_measurement = UnitOfTime.MILLISECONDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator: KlipschCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_response_time"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        return data.get("poll_time_ms")

    @property
    def extra_state_attributes(self) -> dict:
        api = self.coordinator.api
        return {
            "last_request_ms": api.last_response_time,
            "total_requests": api.total_requests,
            "failed_requests": api.failed_requests,
        }


class KlipschStatusSensor(CoordinatorEntity[KlipschCoordinator], SensorEntity):
    """Device online/offline status with decoder info."""

    _attr_has_entity_name = True
    _attr_translation_key = "device_status"
    _attr_icon = "mdi:soundbar"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["offline", "on", "standby"]
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: KlipschCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}

    @property
    def native_value(self) -> str:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return "offline"
        power = data.get("power", "unknown")
        if power == "on":
            return "on"
        return "standby"

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return {}
        attrs = {
            "decoder": data.get("decoder", "unknown"),
            "input": data.get("input", "unknown"),
            "sound_mode": data.get("mode", "unknown"),
            "failed_params": data.get("failed_params", 0),
            "poll_time_ms": data.get("poll_time_ms"),
        }
        # Player info if available
        player = data.get("player")
        if player and isinstance(player, dict):
            attrs["media_title"] = player.get("title", "")
            attrs["media_artist"] = player.get("artist", "")
        return attrs
