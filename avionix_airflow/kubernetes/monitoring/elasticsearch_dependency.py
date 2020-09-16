from avionix import ChartDependency
from avionix.kube.core import PersistentVolumeClaimSpec, ResourceRequirements


class ElasticSearchDependency(ChartDependency):

    _labels = {"storage-type": "elasticsearch"}
    _storage = {"storage": "100Mi"}
    _access_modes = ["ReadWriteOnce"]

    def __init__(self):
        super().__init__(
            "elasticsearch",
            "7.8.1",
            "https://helm.elastic.co",
            "elastic",
            values={
                "replicas": 1,
                "minimumMasterNodes": 1,
                "antiAffinity": "soft",
                "esJavaOpts": "-Xmx128m -Xms128m",
                "resources": {
                    "requests": {"cpu": "100m", "memory": "512M"},
                    "limits": {"cpu": "1000m", "memory": "512M"},
                },
                "volumeClaimTemplate": PersistentVolumeClaimSpec(
                    access_modes=self._access_modes,
                    resources=ResourceRequirements(requests=self._storage),
                    storage_class_name="standard",
                ).to_dict(),
                "service": {"type": "NodePort", "nodePort": 30012},
            },
        )
