from typing import List

from avionix.kubernetes_objects.core import (
    Container,
    CSIPersistentVolumeSource,
    HostPathVolumeSource,
    LabelSelector,
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
        self,
        name: str,
        storage: str,
        host_path: str,
        access_modes: List[str],
        airflow_options: AirflowOptions,
    ):
        self.__airflow_options = airflow_options
        volume_spec = PersistentVolumeSpec(
            access_modes,
            capacity={"storage": storage},
            host_path=HostPathVolumeSource(host_path, type="DirectoryOrCreate"),
            storage_class_name=self.__storage_class,
        )
        if self.__airflow_options.aws_efs_id:
            volume_spec.csi = CSIPersistentVolumeSource(
                driver="efs.csi.aws.com", volume_handle=airflow_options.aws_efs_id
            )

        super().__init__(
            AirflowMeta(
                name,
                annotations={"pv.beta.kubernetes.io/gid": "1001"},
                labels={"storage-type": name},
            ),
            volume_spec,
        )

    @property
    def __storage_class(self):
        if self.__airflow_options.aws_efs_id:
            return "efs-sc"
        return "standard"


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
                selector=LabelSelector({"storage-type": name}),
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
    def __init__(
        self,
        name: str,
        storage: str,
        access_modes: List[str],
        folder: str,
        airflow_options: AirflowOptions,
    ):
        host_path = "/tmp/data/airflow/" + folder
        self.__volume = AirflowVolume(name, name)
        self.__persistent_volume = AirflowPersistentVolume(
            name, storage, host_path, access_modes, airflow_options
        )
        self.__persistent_volume_claim = AirflowPersistentVolumeClaim(
            self.__volume.persistentVolumeClaim.claimName, access_modes, storage
        )
        self.__volume_mount = AirflowVolumeMount(name, folder=folder)
        self.__permission_container = PermissionSettingContainer(
            f"{name}-permission-container", self.__volume_mount
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
            airflow_options=options,
        )


class AirflowDagVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, options: AirflowOptions):
        super().__init__(
            "dags",
            options.dag_storage,
            access_modes=options.access_modes,
            folder="dags",
            airflow_options=options,
        )


class ExternalStorageVolumeGroup(AirflowPersistentVolumeGroup):
    def __init__(self, options: AirflowOptions):
        super().__init__(
            "tmp",
            options.dag_storage,
            access_modes=options.access_modes,
            folder="tmp",
            airflow_options=options,
        )
