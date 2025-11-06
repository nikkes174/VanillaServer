import asyncio
import pathlib
import sys

import pytest

from decorators_for_logging import event, group_logger, logger_for_request

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))


@pytest.mark.asyncio
async def test_logger_for_request_logs_output(capsys):
    @logger_for_request
    async def fake_request():
        await asyncio.sleep(0.01)
        return "ok"

    result = await fake_request()
    captured = capsys.readouterr()

    assert result == "ok"
    assert "Начало запроса" in captured.out
    assert "Конец запроса" in captured.out


@pytest.mark.asyncio
async def test_group_logger_sets_event(capsys):
    called = False

    @group_logger
    async def fake_group():
        nonlocal called
        called = True
        await asyncio.sleep(0.01)
        return [1, 2, 3]

    assert not event.is_set()
    result = await fake_group()
    captured = capsys.readouterr()

    assert called
    assert result == [1, 2, 3]
    assert "выполнено за" in captured.out
