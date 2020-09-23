import pytest

from avionix_airflow import AirflowOptions


@pytest.mark.parametrize(
    "local_mode,worker_image,worker_image_tag,master_image,master_image_tag",
    [(True, None, None, None, None), (False, None, None, None, None)],
)
def test_airflow_options_images(
    local_mode: bool,
    worker_image: str,
    worker_image_tag: str,
    master_image: str,
    master_image_tag: str,
):
    kwargs = {
        "local_mode": local_mode,
        "worker_image": worker_image,
        "worker_image_tag": worker_image_tag,
        "master_image": master_image,
        "master_image_tag": master_image_tag,
    }
    for key in list(kwargs.keys()):
        if kwargs[key] is None:
            del kwargs[key]
    options = AirflowOptions("busybox", ["test"], "* * * * *", **kwargs)

    # Assert expected master image behavior
    if master_image:
        assert options.master_image == (master_image if master_image else "")
    if not master_image and local_mode:
        assert options.master_image == "airflow-image"
    assert options.master_image_tag == (
        master_image_tag if master_image_tag else "latest"
    )
    assert options.worker_image_tag == (
        worker_image_tag if master_image_tag else "latest"
    )
