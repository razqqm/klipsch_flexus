"""Constants for Klipsch Flexus integration."""

DOMAIN = "klipsch_flexus"
DEFAULT_PORT = 80
SCAN_INTERVAL_SECONDS = 15
CONF_SCAN_INTERVAL = "scan_interval"

# API timeouts (seconds) — soundbar is single-threaded and slow
API_TIMEOUT_READ = 8
API_TIMEOUT_WRITE = 10
API_TIMEOUT_POWER = 15  # device needs time to wake up

# Retry settings
API_RETRIES = 2
API_RETRY_DELAY = 0.5  # seconds between retries

# Delay before refresh after command (let device process)
COMMAND_REFRESH_DELAY = 1.0

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
    # Surround channel levels (Dolby Atmos)
    "back_height": "settings:/cinema/dsp/backHeightVolume",
    "back_left": "settings:/cinema/dsp/backLeftVolume",
    "back_right": "settings:/cinema/dsp/backRightVolume",
    "front_height": "settings:/cinema/dsp/frontHeightVolume",
    "side_left": "settings:/cinema/dsp/sideLeftVolume",
    "side_right": "settings:/cinema/dsp/sideRightVolume",
    "player": "player:player/data",
    "player_control": "player:player/control",
}

# Channel level keys (bass/mid/treble + surround speakers + subwoofers)
CHANNEL_LEVELS = [
    ("bass",         "Bass",              "mdi:speaker"),
    ("mid",          "Mid",               "mdi:tune"),
    ("treble",       "Treble",            "mdi:music-clef-treble"),
    ("front_height", "Front Height",      "mdi:speaker"),
    ("side_left",    "Side Left",         "mdi:speaker"),
    ("side_right",   "Side Right",        "mdi:speaker"),
    ("back_left",    "Back Left",         "mdi:speaker"),
    ("back_right",   "Back Right",        "mdi:speaker"),
    ("back_height",  "Back Height",       "mdi:speaker"),
    ("sub_wired",    "Subwoofer Wired",   "mdi:subwoofer"),
    ("sub_wireless", "Subwoofer Wireless", "mdi:subwoofer"),
]

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
