"""Klipsch Flexus HTTP API client."""
from __future__ import annotations

import json
import logging
from urllib.parse import quote

import aiohttp

_LOGGER = logging.getLogger(__name__)


class KlipschAPI:
    """Client for Klipsch Flexus native HTTP API."""

    def __init__(self, host: str, port: int = 80, session: aiohttp.ClientSession | None = None) -> None:
        self._host = host
        self._port = port
        self._base = f"http://{host}:{port}"
        self._session = session
        self._own_session = session is None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
            self._own_session = True
        return self._session

    async def close(self) -> None:
        if self._own_session and self._session and not self._session.closed:
            await self._session.close()

    async def get_data(self, path: str) -> list:
        """GET /api/getData?path={path}&roles=value."""
        session = await self._ensure_session()
        url = f"{self._base}/api/getData?path={quote(path, safe=':/')}&roles=value"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                return await resp.json(content_type=None)
        except Exception:
            _LOGGER.debug("Failed to get %s", path)
            raise

    async def set_data(self, path: str, value: dict, roles: str = "value") -> str:
        """GET /api/setData?path={path}&roles={roles}&value={json}."""
        session = await self._ensure_session()
        val_str = json.dumps(value, separators=(",", ":"))
        url = f"{self._base}/api/setData?path={quote(path, safe=':/')}&roles={roles}&value={quote(val_str)}"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                return await resp.text()
        except Exception:
            _LOGGER.debug("Failed to set %s = %s", path, val_str)
            raise

    async def get_rows(self, path: str) -> dict:
        """GET /api/getRows?path={path}&roles=@all&from=0&to=65535&type=structure."""
        session = await self._ensure_session()
        url = f"{self._base}/api/getRows?path={quote(path, safe=':/')}&roles=@all&from=0&to=65535&type=structure"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                return await resp.json(content_type=None)
        except Exception:
            _LOGGER.debug("Failed to getRows %s", path)
            raise

    async def get_status(self) -> dict:
        """Poll full device status."""
        from .const import API_PATHS

        try:
            vol = await self.get_data(API_PATHS["volume"])
            mute = await self.get_data(API_PATHS["mute"])
            inp = await self.get_data(API_PATHS["input"])
            mode = await self.get_data(API_PATHS["mode"])
            night = await self.get_data(API_PATHS["night"])
            dialog = await self.get_data(API_PATHS["dialog"])
            bass = await self.get_data(API_PATHS["bass"])
            mid = await self.get_data(API_PATHS["mid"])
            treble = await self.get_data(API_PATHS["treble"])
            power = await self.get_data(API_PATHS["power"])
            decoder = await self.get_data(API_PATHS["decoder"])
            eq_preset = await self.get_data(API_PATHS["eq_preset"])
            dirac = await self.get_data(API_PATHS["dirac"])
            sub_w = await self.get_data(API_PATHS["sub_wired"])
            sub_wl = await self.get_data(API_PATHS["sub_wireless"])

            return {
                "online": True,
                "volume": vol[0].get("i32_", 0),
                "muted": mute[0].get("bool_", False),
                "input": inp[0].get("cinemaPhysicalAudioInput", "unknown"),
                "mode": mode[0].get("cinemaPostProcessorMode", "unknown"),
                "night_mode": night[0].get("cinemaNightMode", "off"),
                "dialog_mode": dialog[0].get("cinemaDialogMode", "off"),
                "bass": bass[0].get("i32_", 0),
                "mid": mid[0].get("i32_", 0),
                "treble": treble[0].get("i32_", 0),
                "power": power[0].get("powerTarget", {}).get("target", "unknown"),
                "decoder": decoder[0].get("cinemaAudioDecoder", "unknown"),
                "eq_preset": eq_preset[0].get("cinemaEqPreset", "unknown"),
                "dirac": dirac[0].get("i32_", -1),
                "sub_wired": sub_w[0].get("i32_", 0),
                "sub_wireless": sub_wl[0].get("i32_", 0),
            }
        except Exception:
            return {"online": False}

    # --- Setters ---

    async def set_volume(self, level: int) -> None:
        from .const import API_PATHS
        await self.set_data(API_PATHS["volume"], {"type": "i32_", "i32_": level})

    async def set_mute(self, muted: bool) -> None:
        from .const import API_PATHS
        await self.set_data(API_PATHS["mute"], {"type": "bool_", "bool_": muted})

    async def set_input(self, source: str) -> None:
        from .const import API_PATHS
        await self.set_data(
            API_PATHS["input"],
            {"type": "cinemaPhysicalAudioInput", "cinemaPhysicalAudioInput": source},
        )

    async def set_sound_mode(self, mode: str) -> None:
        from .const import API_PATHS
        await self.set_data(
            API_PATHS["mode"],
            {"type": "cinemaPostProcessorMode", "cinemaPostProcessorMode": mode},
        )

    async def set_night_mode(self, mode: str) -> None:
        from .const import API_PATHS
        await self.set_data(
            API_PATHS["night"],
            {"type": "cinemaNightMode", "cinemaNightMode": mode},
        )

    async def set_dialog_mode(self, mode: str) -> None:
        from .const import API_PATHS
        await self.set_data(
            API_PATHS["dialog"],
            {"type": "cinemaDialogMode", "cinemaDialogMode": mode},
        )

    async def set_eq(self, param: str, value: int) -> None:
        from .const import API_PATHS
        await self.set_data(API_PATHS[param], {"type": "i32_", "i32_": value})

    async def set_eq_preset(self, preset: str) -> None:
        from .const import API_PATHS
        await self.set_data(
            API_PATHS["eq_preset"],
            {"type": "cinemaEqPreset", "cinemaEqPreset": preset},
        )

    async def set_dirac(self, filter_id: int) -> None:
        from .const import API_PATHS
        await self.set_data(API_PATHS["dirac"], {"type": "i32_", "i32_": filter_id})

    async def set_sub(self, which: str, value: int) -> None:
        from .const import API_PATHS
        await self.set_data(API_PATHS[which], {"type": "i32_", "i32_": value})

    async def set_power(self, target: str) -> None:
        from .const import API_PATHS
        await self.set_data(
            API_PATHS["power_req"],
            {"target": target, "reason": "userActivity"},
            roles="activate",
        )

    async def get_dirac_filters(self) -> list[dict]:
        data = await self.get_rows("dirac:filters")
        return [
            {"id": r["value"]["i32_"], "name": r["title"]}
            for r in data.get("rows", [])
        ]
