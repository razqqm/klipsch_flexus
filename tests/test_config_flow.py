"""Tests for Klipsch Flexus config flow."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.klipsch_flexus.const import DOMAIN

from .conftest import MOCK_HOST, MOCK_STATUS


async def test_user_flow_success(hass: HomeAssistant) -> None:
    """Test successful user config flow."""
    with patch(
        "custom_components.klipsch_flexus.config_flow.KlipschAPI"
    ) as mock_cls:
        api = mock_cls.return_value
        api.get_status = AsyncMock(return_value=MOCK_STATUS)
        api.close = AsyncMock()

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_HOST: MOCK_HOST}
        )
        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == f"Klipsch Flexus ({MOCK_HOST})"
        assert result["data"] == {CONF_HOST: MOCK_HOST}


async def test_user_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test config flow when device is offline."""
    with patch(
        "custom_components.klipsch_flexus.config_flow.KlipschAPI"
    ) as mock_cls:
        api = mock_cls.return_value
        api.get_status = AsyncMock(return_value={"online": False})
        api.close = AsyncMock()

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_HOST: MOCK_HOST}
        )
        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_exception(hass: HomeAssistant) -> None:
    """Test config flow when API raises exception."""
    with patch(
        "custom_components.klipsch_flexus.config_flow.KlipschAPI"
    ) as mock_cls:
        api = mock_cls.return_value
        api.get_status = AsyncMock(side_effect=ConnectionError)
        api.close = AsyncMock()

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_HOST: MOCK_HOST}
        )
        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {"base": "cannot_connect"}
