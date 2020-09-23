import pytest

from avionix_airflow import AirflowOptions


@pytest.mark.parametrize(
    "local_mode,worker_image,worker_image_tag,master_image,master_image_tag",
    [
        (True, "", "", "", ""),
        (False, "", "", "", ""),
        (True, "test-image", "oldest", "", ""),
        (False, "test-image", "oldest", "", ""),
    ],
)
def test_airflow_options_images(
    local_mode: bool,
    worker_image: str,
    worker_image_tag: str,
    master_image: str,
    master_image_tag: str,
):
    options = AirflowOptions(
        "busybox",
        ["test"],
        "* * * * *",
        local_mode=local_mode,
        worker_image=worker_image,
        worker_image_tag=worker_image_tag,
        master_image=master_image,
        master_image_tag=master_image_tag,
    )

    # Assert expected master image behavior
    if master_image:
        assert options.master_image == (master_image if master_image else "")
    if not master_image and local_mode:
        assert options.master_image == "airflow-image"
    assert options.master_image_tag == (
        master_image_tag if master_image_tag else "latest"
    )
    assert options.worker_image_tag == (
        worker_image_tag if worker_image_tag else "latest"
    )
