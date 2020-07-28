import pytest

network_test = pytest.mark.flaky(reruns=5, reruns_delay=2)
