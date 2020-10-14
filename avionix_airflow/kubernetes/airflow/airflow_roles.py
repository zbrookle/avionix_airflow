from avionix.kube.core import ServiceAccount
from avionix.kube.meta import ObjectMeta
from avionix.kube.rbac_authorization import (
    PolicyRule,
    Role,
    RoleBinding,
    RoleRef,
    Subject,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions


class AirflowPodRole(Role):
    def __init__(self, airflow_options: AirflowOptions):
        super().__init__(
            ObjectMeta(name="pod-controller", namespace=airflow_options.pods_namespace),
            [PolicyRule(resources=["pods"], verbs=["*"], api_groups=[""],)],
        )


class AirflowPodRoleGroup:
    def __init__(
        self, service_account: ServiceAccount, airflow_options: AirflowOptions
    ):
        self.role = AirflowPodRole(airflow_options)
        self.role_binding = RoleBinding(
            ObjectMeta(
                name="pod-controller-binding", namespace=airflow_options.pods_namespace
            ),
            RoleRef(self.role.metadata.name, "rbac.authorization.k8s.io", kind="Role"),
            [
                Subject(
                    service_account.metadata.name,
                    kind="ServiceAccount",
                    namespace=service_account.metadata.namespace,
                )
            ],
        )
