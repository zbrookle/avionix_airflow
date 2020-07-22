from avionix.kubernetes_objects.pod import Container


class AirflowContainer(Container):
    def __init__(self, name, args):
        super().__init__(
            name=name, args=args, image="airflow-image", image_pull_policy="Never",
        )


class WebserverUI(AirflowContainer):
    def __init__(self):
        super().__init__(name="webserver", args=["webserver"])


class Scheduler(AirflowContainer):
    def __init__(self):
        super().__init__(name="scheduler", args=["scheduler"])
