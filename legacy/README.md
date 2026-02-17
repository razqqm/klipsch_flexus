# Legacy: Klipsch Flexus without custom integration

This is the original pre-integration approach to control the Klipsch Flexus CORE 300 from Home Assistant, using only built-in HA components — no custom integration required.

## How it works

| Component | Purpose |
|-----------|---------|
| `klipsch_cast.py` | Python CLI script — polls full device state, sets any parameter |
| `klipsch.yaml` | HA package — `command_line` sensor + `rest_command` + `script` |

### Architecture

```
┌─────────────┐     GET /api/getData      ┌───────────────────┐
│  HA sensor   │ ──────────────────────── │  Klipsch Flexus   │
│  (30s poll)  │     klipsch_cast.py      │  HTTP API :80     │
└─────────────┘                           └───────────────────┘
                                                   ▲
┌─────────────┐     GET /api/setData               │
│ HA scripts  │ ───────────────────────────────────┘
│ rest_command │     (direct URL calls)
└─────────────┘
```

### Sensor (`command_line`)

Runs `klipsch_cast.py status` every 30 seconds, returns JSON with all state:
- volume, muted, input, sound mode, night/dialog mode
- bass/mid/treble, EQ preset, Dirac filter
- subwoofer levels, decoder, power state

### REST Commands

14 direct `GET` calls to the soundbar API — no Python needed:
- Volume, mute, input, sound mode, night mode, dialog mode
- Bass, mid, treble, EQ preset, Dirac filter
- Subwoofer levels (wired/wireless), power control

### Scripts (for dashboard buttons)

Ready-made scripts with mute toggle, volume +/- 5, dialog cycle, Dirac cycle, night toggle, etc.

## Setup

1. Replace `<SOUNDBAR_IP>` with your soundbar's IP in both files
2. Copy `klipsch_cast.py` to `/config/scripts/`
3. Add to `configuration.yaml`:
   ```yaml
   homeassistant:
     packages:
       klipsch: !include packages/klipsch.yaml
   ```
4. Restart Home Assistant

## Limitations (vs custom integration)

| Feature | Legacy | Custom Integration |
|---------|--------|--------------------|
| Auto-discovery | No | Yes (Zeroconf) |
| Media player entity | No | Yes |
| Playback controls | No | Yes (play/pause/next/prev) |
| Album art / track info | No | Yes |
| Surround channel levels | No | Yes (11 sliders) |
| Optimistic updates | No | Yes (instant UI) |
| Retry / error handling | Basic | Full (2x retry, fallback) |
| Translations | No | 7 languages |
| HACS install | No | One click |
| Diagnostics download | No | Yes |

## API Reference

The `klipsch_cast.py` script documents all known API endpoints. See the `PATHS` dictionary for the complete list of paths and data formats.

```bash
python3 klipsch_cast.py status          # full JSON state
python3 klipsch_cast.py volume 45       # set volume
python3 klipsch_cast.py input hdmiarc   # switch to TV ARC
python3 klipsch_cast.py mode movie      # set sound mode
python3 klipsch_cast.py power online    # wake up
python3 klipsch_cast.py player pause    # media control
python3 klipsch_cast.py dirac_filters   # list Dirac filters
```
