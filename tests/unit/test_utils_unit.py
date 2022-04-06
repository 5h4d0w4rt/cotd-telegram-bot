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


@pytest.fixture
def webm_test_out_file():
    import pathlib

    out = pathlib.Path("test.mp4")
    yield out
    out.unlink()


def fake_webm_to_mp4(outs):
    import subprocess

    out = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "testsrc2=d=1[out0];sine=d=1[out1]",
            outs
        ]
    )

    return out.returncode

@pytest.mark.xfail(reason="ffmpeg is disabled, expected to fail")
def test_utils_webm_to_mp4_return_false(webm_test_out_file):
    import subprocess

    assert fake_webm_to_mp4(webm_test_out_file) == 0
    assert (
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", webm_test_out_file, "-f", "null", "-"]
        ).returncode
        == 0
    )


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main(sys.argv[1:]))
