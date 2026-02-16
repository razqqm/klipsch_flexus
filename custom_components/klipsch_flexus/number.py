"""Number entities for Klipsch Flexus channel levels."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CHANNEL_LEVELS
from .coordinator import KlipschCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: KlipschCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        KlipschChannelLevel(coordinator, entry, key, name, icon)
        for key, name, icon in CHANNEL_LEVELS
    ])


class KlipschChannelLevel(CoordinatorEntity[KlipschCoordinator], NumberEntity):
    """Channel level slider (bass/mid/treble/surround/subwoofer)."""

    _attr_has_entity_name = True
    _attr_native_min_value = -6
    _attr_native_max_value = 6
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: KlipschCoordinator,
        entry: ConfigEntry,
        param: str,
        name: str,
        icon: str,
    ) -> None:
        super().__init__(coordinator)
        self._param = param
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{entry.entry_id}_{param}"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        return data.get(self._param, 0)

    async def async_set_native_value(self, value: float) -> None:
        int_val = int(value)
        await self.coordinator.api.set_channel_level(self._param, int_val)
        # Optimistic update
        if self.coordinator.data:
            self.coordinator.data[self._param] = int_val
            self.async_write_ha_state()
        self.coordinator.async_request_delayed_refresh()
