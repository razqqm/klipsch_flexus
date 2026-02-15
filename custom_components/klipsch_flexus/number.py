"""Number entities for Klipsch Flexus (EQ, subwoofer)."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KlipschCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: KlipschCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        KlipschEqNumber(coordinator, entry, "bass", "Bass", "mdi:speaker"),
        KlipschEqNumber(coordinator, entry, "mid", "Mid", "mdi:tune"),
        KlipschEqNumber(coordinator, entry, "treble", "Treble", "mdi:music-clef-treble"),
        KlipschSubNumber(coordinator, entry, "sub_wired", "Subwoofer Wired", "mdi:subwoofer"),
        KlipschSubNumber(coordinator, entry, "sub_wireless", "Subwoofer Wireless", "mdi:subwoofer"),
    ])


class KlipschEqNumber(CoordinatorEntity[KlipschCoordinator], NumberEntity):
    """EQ parameter (bass/mid/treble)."""

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
        await self.coordinator.api.set_eq(self._param, int(value))
        await self.coordinator.async_request_refresh()


class KlipschSubNumber(CoordinatorEntity[KlipschCoordinator], NumberEntity):
    """Subwoofer level."""

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
        await self.coordinator.api.set_sub(self._param, int(value))
        await self.coordinator.async_request_refresh()
