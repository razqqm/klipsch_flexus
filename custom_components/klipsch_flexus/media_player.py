"""Media player platform for Klipsch Flexus."""
from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SOURCES, SOURCES_REVERSE, SOUND_MODES
from .coordinator import KlipschCoordinator

_BASE_FEATURES = (
    MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
    | MediaPlayerEntityFeature.SELECT_SOUND_MODE
    | MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.TURN_OFF
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: KlipschCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([KlipschMediaPlayer(coordinator, entry)])


class KlipschMediaPlayer(CoordinatorEntity[KlipschCoordinator], MediaPlayerEntity):
    """Klipsch Flexus media player."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_icon = "mdi:speaker"

    def __init__(self, coordinator: KlipschCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_media_player"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Klipsch Flexus CORE 300",
            "manufacturer": "Klipsch",
            "model": "Flexus CORE 300",
        }
        self._attr_source_list = list(SOURCES.values())
        self._attr_sound_mode_list = SOUND_MODES

    def _player_data(self) -> dict:
        data = self.coordinator.data or {}
        return data.get("player", {})

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        features = _BASE_FEATURES
        player = self._player_data()
        controls = player.get("controls", {})
        if controls.get("pause"):
            features |= MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE
        if controls.get("next_"):
            features |= MediaPlayerEntityFeature.NEXT_TRACK
        if controls.get("previous"):
            features |= MediaPlayerEntityFeature.PREVIOUS_TRACK
        return features

    @property
    def state(self) -> MediaPlayerState:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return MediaPlayerState.OFF
        power = data.get("power", "unknown")
        if power == "networkStandby":
            return MediaPlayerState.STANDBY
        player = self._player_data()
        player_state = player.get("state")
        if player_state == "playing":
            return MediaPlayerState.PLAYING
        if player_state == "paused":
            return MediaPlayerState.PAUSED
        return MediaPlayerState.IDLE

    @property
    def volume_level(self) -> float | None:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        return data.get("volume", 0) / 100.0

    @property
    def is_volume_muted(self) -> bool | None:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return None
        return data.get("muted", False)

    @property
    def source(self) -> str | None:
        data = self.coordinator.data or {}
        raw = data.get("input", "unknown")
        return SOURCES.get(raw, raw)

    @property
    def sound_mode(self) -> str | None:
        data = self.coordinator.data or {}
        return data.get("mode")

    @property
    def media_content_type(self) -> MediaType | None:
        player = self._player_data()
        if player.get("state") in ("playing", "paused"):
            return MediaType.MUSIC
        return None

    @property
    def media_title(self) -> str | None:
        player = self._player_data()
        track = player.get("trackRoles", {})
        return track.get("title")

    @property
    def media_artist(self) -> str | None:
        player = self._player_data()
        meta = player.get("trackRoles", {}).get("mediaData", {}).get("metaData", {})
        return meta.get("artist")

    @property
    def media_album_name(self) -> str | None:
        player = self._player_data()
        meta = player.get("trackRoles", {}).get("mediaData", {}).get("metaData", {})
        return meta.get("album")

    @property
    def media_image_url(self) -> str | None:
        player = self._player_data()
        track = player.get("trackRoles", {})
        return track.get("icon")

    @property
    def media_duration(self) -> int | None:
        player = self._player_data()
        status = player.get("status", {})
        duration_ms = status.get("duration")
        if duration_ms is not None:
            return duration_ms // 1000
        return None

    @property
    def app_name(self) -> str | None:
        player = self._player_data()
        media_roles = player.get("mediaRoles", {})
        return media_roles.get("title")

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data or {}
        if not data.get("online"):
            return {}
        attrs = {"decoder": data.get("decoder", "unknown")}
        player = self._player_data()
        meta = player.get("trackRoles", {}).get("mediaData", {}).get("metaData", {})
        app = meta.get("externalAppName")
        if app:
            attrs["source_app"] = app
        return attrs

    async def async_set_volume_level(self, volume: float) -> None:
        await self.coordinator.api.set_volume(round(volume * 100))
        await self.coordinator.async_request_refresh()

    async def async_volume_up(self) -> None:
        data = self.coordinator.data or {}
        current = data.get("volume", 0)
        await self.coordinator.api.set_volume(min(current + 5, 100))
        await self.coordinator.async_request_refresh()

    async def async_volume_down(self) -> None:
        data = self.coordinator.data or {}
        current = data.get("volume", 0)
        await self.coordinator.api.set_volume(max(current - 5, 0))
        await self.coordinator.async_request_refresh()

    async def async_mute_volume(self, mute: bool) -> None:
        await self.coordinator.api.set_mute(mute)
        await self.coordinator.async_request_refresh()

    async def async_select_source(self, source: str) -> None:
        raw = SOURCES_REVERSE.get(source, source)
        await self.coordinator.api.set_input(raw)
        await self.coordinator.async_request_refresh()

    async def async_select_sound_mode(self, sound_mode: str) -> None:
        await self.coordinator.api.set_sound_mode(sound_mode)
        await self.coordinator.async_request_refresh()

    async def async_media_play(self) -> None:
        await self.coordinator.api.media_control("pause")
        await self.coordinator.async_request_refresh()

    async def async_media_pause(self) -> None:
        await self.coordinator.api.media_control("pause")
        await self.coordinator.async_request_refresh()

    async def async_media_next_track(self) -> None:
        await self.coordinator.api.media_control("next")
        await self.coordinator.async_request_refresh()

    async def async_media_previous_track(self) -> None:
        await self.coordinator.api.media_control("previous")
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self) -> None:
        await self.coordinator.api.set_power("online")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        await self.coordinator.api.set_power("networkStandby")
        await self.coordinator.async_request_refresh()
