from avionix import ChartDependency


class ElasticSearchDependency(ChartDependency):
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
                "volumeClaimTemplate": {
                    "accessModes": ["ReadWriteOnce"],
                    "storageClassName": "standard",
                    "resources": {"requests": {"storage": "100M"}},
                },
                "service": {"type": "NodePort", "nodePort": 30012},
            },
        )
