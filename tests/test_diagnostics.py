"""Tests for Klipsch Flexus diagnostics."""

from __future__ import annotations

from unittest.mock import MagicMock

from custom_components.klipsch_flexus.diagnostics import (
    async_get_config_entry_diagnostics,
)

from .conftest import MOCK_HOST, MOCK_STATUS


async def test_diagnostics(hass) -> None:
    """Test diagnostics output."""
    mock_api = MagicMock()
    mock_api.last_response_time = 42.5
    mock_api.total_requests = 100
    mock_api.failed_requests = 2

    mock_coordinator = MagicMock()
    mock_coordinator.data = MOCK_STATUS.copy()
    mock_coordinator.dirac_filters = [{"id": 1, "name": "Filter 1"}]
    mock_coordinator.api = mock_api

    mock_entry = MagicMock()
    mock_entry.data = {"host": MOCK_HOST}
    mock_entry.options = {"scan_interval": 15}
    mock_entry.entry_id = "test_entry_id"

    hass.data = {"klipsch_flexus": {"test_entry_id": mock_coordinator}}

    result = await async_get_config_entry_diagnostics(hass, mock_entry)

    assert "entry" in result
    assert "device_status" in result
    assert "api_stats" in result
    # Host should be redacted
    assert result["entry"]["data"]["host"] == "**REDACTED**"
    assert result["api_stats"]["total_requests"] == 100
