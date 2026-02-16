# Klipsch Flexus CORE 300

**Language / Язык:** English | [Русский](README_ru.md)

[![HACS Default](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/release/razqqm/klipsch_flexus.svg?style=for-the-badge)](https://github.com/razqqm/klipsch_flexus/releases)
[![License](https://img.shields.io/github/license/razqqm/klipsch_flexus.svg?style=for-the-badge)](LICENSE)

[![Validate](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml)
[![Hassfest](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml)
[![CI](https://github.com/razqqm/klipsch_flexus/actions/workflows/ci.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/ci.yaml)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Home Assistant custom integration for **Klipsch Flexus CORE 300** — a 5.1.2-Channel Dolby Atmos Sound Bar.

Controls the soundbar via its **native local HTTP API** — no cloud, no delays. Partially replaces the Klipsch Connect Plus app for day-to-day use.

> The soundbar must be pre-configured via the official Klipsch Connect Plus app (Wi-Fi, firmware, speaker pairing, Dirac calibration). This integration handles ongoing control only.

## Features

### Media Player
- **Volume** — set level, step up/down, mute/unmute
- **Power** — turn on / standby
- **Input source** — TV ARC, HDMI, SPDIF, Bluetooth, Google Cast
- **Sound mode** — Movie, Music, Game, Sport, Night, Direct, Surround, Stereo
- **Playback** — play/pause, next/previous track
- **Media info** — title, artist, album, artwork, source app

### Channel Levels (11 sliders, -6 to +6 dB)

| Channel | Description |
|---------|-------------|
| Front Height | Dolby Atmos front height speaker |
| Back Height | Dolby Atmos rear height speaker |
| Side Left / Right | Surround side speakers |
| Back Left / Right | Surround rear speakers |
| Subwoofer Wireless 1 / 2 | Wireless subwoofer levels |
| Bass / Mid / Treble | Tone EQ controls |

### Audio Settings (Selects)
- **EQ Preset** — Flat, Bass, Rock, Vocal
- **Night Mode** — reduces dynamic range for quiet listening
- **Dialog Mode** — boosts dialog clarity (3 levels)
- **Dirac Live** — room correction filter (auto-discovered from device)

### Diagnostics
- **Response Time** — API poll duration in ms, request/failure counters
- **Device Status** — On / Standby / Offline with decoder, input, sound mode info
- **Download diagnostics** — full device state export (Settings > Devices > Klipsch Flexus > Download diagnostics)

### Translations
Full UI translation in **7 languages**: English, Russian, German, Spanish, French, Italian, Portuguese. All entity names, states, and configuration screens are translated.

## Installation

### HACS (recommended)

1. Open **HACS** > Integrations > search **Klipsch Flexus**
2. Install and restart Home Assistant
3. Go to **Settings** > Devices & Services > **Add Integration** > Klipsch Flexus
4. Enter the soundbar's IP address

### Manual

1. Copy `custom_components/klipsch_flexus/` to your HA `config/custom_components/` directory
2. Restart Home Assistant
3. Add the integration via Settings > Devices & Services

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Host | — | IP address of the soundbar (required) |
| Poll interval | 15 s | Configurable via Options (5–120 s) |

**Tip:** Assign a static IP / DHCP reservation to the soundbar for reliable operation.

You can change the IP address later via **Reconfigure** (Settings > Devices > Klipsch Flexus > Reconfigure).

## How It Works

The soundbar exposes a local HTTP API on port 80:
- `GET /api/getData` — read parameters
- `GET /api/setData` — write parameters
- `GET /api/getRows` — list structured data (Dirac filters)

### Resilient Design for a Slow Device

The Klipsch Flexus has a **single-threaded HTTP server** that processes one request at a time. The integration is built around this constraint:

| Mechanism | Description |
|-----------|-------------|
| Request serialization | All API calls go through `asyncio.Lock` — no concurrent requests |
| Retry with backoff | Transient errors retried 2x with 0.5 s delay |
| Adaptive timeouts | 8 s reads, 10 s writes, 15 s power commands |
| Graceful degradation | Failed reads fall back to last-known cached values |
| Optimistic updates | UI updates instantly, then verified via delayed poll |

## Entities

| Entity | Type | Category |
|--------|------|----------|
| Klipsch Flexus CORE 300 | Media Player | — |
| Night Mode | Select | Config |
| Dialog Mode | Select | Config |
| EQ Preset | Select | Config |
| Dirac Filter | Select | Config |
| Back Height / Left / Right | Number (x3) | Config |
| Front Height | Number | Config |
| Side Left / Right | Number (x2) | Config |
| Subwoofer Wireless 1 / 2 | Number (x2) | Config |
| Bass / Mid / Treble | Number (x3) | Config |
| Response Time | Sensor | Diagnostic |
| Device Status | Sensor | Diagnostic |

**Total: 18 entities** (1 media player + 4 selects + 11 numbers + 2 sensors)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Cannot connect | Check that the soundbar is on the same network. Try: `http://<IP>/api/getData?path=player:volume&roles=value` |
| Entities unavailable | The Klipsch app may be polling simultaneously — close it and retry |
| Slow updates | Increase poll interval in Options (Settings > Devices > Klipsch Flexus > Configure) |
| Integration not loading | Check Home Assistant logs for import errors. Ensure you're on HA 2024.4.0+ |

## Known Limitations

- One soundbar per integration entry (add multiple as separate entries)
- No multi-room / wireless surround group management (use Klipsch Connect Plus app)
- AirPlay and Cast protocols are not used — only the native HTTP API
- Initial device setup requires the official Klipsch Connect Plus app

## License

MIT — see [LICENSE](LICENSE).
