# Klipsch Flexus

[![HACS Default](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/release/razqqm/klipsch_flexus.svg?style=for-the-badge)](https://github.com/razqqm/klipsch_flexus/releases)
[![License](https://img.shields.io/github/license/razqqm/klipsch_flexus.svg?style=for-the-badge)](LICENSE)
[![Auto Discovery](https://img.shields.io/badge/Auto_Discovery-Zeroconf-44cc11.svg?style=for-the-badge)](#descoberta-automática)

[![Validate](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/validate.yaml)
[![Hassfest](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/hassfest.yaml)
[![CI](https://github.com/razqqm/klipsch_flexus/actions/workflows/ci.yaml/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/ci.yaml)
[![CodeQL](https://github.com/razqqm/klipsch_flexus/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/github-code-scanning/codeql)
[![Copilot](https://img.shields.io/badge/Copilot-Code_Review-8957e5.svg)](https://github.com/razqqm/klipsch_flexus/actions/workflows/copilot-pull-request-reviewer/copilot-pull-request-reviewer)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

🌐 [English](../README.md) | [Русский](README_ru.md) | [Deutsch](README_de.md) | [Español](README_es.md) | **Português**

---

Integração personalizada do Home Assistant para soundbars **Klipsch Flexus** — controle via **API HTTP local nativa**, sem nuvem, sem atrasos.

### Modelos compatíveis

| Modelo | Canais | Recursos |
|--------|--------|----------|
| **Flexus CORE 300** | 5.1.2 | Dirac Live, Dolby Atmos, 13 drivers |
| **Flexus CORE 200** | 3.1.2 | Dolby Atmos up-firing |
| **Flexus CORE 100** | 2.1 | Virtual Dolby Atmos |

> A soundbar deve ser pré-configurada pelo aplicativo oficial Klipsch Connect Plus (Wi-Fi, firmware, pareamento de caixas, calibração Dirac). Esta integração cuida apenas do controle diário.

## Recursos

### Media Player
- **Volume** — nível, aumentar/diminuir, silenciar
- **Energia** — ligar / standby
- **Fonte de entrada** — TV ARC, HDMI, SPDIF, Bluetooth, Google Cast
- **Modo de som** — Movie, Music, Game, Sport, Night, Direct, Surround, Stereo
- **Reprodução** — play/pausa, próxima/anterior faixa
- **Info de mídia** — título, artista, álbum, capa, app de origem

### Níveis de canal (11 controles, -6 a +6 dB)

| Canal | Descrição |
|-------|-----------|
| Front Height | Alto-falante de altura frontal Dolby Atmos |
| Back Height | Alto-falante de altura traseiro Dolby Atmos |
| Side Left / Right | Alto-falantes surround laterais |
| Back Left / Right | Alto-falantes surround traseiros |
| Subwoofer Wireless 1 / 2 | Níveis do subwoofer sem fio |
| Bass / Mid / Treble | Controles de equalização |

### Configurações de áudio (Selects)
- **Predefinição EQ** — Flat, Bass, Rock, Vocal
- **Modo noturno** — reduz a faixa dinâmica para audição silenciosa
- **Modo diálogo** — melhora a clareza da fala (3 níveis)
- **Dirac Live** — filtro de correção de sala (detectado automaticamente do dispositivo)

### Diagnósticos
- **Tempo de resposta** — duração da consulta API em ms, contadores de requisições/erros
- **Status do dispositivo** — Ligado / Standby / Offline com info do decodificador, entrada e modo de som
- **Baixar diagnósticos** — exportação completa do estado (Configurações > Dispositivos > Klipsch Flexus > Baixar diagnósticos)

### Traduções
Tradução completa da interface em **7 idiomas**: inglês, russo, alemão, espanhol, francês, italiano, português. Todos os nomes de entidades, estados e telas de configuração estão traduzidos.

## Instalação

### HACS (recomendado)

1. Abra **HACS** > Integrações > pesquise **Klipsch Flexus**
2. Instale e reinicie o Home Assistant
3. A soundbar deve ser **descoberta automaticamente** — verifique as notificações
4. Ou vá para **Configurações** > Dispositivos e serviços > **Adicionar integração** > Klipsch Flexus

### Manual

1. Copie `custom_components/klipsch_flexus/` para o diretório `config/custom_components/` do seu HA
2. Reinicie o Home Assistant
3. Adicione a integração em Configurações > Dispositivos e serviços

## Descoberta automática

A soundbar é descoberta automaticamente na sua rede via **mDNS / Zeroconf** (protocolo Google Cast).

Com a soundbar ligada, o Home Assistant mostrará uma notificação:
> Encontrado **Klipsch Flexus CORE 300** em `192.168.1.100`. Deseja adicionar esta soundbar?

**Como funciona:**
- A soundbar se anuncia como `Flexus-Core-*` via serviço mDNS `_googlecast._tcp`
- A integração identifica o dispositivo pelos registros TXT `md` (modelo) e `fn` (nome)
- Dispositivos proxy AirCast são filtrados automaticamente

Se a descoberta automática não funcionar (ex.: isolamento de rede), você sempre pode adicionar a integração manualmente informando o endereço IP.

## Configuração

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| Host | — | Endereço IP da soundbar (obrigatório) |
| Intervalo de consulta | 15 s | Configurável em Opções (5–120 s) |

**Dica:** Atribua um IP estático / reserva DHCP à soundbar.

Você pode alterar o IP depois em **Reconfigurar** (Configurações > Dispositivos > Klipsch Flexus > Reconfigurar).

## Como funciona

A soundbar disponibiliza uma API HTTP local na porta 80:
- `GET /api/getData` — ler parâmetros
- `GET /api/setData` — escrever parâmetros
- `GET /api/getRows` — listar dados estruturados (filtros Dirac)

### Design resiliente para um dispositivo lento

O Klipsch Flexus tem um **servidor HTTP single-thread** que processa uma requisição por vez. A integração é construída em torno dessa limitação:

| Mecanismo | Descrição |
|-----------|-----------|
| Serialização de requisições | Todas as chamadas API passam por `asyncio.Lock` — sem concorrência |
| Retry com espera | Erros temporários reexecutados 2x com 0,5 s de espera |
| Timeouts adaptativos | 8 s leitura, 10 s escrita, 15 s comandos de energia |
| Degradação elegante | Leituras falhas usam os últimos valores conhecidos |
| Atualizações otimistas | UI atualiza instantaneamente, depois verificado por polling |

## Entidades

| Entidade | Tipo | Categoria |
|----------|------|-----------|
| Klipsch Flexus CORE 300 | Media Player | — |
| Modo noturno | Select | Configuração |
| Modo diálogo | Select | Configuração |
| Predefinição EQ | Select | Configuração |
| Filtro Dirac | Select | Configuração |
| Back Height / Left / Right | Number (x3) | Configuração |
| Front Height | Number | Configuração |
| Side Left / Right | Number (x2) | Configuração |
| Subwoofer Wireless 1 / 2 | Number (x2) | Configuração |
| Bass / Mid / Treble | Number (x3) | Configuração |
| Tempo de resposta | Sensor | Diagnóstico |
| Status do dispositivo | Sensor | Diagnóstico |

**Total: 18 entidades** (1 media player + 4 selects + 11 numbers + 2 sensors)

## Solução de problemas

| Problema | Solução |
|----------|---------|
| Não conecta | Verifique se a soundbar está na mesma rede. Tente: `http://<IP>/api/getData?path=player:volume&roles=value` |
| Entidades indisponíveis | O app Klipsch pode estar consultando simultaneamente — feche-o |
| Atualizações lentas | Aumente o intervalo de consulta em Opções |
| Integração não carrega | Verifique os logs do HA por erros de importação. Requer HA 2024.4.0+ |

## Limitações conhecidas

- Uma soundbar por entrada de integração (adicione várias separadamente)
- Sem gerenciamento de multi-room / grupos surround sem fio (use Klipsch Connect Plus)
- AirPlay e Cast não são utilizados — apenas a API HTTP nativa
- A configuração inicial requer o app oficial Klipsch Connect Plus

## Licença

MIT — ver [LICENSE](../LICENSE).
