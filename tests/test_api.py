"""Tests for Klipsch Flexus API client."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from custom_components.klipsch_flexus.api import KlipschAPI


@pytest.fixture
def api():
    """Create an API client with mocked session."""
    return KlipschAPI("192.168.1.100")


async def test_get_data_success(api: KlipschAPI) -> None:
    """Test successful getData call."""
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value=[{"i32_": 25}])
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)

    mock_session = AsyncMock(spec=aiohttp.ClientSession)
    mock_session.get = MagicMock(return_value=mock_response)
    mock_session.closed = False
    api._session = mock_session
    api._own_session = False

    result = await api.get_data("player:volume")
    assert result == [{"i32_": 25}]
    assert api.total_requests == 1
    assert api.failed_requests == 0
    assert api.last_response_time is not None


async def test_get_data_retry_on_timeout(api: KlipschAPI) -> None:
    """Test retry logic on timeout."""
    call_count = 0

    async def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise TimeoutError()
        mock_resp = AsyncMock()
        mock_resp.json = AsyncMock(return_value=[{"i32_": 10}])
        mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
        mock_resp.__aexit__ = AsyncMock(return_value=False)
        return mock_resp

    mock_session = AsyncMock(spec=aiohttp.ClientSession)
    mock_session.get = mock_get
    mock_session.closed = False
    api._session = mock_session
    api._own_session = False

    result = await api.get_data("player:volume")
    assert result == [{"i32_": 10}]
    assert call_count == 3  # 2 retries + 1 success


async def test_get_data_all_retries_fail(api: KlipschAPI) -> None:
    """Test that exception is raised after all retries fail."""
    mock_session = AsyncMock(spec=aiohttp.ClientSession)
    mock_session.get = MagicMock(side_effect=TimeoutError())
    mock_session.closed = False
    api._session = mock_session
    api._own_session = False

    with pytest.raises(TimeoutError):
        await api.get_data("player:volume")


async def test_get_status_graceful_degradation(api: KlipschAPI) -> None:
    """Test graceful degradation when some params fail."""
    call_count = 0

    async def mock_get_data(path, timeout=8):
        nonlocal call_count
        call_count += 1
        if "volume" in path:
            return [{"i32_": 50}]
        if "mute" in path:
            return [{"bool_": False}]
        if "powerTarget" in path or "powermanager" in path:
            return [{"powerTarget": {"target": "on"}}]
        # Fail for everything else
        raise TimeoutError()

    api.get_data = mock_get_data
    result = await api.get_status()

    # Should still be online since not ALL params failed
    assert result["online"] is True
    assert result["volume"] == 50


async def test_get_status_all_fail(api: KlipschAPI) -> None:
    """Test offline status when all params fail."""
    api.get_data = AsyncMock(side_effect=TimeoutError())
    result = await api.get_status()
    assert result == {"online": False}


async def test_close_session(api: KlipschAPI) -> None:
    """Test session cleanup."""
    mock_session = AsyncMock(spec=aiohttp.ClientSession)
    mock_session.closed = False
    api._session = mock_session
    api._own_session = True

    await api.close()
    mock_session.close.assert_called_once()
