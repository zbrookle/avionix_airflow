from avionix import ChartDependency


class StableChartDependency(ChartDependency):
    def __init__(self, name: str, version: str, values: dict):
        super().__init__(
            name, version, "https://charts.helm.sh/stable", "stable", values=values,
        )
