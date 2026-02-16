# Klipsch Flexus CORE 300

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![Validate](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml)
[![Hassfest](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml)

Home Assistant integration for **Klipsch Flexus CORE 300** (5.1.2-Channel Dolby Atmos Sound Bar).

Controls the soundbar via its native local HTTP API — no cloud, no delays.

![Klipsch Flexus CORE 300](custom_components/klipsch_flexus/images/icon.png)

## Features

### Media Player
- Volume control (set / step / mute)
- Power on / off (standby)
- Input source selection (TV ARC, HDMI, SPDIF, Bluetooth, Google Cast)
- Sound mode (Movie, Music, Game, Sport, Night, Direct, Surround, Stereo)
- Playback controls — play/pause, next/previous track
- Media metadata — title, artist, album, artwork, source app

### Channel Levels (Number Sliders, -6 to +6)
- **Bass / Mid / Treble** — main EQ channels
- **Front Height** — Dolby Atmos height channel
- **Side Left / Side Right** — surround sides
- **Back Left / Back Right** — surround rears
- **Back Height** — rear Atmos height channel
- **Subwoofer Wired / Subwoofer Wireless** — sub levels

### Audio Settings (Select Entities)
- **EQ Preset** — Flat, Bass, Rock, Vocal
- **Night Mode** — Off / On
- **Dialog Mode** — Off / Level 1 / Level 2 / Level 3
- **Dirac Live** — room correction filter (filters auto-discovered from device)

### Device Attributes
The media player entity exposes these as state attributes:
`decoder`, `eq_preset`, `night_mode`, `dialog_mode`, `bass`, `mid`, `treble`,
`front_height`, `side_left`, `side_right`, `back_left`, `back_right`, `back_height`,
`sub_wired`, `sub_wireless`, `dirac_filter`, `source_app`

## Prerequisites

> **The soundbar must be already configured and working via the official Klipsch Stream app.**
>
> This integration communicates with the soundbar's local HTTP API, which is only available
> after the initial setup through the Klipsch Stream app (Wi-Fi configuration, firmware updates,
> speaker pairing, Dirac calibration, etc.).
>
> The integration does NOT replace the official app — it extends control into Home Assistant.
> Keep the Klipsch Stream app installed for initial setup and advanced configuration.

## Installation

### HACS (recommended)

1. Open HACS → Integrations → **Custom repositories**
2. Add `https://github.com/razqqm/klipsch_flexus` (type: Integration)
3. Search for **Klipsch Flexus** and install
4. Restart Home Assistant
5. Go to Settings → Devices & Services → **Add Integration** → Klipsch Flexus
6. Enter the soundbar's IP address

### Manual

1. Copy `custom_components/klipsch_flexus/` to your HA `config/custom_components/` directory
2. Restart Home Assistant
3. Add the integration via Settings → Devices & Services

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Host | — | IP address of the soundbar (required) |
| Poll interval | 15 s | Status polling interval (configurable via Options) |

**Tip:** Assign a static IP / DHCP reservation to the soundbar for reliable operation.

## How It Works

The soundbar exposes a local HTTP API on port 80 with endpoints:
- `GET /api/getData` — read device parameters
- `GET /api/setData` — write device parameters
- `GET /api/getRows` — list structured data (e.g. Dirac filters)

### Slow Device Handling

The Klipsch Flexus has a **single-threaded HTTP server** that can only process one request at a time.
This integration includes several mechanisms to ensure reliable operation:

- **Request serialization** — all API calls are serialized via `asyncio.Lock` to prevent collisions
- **Retry with backoff** — transient errors are retried (2 attempts, 0.5 s delay)
- **Adaptive timeouts** — 8 s for reads, 10 s for writes, 15 s for power commands
- **Graceful degradation** — if individual parameters fail to read, last-known cached values are used
- **Optimistic updates** — UI reflects changes immediately, then confirms via delayed poll

## Entities Created

| Entity | Type | Description |
|--------|------|-------------|
| `media_player.klipsch_flexus_core_300` | Media Player | Main control entity |
| `number.*_bass` | Number | Bass level (-6 to +6) |
| `number.*_mid` | Number | Mid level (-6 to +6) |
| `number.*_treble` | Number | Treble level (-6 to +6) |
| `number.*_front_height` | Number | Front height channel (-6 to +6) |
| `number.*_side_left` | Number | Side left channel (-6 to +6) |
| `number.*_side_right` | Number | Side right channel (-6 to +6) |
| `number.*_back_left` | Number | Back left channel (-6 to +6) |
| `number.*_back_right` | Number | Back right channel (-6 to +6) |
| `number.*_back_height` | Number | Back height channel (-6 to +6) |
| `number.*_sub_wired` | Number | Wired subwoofer level (-6 to +6) |
| `number.*_sub_wireless` | Number | Wireless subwoofer level (-6 to +6) |
| `select.*_night_mode` | Select | Night mode |
| `select.*_dialog_mode` | Select | Dialog enhancement mode |
| `select.*_eq_preset` | Select | EQ preset |
| `select.*_dirac` | Select | Dirac Live filter |

## License

MIT — see [LICENSE](LICENSE).
