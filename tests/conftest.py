from datetime import datetime, timedelta, date

import pytest


@pytest.fixture()
def now_str():
    return datetime.utcnow().isoformat() + 'Z'


@pytest.fixture()
def tomorrow_str():
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_dt = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    return tomorrow_dt.isoformat() + 'Z'
