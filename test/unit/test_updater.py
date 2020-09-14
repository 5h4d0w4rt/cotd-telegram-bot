import pytest
import cotd.updater


def test_cotd_initialized(config: cotd.updater.Config):
    cotd_bot = cotd.updater.COTDBot(config=config)
    assert 
