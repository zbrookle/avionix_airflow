from typing import List

from avionix.kube.core import ServiceAccount
from avionix.kube.rbac_authorization import (
    PolicyRule,
    Role,
    RoleBinding,
    RoleRef,
    Subject,
)

from avionix_airflow.kubernetes.namespace_meta import AirflowMeta


class AirflowRole(Role):
    def __init__(self, name: str, rules: List[PolicyRule]):
        super().__init__(AirflowMeta(name), rules)


class AirflowRoleBinding(RoleBinding):
    def __init__(self, name: str, role_ref: RoleRef, subjects: List[Subject]):
        super().__init__(AirflowMeta(name), role_ref, subjects)


class AirflowPodRole(AirflowRole):
    def __init__(self):
        super().__init__(
            "pod-reader",
            [
                PolicyRule(
                    resources=["pods"],
                    verbs=["get", "watch", "list", "create", "update", "delete"],
                    api_groups=[""],
                )
            ],
        )


class AirflowPodRoleGroup:
    def __init__(self, service_account: ServiceAccount):
        self.role = AirflowPodRole()
        self.role_binding = AirflowRoleBinding(
            "pod-reader-binding",
            RoleRef(self.role.metadata.name, "rbac.authorization.k8s.io", kind="Role"),
            [Subject(service_account.metadata.name, kind="ServiceAccount")],
        )
