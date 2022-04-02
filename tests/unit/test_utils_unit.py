import datetime
import pytest


@pytest.fixture
def threshold() -> int:
    return 180


@pytest.fixture
def now() -> datetime.datetime:
    return datetime.datetime.now()


@pytest.fixture
def different_date(threshold) -> datetime.datetime:
    return datetime.datetime.now() - datetime.timedelta(seconds=threshold)


def test_utils_check_timer_return_false_when_timer_less_than_target(
    now: datetime.datetime, different_date: datetime.datetime, threshold: int
) -> None:
    from cotd.utils import check_timer

    assert (
        check_timer(
            now,
            different_date,
            threshold - 1,
        )
        == False
    )


def test_utils_check_timer_return_true_when_timer_is_exact(
    now: datetime.datetime, different_date: datetime.datetime, threshold: int
) -> None:
    from cotd.utils import check_timer

    assert (
        check_timer(
            now,
            different_date,
            threshold,
        )
        == True
    )


def test_utils_check_timer_return_true_when_timer_is_expired(
    now: datetime.datetime, different_date: datetime.datetime, threshold: int
) -> None:
    from cotd.utils import check_timer

    assert (
        check_timer(
            now,
            different_date,
            threshold + 1,
        )
        == True
    )


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main(sys.argv[1:]))
