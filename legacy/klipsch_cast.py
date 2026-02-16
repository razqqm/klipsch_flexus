#!/usr/bin/env python3
"""Klipsch Flexus CORE 300 — full API control for HA (legacy CLI version).

This is the original standalone script before the custom integration was created.
Kept here as reference for the API endpoints and data format.

Uses native HTTP API on port 80 (reverse-engineered from Klipsch Connect Plus).

API format:
  GET /api/getData?path={path}&roles=value
  GET /api/setData?path={path}&roles=value&value={json}
  GET /api/setData?path={path}&roles=activate&value={json}   (for actions)
  GET /api/getRows?path={path}&roles=@all&from=0&to=65535&type=structure

Usage:
  python3 klipsch_cast.py status              # JSON status
  python3 klipsch_cast.py volume 45           # set volume
  python3 klipsch_cast.py mute / unmute       # mute control
  python3 klipsch_cast.py input hdmiarc       # set input source
  python3 klipsch_cast.py mode movie          # set sound mode
  python3 klipsch_cast.py power online        # power on
  python3 klipsch_cast.py player pause        # media control

Replace <SOUNDBAR_IP> with your soundbar's IP address.
"""
import sys, json, urllib.request
from urllib.parse import quote

HOST = "<SOUNDBAR_IP>"
BASE = f"http://{HOST}"

# API paths
PATHS = {
    # Core
    "volume":       "player:volume",
    "mute":         "settings:/mediaPlayer/mute",
    "input":        "cinema:/external/physicalAudioInput",
    "mode":         "settings:/cinema/postProcessorMode",
    "night":        "cinema:/nightMode",
    "dialog":       "settings:/cinema/dialogMode",
    "bass":         "cinema:cinemaBass",
    "mid":          "cinema:cinemaMid",
    "treble":       "cinema:cinemaTreble",
    "power":        "powermanager:target",
    "decoder":      "cinema:/audioDecoder",
    "player":       "player:player/data",
    # EQ preset
    "eq_preset":    "settings:/cinema/dsp/cinemaEqPreset",
    # Dirac room correction
    "dirac":        "dirac:/activeFilter",
    # Speaker channel volumes
    "front_height": "settings:/cinema/dsp/frontHeightVolume",
    "side_left":    "settings:/cinema/dsp/sideLeftVolume",
    "side_right":   "settings:/cinema/dsp/sideRightVolume",
    "back_height":  "settings:/cinema/dsp/backHeightVolume",
    "back_left":    "settings:/cinema/dsp/backLeftVolume",
    "back_right":   "settings:/cinema/dsp/backRightVolume",
    "sub_wired":    "settings:/cinema/dsp/wiredSubwooferVolume",
    "sub_wireless": "settings:/cinema/dsp/wirelessSubwoofersVolume",
    # Power control (action)
    "power_req":    "powermanager:targetRequest",
    # Player control (action)
    "player_ctrl":  "player:player/control",
    # Settings
    "auto_on":      "settings:/system/autoOn",
    "auto_standby": "settings:/system/autoStandby",
    "led_mode":     "settings:/cinema/ledMode",
    "peripherals":  "cinema:peripherals",
}

OFFLINE = {
    "state": "offline", "volume": 0, "muted": False,
    "input": "unknown", "mode": "unknown",
    "night_mode": "unknown", "dialog_mode": "unknown",
    "bass": 0, "mid": 0, "treble": 0,
    "power": "unknown", "decoder": "unknown",
    "eq_preset": "unknown", "dirac": -1,
    "sub_wired": 0, "sub_wireless": 0,
}


def api_get(path):
    url = f"{BASE}/api/getData?path={quote(path, safe=':/')}&roles=value"
    return json.loads(urllib.request.urlopen(urllib.request.Request(url), timeout=5).read())


def api_set(path, value, roles="value"):
    val_str = json.dumps(value, separators=(',', ':'))
    url = f"{BASE}/api/setData?path={quote(path, safe=':/')}&roles={roles}&value={quote(val_str)}"
    return urllib.request.urlopen(urllib.request.Request(url), timeout=5).read().decode()


def api_get_rows(path):
    url = f"{BASE}/api/getRows?path={quote(path, safe=':/')}&roles=@all&from=0&to=65535&type=structure"
    return json.loads(urllib.request.urlopen(urllib.request.Request(url), timeout=5).read())


def cmd_status():
    try:
        vol = api_get(PATHS["volume"])
        mute = api_get(PATHS["mute"])
        inp = api_get(PATHS["input"])
        mode = api_get(PATHS["mode"])
        night = api_get(PATHS["night"])
        dialog = api_get(PATHS["dialog"])
        bass = api_get(PATHS["bass"])
        mid = api_get(PATHS["mid"])
        treble = api_get(PATHS["treble"])
        power = api_get(PATHS["power"])
        decoder = api_get(PATHS["decoder"])
        eq_preset = api_get(PATHS["eq_preset"])
        dirac = api_get(PATHS["dirac"])
        sub_w = api_get(PATHS["sub_wired"])
        sub_wl = api_get(PATHS["sub_wireless"])

        result = {
            "state": "on",
            "volume": vol[0].get("i32_", 0),
            "muted": mute[0].get("bool_", False),
            "input": inp[0].get("cinemaPhysicalAudioInput", "unknown"),
            "mode": mode[0].get("cinemaPostProcessorMode", "unknown"),
            "night_mode": night[0].get("cinemaNightMode", "unknown"),
            "dialog_mode": dialog[0].get("cinemaDialogMode", "unknown"),
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
        result = dict(OFFLINE)
    print(json.dumps(result))


def cmd_set_volume(level):
    api_set(PATHS["volume"], {"type": "i32_", "i32_": int(level)})


def cmd_set_mute(state):
    api_set(PATHS["mute"], {"type": "bool_", "bool_": state})


def cmd_set_input(source):
    api_set(PATHS["input"], {"type": "cinemaPhysicalAudioInput", "cinemaPhysicalAudioInput": source})


def cmd_set_mode(mode):
    api_set(PATHS["mode"], {"type": "cinemaPostProcessorMode", "cinemaPostProcessorMode": mode})


def cmd_set_night(mode):
    api_set(PATHS["night"], {"type": "cinemaNightMode", "cinemaNightMode": mode})


def cmd_set_dialog(mode):
    api_set(PATHS["dialog"], {"type": "cinemaDialogMode", "cinemaDialogMode": mode})


def cmd_set_eq(param, value):
    api_set(PATHS[param], {"type": "i32_", "i32_": int(value)})


def cmd_set_eq_preset(preset):
    api_set(PATHS["eq_preset"], {"type": "cinemaEqPreset", "cinemaEqPreset": preset})


def cmd_set_dirac(filter_id):
    api_set(PATHS["dirac"], {"type": "i32_", "i32_": int(filter_id)})


def cmd_set_sub(which, value):
    api_set(PATHS[which], {"type": "i32_", "i32_": int(value)})


def cmd_set_channel(channel, value):
    api_set(PATHS[channel], {"type": "i32_", "i32_": int(value)})


def cmd_power(target):
    api_set(PATHS["power_req"], {"target": target, "reason": "userActivity"}, roles="activate")


def cmd_player_control(action):
    api_set(PATHS["player_ctrl"], {"control": action}, roles="activate")


def cmd_dirac_filters():
    data = api_get_rows("dirac:filters")
    filters = [{"id": r["value"]["i32_"], "name": r["title"]} for r in data.get("rows", [])]
    print(json.dumps(filters))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "status":
        cmd_status()
    elif args[0] == "volume" and len(args) > 1:
        cmd_set_volume(args[1])
    elif args[0] == "mute":
        cmd_set_mute(True)
    elif args[0] == "unmute":
        cmd_set_mute(False)
    elif args[0] == "input" and len(args) > 1:
        cmd_set_input(args[1])
    elif args[0] == "mode" and len(args) > 1:
        cmd_set_mode(args[1])
    elif args[0] == "night" and len(args) > 1:
        cmd_set_night(args[1])
    elif args[0] == "dialog" and len(args) > 1:
        cmd_set_dialog(args[1])
    elif args[0] in ("bass", "mid", "treble") and len(args) > 1:
        cmd_set_eq(args[0], args[1])
    elif args[0] == "eq_preset" and len(args) > 1:
        cmd_set_eq_preset(args[1])
    elif args[0] == "dirac" and len(args) > 1:
        cmd_set_dirac(args[1])
    elif args[0] == "dirac_filters":
        cmd_dirac_filters()
    elif args[0] in ("sub_wired", "sub_wireless") and len(args) > 1:
        cmd_set_sub(args[0], args[1])
    elif args[0] in ("front_height", "side_left", "side_right", "back_height", "back_left", "back_right") and len(args) > 1:
        cmd_set_channel(args[0], args[1])
    elif args[0] == "power" and len(args) > 1:
        cmd_power(args[1])
    elif args[0] == "player" and len(args) > 1:
        cmd_player_control(args[1])
