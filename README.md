# Klipsch Flexus CORE 300

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)

Home Assistant integration for **Klipsch Flexus CORE 300** (5.1.2-Channel Dolby Atmos Sound Bar).

Controls the soundbar via its native local HTTP API — no cloud, no delays.

## Features

- **Media player** — volume, mute, power on/off, input select, sound mode
- **Playback controls** — play/pause, next/previous track, track info (title, artist, album, artwork)
- **EQ** — bass, mid, treble sliders (-6 to +6)
- **EQ presets** — Flat, Bass, Rock, Vocal
- **Subwoofer levels** — wired and wireless (-6 to +6)
- **Night mode** — Off / On
- **Dialog mode** — Off / Level 1 / Level 2 / Level 3
- **Dirac Live** — room correction filter selection (auto-discovered)
- **Configurable poll interval** via options flow

## Installation (HACS)

1. Open HACS → Integrations → **Custom repositories**
2. Add `https://github.com/razqqm/klipsch_flexus` (type: Integration)
3. Install **Klipsch Flexus**
4. Restart Home Assistant
5. Go to Settings → Devices & Services → **Add Integration** → Klipsch Flexus
6. Enter the IP address of your soundbar

## Requirements

- Klipsch Flexus CORE 300 on the same local network
- Static IP recommended for the soundbar
