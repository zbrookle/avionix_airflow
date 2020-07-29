from typing import List

from avionix.kubernetes_objects.core import (
    Container,
    HostPathVolumeSource,
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimSpec,
    PersistentVolumeClaimVolumeSource,
    PersistentVolumeSpec,
    ResourceRequirements,
    Volume,
    VolumeMount,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta


class AirflowPersistentVolume(PersistentVolume):
    def __init__(
        self, name: str, storage: str, host_path: str, access_modes: List[str]
    ):
        super().__init__(
            AirflowMeta(name, annotations={"pv.beta.kubernetes.io/gid": "1001"}),
            PersistentVolumeSpec(
                access_modes,
                capacity={"storage": storage},
                host_path=HostPathVolumeSource(host_path, type="DirectoryOrCreate"),
                storage_class_name="standard",
            ),
        )


class AirflowVolume(Volume):
    def __init__(self, name: str, claim_name: str):
        super().__init__(
            name,
            persistent_volume_claim=PersistentVolumeClaimVolumeSource(
                claim_name, read_only=False
            ),
        )


class AirflowPersistentVolumeClaim(PersistentVolumeClaim):
    def __init__(self, name: str, access_modes: List[str], storage: str):
        super().__init__(
            AirflowMeta(name),
            PersistentVolumeClaimSpec(
                access_modes,
                resources=ResourceRequirements(requests={"storage": storage}),
            ),
        )


class AirflowVolumeMount(VolumeMount):
    def __init__(self, name: str, folder: str):
        super().__init__(
            name, mount_path="/usr/local/airflow/" + folder, mount_propagation=None
        )


class PermissionSettingContainer(Container):
    def __init__(self, name: str, volume_mount: VolumeMount):
        super().__init__(
            f"{name}-set-owner",
            image="busybox",
            command=["/bin/chmod", "777", volume_mount.mountPath],
            volume_mounts=[volume_mount],
        )


class AirflowPersistentVolumeGroup:
    def __init__(self, name: str, storage: str, access_modes: List[str], folder: str):
        host_path = "/tmp/data/airflow/" + folder
        volume_name = f"{name}-volume"
        self.__volume = AirflowVolume(volume_name, f"{name}-pv-claim")
        self.__persistent_volume = AirflowPersistentVolume(
            f"{name}-pv", storage, host_path, access_modes
        )
        self.__persistent_volume_claim = AirflowPersistentVolumeClaim(
            self.__volume.persistentVolumeClaim.claimName, access_modes, storage
        )
        self.__volume_mount = AirflowVolumeMount(volume_name, folder=folder)
        self.__permission_container = PermissionSettingContainer(
            f"" f"{name}-permission-container", self.__volume_mount
        )

    @property
    def persistent_volume(self):
        return self.__persistent_volume

    @property
    def volume(self):
        return self.__volume

    @property
    def persistent_volume_claim(self):
        return self.__persistent_volume_claim

    @property
    def volume_mount(self):
        return self.__volume_mount

    @property
    def permission_container(self):
        return self.__permission_container


class AirflowLogVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, options: AirflowOptions):
        super().__init__(
            "logs",
            options.log_storage,
            access_modes=options.access_modes,
            folder="logs",
        )


class AirflowDagVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, options: AirflowOptions):
        super().__init__(
            "dags",
            options.dag_storage,
            access_modes=options.access_modes,
            folder="dags",
        )


class ExternalStorageVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, options: AirflowOptions):
        super().__init__(
            "tmp", options.dag_storage, access_modes=options.access_modes, folder="tmp"
        )
