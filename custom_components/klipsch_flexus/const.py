"""Constants for Klipsch Flexus integration."""

DOMAIN = "klipsch_flexus"
DEFAULT_PORT = 80
SCAN_INTERVAL_SECONDS = 15

# API paths
API_PATHS = {
    "volume": "player:volume",
    "mute": "settings:/mediaPlayer/mute",
    "input": "cinema:/external/physicalAudioInput",
    "mode": "settings:/cinema/postProcessorMode",
    "night": "cinema:/nightMode",
    "dialog": "settings:/cinema/dialogMode",
    "bass": "cinema:cinemaBass",
    "mid": "cinema:cinemaMid",
    "treble": "cinema:cinemaTreble",
    "power": "powermanager:target",
    "power_req": "powermanager:targetRequest",
    "decoder": "cinema:/audioDecoder",
    "eq_preset": "settings:/cinema/dsp/cinemaEqPreset",
    "dirac": "dirac:/activeFilter",
    "sub_wired": "settings:/cinema/dsp/wiredSubwooferVolume",
    "sub_wireless": "settings:/cinema/dsp/wirelessSubwoofersVolume",
}

# Source list (input names → display names)
SOURCES = {
    "hdmiarc": "TV ARC",
    "hdmi1": "HDMI",
    "spdif": "SPDIF",
    "bluetooth": "Bluetooth",
    "googlecast": "Google Cast",
}
SOURCES_REVERSE = {v: k for k, v in SOURCES.items()}

# Sound modes
SOUND_MODES = ["movie", "music", "game", "sport", "night", "direct", "surround", "stereo"]

# Night mode
NIGHT_MODES = {"off": "Off", "nightMode_1": "On"}
NIGHT_MODES_REVERSE = {v: k for k, v in NIGHT_MODES.items()}

# Dialog mode
DIALOG_MODES = {
    "off": "Off",
    "dialog_1": "Level 1",
    "dialog_2": "Level 2",
    "dialog_3": "Level 3",
}
DIALOG_MODES_REVERSE = {v: k for k, v in DIALOG_MODES.items()}

# EQ Presets
EQ_PRESETS = ["flat", "bass", "rock", "vocal"]

# Dirac filters (discovered dynamically, but defaults)
DIRAC_OFF = -1
