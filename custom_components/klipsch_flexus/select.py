"""Select entities for Klipsch Flexus."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    NIGHT_MODES,
    NIGHT_MODES_REVERSE,
    DIALOG_MODES,
    DIALOG_MODES_REVERSE,
    EQ_PRESETS,
)
from .coordinator import KlipschCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: KlipschCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        KlipschNightModeSelect(coordinator, entry),
        KlipschDialogModeSelect(coordinator, entry),
        KlipschEqPresetSelect(coordinator, entry),
        KlipschDiracSelect(coordinator, entry),
    ]
    async_add_entities(entities)


class KlipschNightModeSelect(CoordinatorEntity[KlipschCoordinator], SelectEntity):
    """Night mode selector."""

    _attr_has_entity_name = True
    _attr_name = "Night Mode"
    _attr_icon = "mdi:weather-night"

    def __init__(self, coordinator: KlipschCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_night_mode"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}
        self._attr_options = list(NIGHT_MODES.values())

    @property
    def current_option(self) -> str | None:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        raw = data.get("night_mode", "off")
        return NIGHT_MODES.get(raw, raw)

    async def async_select_option(self, option: str) -> None:
        raw = NIGHT_MODES_REVERSE.get(option, option)
        await self.coordinator.api.set_night_mode(raw)
        await self.coordinator.async_request_refresh()


class KlipschDialogModeSelect(CoordinatorEntity[KlipschCoordinator], SelectEntity):
    """Dialog mode selector."""

    _attr_has_entity_name = True
    _attr_name = "Dialog Mode"
    _attr_icon = "mdi:account-voice"

    def __init__(self, coordinator: KlipschCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_dialog_mode"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}
        self._attr_options = list(DIALOG_MODES.values())

    @property
    def current_option(self) -> str | None:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        raw = data.get("dialog_mode", "off")
        return DIALOG_MODES.get(raw, raw)

    async def async_select_option(self, option: str) -> None:
        raw = DIALOG_MODES_REVERSE.get(option, option)
        await self.coordinator.api.set_dialog_mode(raw)
        await self.coordinator.async_request_refresh()


class KlipschEqPresetSelect(CoordinatorEntity[KlipschCoordinator], SelectEntity):
    """EQ preset selector."""

    _attr_has_entity_name = True
    _attr_name = "EQ Preset"
    _attr_icon = "mdi:tune-variant"

    def __init__(self, coordinator: KlipschCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_eq_preset"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}
        self._attr_options = [p.title() for p in EQ_PRESETS]

    @property
    def current_option(self) -> str | None:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        raw = data.get("eq_preset", "flat")
        return raw.title()

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.api.set_eq_preset(option.lower())
        await self.coordinator.async_request_refresh()


class KlipschDiracSelect(CoordinatorEntity[KlipschCoordinator], SelectEntity):
    """Dirac room correction filter selector."""

    _attr_has_entity_name = True
    _attr_name = "Dirac Filter"
    _attr_icon = "mdi:tune"

    def __init__(self, coordinator: KlipschCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_dirac"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}
        self._dirac_map: dict[str, int] = {}
        self._dirac_reverse: dict[int, str] = {}
        self._update_filter_options()

    def _update_filter_options(self) -> None:
        filters = self.coordinator.dirac_filters
        if filters:
            self._dirac_map = {f["name"]: f["id"] for f in filters}
            self._dirac_reverse = {f["id"]: f["name"] for f in filters}
            self._attr_options = [f["name"] for f in filters]
        else:
            self._attr_options = ["off"]
            self._dirac_map = {"off": -1}
            self._dirac_reverse = {-1: "off"}

    @property
    def current_option(self) -> str | None:
        self._update_filter_options()
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        dirac_id = data.get("dirac", -1)
        return self._dirac_reverse.get(dirac_id, "off")

    async def async_select_option(self, option: str) -> None:
        filter_id = self._dirac_map.get(option, -1)
        await self.coordinator.api.set_dirac(filter_id)
        await self.coordinator.async_request_refresh()
