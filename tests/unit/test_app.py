import pytest
from freezegun import freeze_time
from notification.app import DateTypeManager, lambda_handler


def test_DateTypeManager():
    with freeze_time("2021-11-26 09:00:00"):
        dm = DateTypeManager()
        assert dm.get_day_type() == dm.NORMAL_DAY

    with freeze_time("2021-11-29 09:00:00"):
        dm = DateTypeManager()
        assert dm.get_day_type() == dm.DAY_BEFORE_LAST_DAY

    with freeze_time("2021-11-30 09:00:00"):
        dm = DateTypeManager()
        assert dm.get_day_type() == dm.LAST_DAY

    with freeze_time("2022-01-28 09:00:00"):
        dm = DateTypeManager()
        assert dm.get_day_type() == dm.DAY_BEFORE_LAST_DAY

    with freeze_time("2022-01-31 09:00:00"):
        dm = DateTypeManager()
        assert dm.get_day_type() == dm.LAST_DAY
