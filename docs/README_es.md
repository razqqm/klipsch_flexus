# Klipsch Flexus

[![HACS Default](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/release/razqqm/klipsch_flexus.svg?style=for-the-badge)](https://github.com/razqqm/klipsch_flexus/releases)
[![License](https://img.shields.io/github/license/razqqm/klipsch_flexus.svg?style=for-the-badge)](LICENSE)
[![Auto Discovery](https://img.shields.io/badge/Auto_Discovery-Zeroconf-44cc11.svg?style=for-the-badge)](#descubrimiento-automático)

[![Validate](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml)
[![Hassfest](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml)
[![CI](https://github.com/razqqm/klipsch_flexus/actions/workflows/ci.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/ci.yaml)
[![CodeQL](https://github.com/razqqm/klipsch_flexus/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/github-code-scanning/codeql)
[![Copilot](https://img.shields.io/badge/Copilot-Code_Review-8957e5.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/copilot-pull-request-reviewer/copilot-pull-request-reviewer)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

🌐 [English](../README.md) | [Русский](README_ru.md) | [Deutsch](README_de.md) | **Español** | [Português](README_pt.md)

---

Integración personalizada de Home Assistant para barras de sonido **Klipsch Flexus** — control mediante **API HTTP local nativa**, sin nube, sin retrasos.

### Modelos compatibles

| Modelo | Canales | Características |
|--------|---------|----------------|
| **Flexus CORE 300** | 5.1.2 | Dirac Live, Dolby Atmos, 13 drivers |
| **Flexus CORE 200** | 3.1.2 | Dolby Atmos up-firing |
| **Flexus CORE 100** | 2.1 | Virtual Dolby Atmos |

> La barra de sonido debe estar preconfigurada mediante la aplicación oficial Klipsch Connect Plus (Wi-Fi, firmware, emparejamiento de altavoces, calibración Dirac). Esta integración solo se encarga del control diario.

## Características

### Reproductor multimedia
- **Volumen** — nivel, subir/bajar, silenciar
- **Encendido** — encender / modo espera
- **Fuente de entrada** — TV ARC, HDMI, SPDIF, Bluetooth, Google Cast
- **Modo de sonido** — Movie, Music, Game, Sport, Night, Direct, Surround, Stereo
- **Reproducción** — play/pausa, pista siguiente/anterior
- **Info multimedia** — título, artista, álbum, carátula, app de origen

### Niveles de canal (11 controles, -6 a +6 dB)

| Canal | Descripción |
|-------|-------------|
| Front Height | Altavoz de altura frontal Dolby Atmos |
| Back Height | Altavoz de altura trasero Dolby Atmos |
| Side Left / Right | Altavoces surround laterales |
| Back Left / Right | Altavoces surround traseros |
| Subwoofer Wireless 1 / 2 | Niveles de subwoofer inalámbrico |
| Bass / Mid / Treble | Controles de ecualización |

### Ajustes de audio (Selects)
- **Preajuste EQ** — Flat, Bass, Rock, Vocal
- **Modo nocturno** — reduce el rango dinámico para escucha silenciosa
- **Modo diálogo** — mejora la claridad del habla (3 niveles)
- **Dirac Live** — filtro de corrección de sala (detectado automáticamente del dispositivo)

### Diagnósticos
- **Tiempo de respuesta** — duración de la consulta API en ms, contadores de peticiones/errores
- **Estado del dispositivo** — Encendido / Espera / Sin conexión con info del decodificador, entrada y modo de sonido
- **Descargar diagnósticos** — exportación completa del estado (Ajustes > Dispositivos > Klipsch Flexus > Descargar diagnósticos)

### Traducciones
Traducción completa de la interfaz en **7 idiomas**: inglés, ruso, alemán, español, francés, italiano, portugués. Todos los nombres de entidades, estados y pantallas de configuración están traducidos.

## Instalación

### HACS (recomendado)

1. Abra **HACS** > Integraciones > busque **Klipsch Flexus**
2. Instale y reinicie Home Assistant
3. La barra de sonido debería **descubrirse automáticamente** — revise las notificaciones
4. O vaya a **Ajustes** > Dispositivos y servicios > **Agregar integración** > Klipsch Flexus

### Manual

1. Copie `custom_components/klipsch_flexus/` al directorio `config/custom_components/` de su HA
2. Reinicie Home Assistant
3. Agregue la integración desde Ajustes > Dispositivos y servicios

## Descubrimiento automático

La barra de sonido se descubre automáticamente en su red mediante **mDNS / Zeroconf** (protocolo Google Cast).

Con la barra de sonido encendida, Home Assistant mostrará una notificación:
> Se encontró **Klipsch Flexus CORE 300** en `192.168.1.100`. ¿Desea agregar esta barra de sonido?

**Cómo funciona:**
- La barra se anuncia como `Flexus-Core-*` a través del servicio mDNS `_googlecast._tcp`
- La integración identifica el dispositivo por los registros TXT `md` (modelo) y `fn` (nombre)
- Los dispositivos proxy AirCast se filtran automáticamente

Si el descubrimiento automático no funciona (p.ej. aislamiento de red), siempre puede agregar la integración manualmente ingresando la dirección IP.

## Configuración

| Parámetro | Predeterminado | Descripción |
|-----------|---------------|-------------|
| Host | — | Dirección IP de la barra de sonido (obligatorio) |
| Intervalo de consulta | 15 s | Configurable en Opciones (5–120 s) |

**Consejo:** Asigne una IP estática / reserva DHCP a la barra de sonido.

Puede cambiar la IP más tarde mediante **Reconfigurar** (Ajustes > Dispositivos > Klipsch Flexus > Reconfigurar).

## Cómo funciona

La barra de sonido expone una API HTTP local en el puerto 80:
- `GET /api/getData` — leer parámetros
- `GET /api/setData` — escribir parámetros
- `GET /api/getRows` — listar datos estructurados (filtros Dirac)

### Diseño resiliente para un dispositivo lento

El Klipsch Flexus tiene un **servidor HTTP de un solo hilo** que procesa una petición a la vez. La integración está diseñada en torno a esta limitación:

| Mecanismo | Descripción |
|-----------|-------------|
| Serialización de peticiones | Todas las llamadas API pasan por `asyncio.Lock` — sin concurrencia |
| Reintento con espera | Errores temporales reintentados 2x con 0,5 s de espera |
| Timeouts adaptativos | 8 s lectura, 10 s escritura, 15 s comandos de encendido |
| Degradación elegante | Lecturas fallidas usan los últimos valores conocidos |
| Actualizaciones optimistas | UI se actualiza al instante, luego se verifica por polling |

## Entidades

| Entidad | Tipo | Categoría |
|---------|------|-----------|
| Klipsch Flexus CORE 300 | Media Player | — |
| Modo nocturno | Select | Configuración |
| Modo diálogo | Select | Configuración |
| Preajuste EQ | Select | Configuración |
| Filtro Dirac | Select | Configuración |
| Back Height / Left / Right | Number (x3) | Configuración |
| Front Height | Number | Configuración |
| Side Left / Right | Number (x2) | Configuración |
| Subwoofer Wireless 1 / 2 | Number (x2) | Configuración |
| Bass / Mid / Treble | Number (x3) | Configuración |
| Tiempo de respuesta | Sensor | Diagnóstico |
| Estado del dispositivo | Sensor | Diagnóstico |

**Total: 18 entidades** (1 reproductor + 4 selects + 11 numbers + 2 sensors)

## Solución de problemas

| Problema | Solución |
|----------|----------|
| No se puede conectar | Verifique que la barra de sonido esté en la misma red. Pruebe: `http://<IP>/api/getData?path=player:volume&roles=value` |
| Entidades no disponibles | La app Klipsch puede estar consultando simultáneamente — ciérrela |
| Actualizaciones lentas | Aumente el intervalo de consulta en Opciones |
| La integración no carga | Revise los logs de HA por errores de importación. Se requiere HA 2024.4.0+ |

## Versión Legacy (sin integración personalizada)

Si prefiere no instalar una integración personalizada, consulte la carpeta [`legacy/`](../legacy/) para un enfoque autónomo usando solo componentes integrados de HA (`command_line` sensor + `rest_command` + scripts).

Esta fue la implementación original antes de crear la integración. Proporciona control básico de volumen/entrada/modo a través de botones del panel, pero sin entidad de reproductor multimedia, controles de reproducción, descubrimiento automático ni traducciones. Consulte [`legacy/README.md`](../legacy/README.md).

## Limitaciones conocidas

- Una barra de sonido por entrada de integración (agregue varias por separado)
- Sin gestión de multiroom / grupos de altavoces inalámbricos (use Klipsch Connect Plus)
- AirPlay y Cast no se utilizan — solo la API HTTP nativa
- La configuración inicial requiere la app oficial Klipsch Connect Plus

## Licencia

MIT — ver [LICENSE](../LICENSE).
